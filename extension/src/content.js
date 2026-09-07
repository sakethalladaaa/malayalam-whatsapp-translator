(() => {
  "use strict";

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

    popup.appendChild(text);
    popup.appendChild(button);
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
  }

  document.addEventListener("mouseup", () => {
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
