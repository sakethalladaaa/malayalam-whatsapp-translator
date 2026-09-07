(() => {
  "use strict";

  const API_URL = "http://127.0.0.1:8000/translate";
  let popup = null;

  function removePopup() {
    if (popup) {
      popup.remove();
      popup = null;
    }
  }

  function createPopup(selectedText) {
    removePopup();

    popup = document.createElement("div");
    popup.className = "malayalam-translator-popup";

    const text = document.createElement("div");
    text.className = "malayalam-translator-text";
    text.textContent = selectedText;

    const button = document.createElement("button");
    button.className = "malayalam-translator-button";
    button.type = "button";
    button.textContent = "Translate";

    const result = document.createElement("div");
    result.className = "malayalam-translator-result";

    popup.appendChild(text);
    popup.appendChild(button);
    popup.appendChild(result);
    document.body.appendChild(popup);

    const selection = window.getSelection();
    if (!selection || selection.rangeCount === 0) {
      removePopup();
      return;
    }

    const rect = selection.getRangeAt(0).getBoundingClientRect();

    popup.style.left = `${Math.max(8, rect.left)}px`;
    popup.style.top = `${Math.min(
      window.innerHeight - popup.offsetHeight - 8,
      rect.bottom + 8
    )}px`;

    button.addEventListener("click", async () => {
      button.disabled = true;
      button.textContent = "Translating...";
      result.textContent = "";

      try {
        const response = await fetch(API_URL, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            text: selectedText,
          }),
        });

        if (!response.ok) {
          throw new Error(`Backend returned ${response.status}`);
        }

        const data = await response.json();

        if (typeof data.translation === "string" && data.translation.trim()) {
          result.textContent = data.translation;
        } else {
          result.textContent = "Translation unavailable.";
        }
      } catch (error) {
        console.error(
          "[Malayalam WhatsApp Translator] Translation failed:",
          error
        );
        result.textContent = "Unable to connect to translation service.";
      } finally {
        button.disabled = false;
        button.textContent = "Translate";
      }
    });
  }

  document.addEventListener("mouseup", (event) => {
    if (popup && popup.contains(event.target)) {
      return;
    }

    const selectedText = window.getSelection()?.toString().trim();

    if (!selectedText) {
      removePopup();
      return;
    }

    createPopup(selectedText);
  });

  document.addEventListener("mousedown", (event) => {
    if (popup && !popup.contains(event.target)) {
      removePopup();
    }
  });
})();
