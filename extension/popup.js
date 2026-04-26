document.getElementById("scanBtn").onclick = () => {
  const status = document.getElementById("status");
  status.innerText = "Scanning...";

  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    const tabId = tabs[0].id;

    chrome.tabs.sendMessage(tabId, { action: "scan" }, () => {
      if (chrome.runtime.lastError) {
        status.innerText = "❌ Open a LinkedIn job page";
      } else {
        status.innerText = "✅ Scan triggered";
      }
    });
  });
};