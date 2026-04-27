console.log("✅ SecureHire content.js injected");

let isRunning = false;
let lastSignature = "";

// 🔥 JOB PAGE DETECTION
function isJobPage(title, desc) {
  const text = (title + " " + desc).toLowerCase();

  const strongSignals = [
    "job description",
    "responsibilities",
    "requirements",
    "apply",
    "experience"
  ];

  const weakSignals = [
    "years", "salary", "location", "skills", "role"
  ];

  let strong = strongSignals.filter(w => text.includes(w)).length;
  let weak = weakSignals.filter(w => text.includes(w)).length;

  return desc.length > 100 && (strong >= 1 || weak >= 2);
}

// 🔥 CONTEXT CHECK
function isLikelyJobContext(title, desc) {
  const text = (title + " " + desc).toLowerCase();

  const signals = [
    "job", "apply", "experience", "years", "salary",
    "responsibilities", "requirements", "skills",
    "location", "opening", "hiring"
  ];

  let count = signals.filter(w => text.includes(w)).length;

  return desc.length > 150 && count >= 1;
}

// 🔥 MAIN FUNCTION
async function runSecureHire() {
  if (isRunning) return;
  isRunning = true;

  console.log("🚀 runSecureHire triggered");

  document.getElementById("securehire-badge")?.remove();
  document.getElementById("securehire-loading")?.remove();

  const title =
    document.querySelector("h1")?.innerText ||
    document.querySelector("h2")?.innerText ||
    document.title ||
    "";

  const desc =
    document.querySelector(".styles_job-desc-container__txpYf")?.innerText ||
    document.querySelector(".jobs-description-content__text")?.innerText ||
    document.querySelector("article")?.innerText ||
    document.querySelector("main")?.innerText ||
    document.body.innerText.slice(0, 3000);

  console.log("🧠 TITLE:", title);
  console.log("🧠 DESC LENGTH:", desc.length);

  // ❌ NOT A JOB PAGE
  if (!title || !isJobPage(title, desc)) {
    console.log("❌ Not a job page");

    if (isLikelyJobContext(title, desc)) {
      const badge = document.createElement("div");
      badge.id = "securehire-badge";
      badge.innerText = "⚠️ Not a job posting page";

      badge.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 10px;
        border-radius: 8px;
        background: #ccc;
        color: #000;
        z-index: 9999;
        font-size: 14px;
      `;

      document.body.appendChild(badge);
    }

    isRunning = false;
    return;
  }

  // 🔥 SALARY EXTRACTION (FIXED)
  let salaryText = "";

  const salaryElement =
    document.querySelector("[class*='salary']") ||
    document.querySelector("[class*='Salary']");

  if (salaryElement) {
    salaryText = salaryElement.innerText;
  }

  // 🔥 fallback detection
  if (!salaryText) {
  const body = document.body.innerText.toLowerCase();

  if (body.includes("lpa") || body.includes("₹") || body.includes("ctc")) {
    salaryText = "₹ salary mentioned";
  }
}

  console.log("💰 SALARY:", salaryText);

  // 🔹 LOADING
  const loading = document.createElement("div");
  loading.id = "securehire-loading";
  loading.innerText = "Analyzing job...";
  loading.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background: #333;
    color: white;
    padding: 10px;
    z-index: 9999;
    border-radius: 6px;
  `;
  document.body.appendChild(loading);

  // 🔥 CALL BACKEND (UPDATED PAYLOAD)
  chrome.runtime.sendMessage(
    {
      action: "predict",
      payload: {
        title,
        description: desc,
        requirements: "",
        salary: salaryText   // ✅ FIXED
      }
    },
    (data) => {
      loading.remove();

      if (!data || data.error) {
        console.error("❌ API failed");
        isRunning = false;
        return;
      }

      const risk = (data.confidence * 100).toFixed(0);
      const real = ((1 - data.confidence) * 100).toFixed(0);

      const reasonsText = data.reasons && data.reasons.length
        ? "\n\nReasons:\n• " + data.reasons.join("\n• ")
        : "";

      const badge = document.createElement("div");
      badge.id = "securehire-badge";

      badge.innerText =
        `SecureHire: ${data.verdict}\nReal: ${real}% | Risk: ${risk}%${reasonsText}`;

      let bg =
        data.verdict === "HIGH RISK"
          ? "#ff4d4d"
          : data.verdict === "SUSPICIOUS"
          ? "#ffe066"
          : "#b6fcb6";

      badge.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 12px 14px;
        border-radius: 10px;
        font-size: 13px;
        line-height: 1.4;
        background: ${bg};
        color: #000;
        z-index: 9999;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        white-space: pre-line;
        max-width: 300px;
      `;

      document.body.appendChild(badge);

      isRunning = false;
    }
  );
}

// MESSAGE LISTENER
chrome.runtime.onMessage.addListener((req) => {
  if (req.action === "scan") {
    runSecureHire();
  }
});

// PAGE CHANGE DETECTION
setInterval(() => {
  const title =
    document.querySelector("h1")?.innerText ||
    document.title;

  const snippet = document.body.innerText.slice(0, 200);

  const signature = title + snippet;

  if (signature && signature !== lastSignature) {
    lastSignature = signature;

    console.log("🔄 Page changed → auto scan");
    runSecureHire();
  }
}, 2500);