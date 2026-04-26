chrome.runtime.onMessage.addListener(async (request, sender, sendResponse) => {
  if (request.action === "predict") {
    try {
      const res = await fetch("https://securehire-api.onrender.com/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(request.payload)
      });

      const data = await res.json();
      sendResponse(data);

    } catch (e) {
      sendResponse({ error: "API failed" });
    }
  }

  return true;
});