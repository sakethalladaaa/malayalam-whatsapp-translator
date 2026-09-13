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

    const viewportPadding = 8;
    const maxLeft = Math.max(
      viewportPadding,
      window.innerWidth - popup.offsetWidth - viewportPadding
    );
    const left = Math.min(
      Math.max(viewportPadding, rect.left),
      maxLeft
    );

    const spaceBelow = window.innerHeight - rect.bottom;
    const preferredTop =
      spaceBelow >= popup.offsetHeight + viewportPadding
        ? rect.bottom + viewportPadding
        : rect.top - popup.offsetHeight - viewportPadding;
    const maxTop = Math.max(
      viewportPadding,
      window.innerHeight - popup.offsetHeight - viewportPadding
    );
    const top = Math.min(Math.max(viewportPadding, preferredTop), maxTop);

    popup.style.left = `${left}px`;
    popup.style.top = `${top}px`;

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

    const selection = window.getSelection();
    const selectedText = selection?.toString().trim();

    if (!selectedText) {
      removePopup();
      return;
    }

    const anchorNode = selection?.anchorNode;
    const focusNode = selection?.focusNode;
    const domHelper = window.MalayalamTranslatorWhatsAppDOM;

    const anchorMessage = domHelper?.findMessageContainer(anchorNode);
    const focusMessage = domHelper?.findMessageContainer(focusNode);

    if (
      !anchorMessage ||
      !focusMessage ||
      anchorMessage !== focusMessage
    ) {
      removePopup();
      return;
    }

    const textToTranslate = selectedText;

    createPopup(textToTranslate);
  });

  document.addEventListener("mousedown", (event) => {
    if (popup && !popup.contains(event.target)) {
      removePopup();
    }
  });
})();
