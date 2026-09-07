(() => {
  "use strict";

  document.addEventListener("mouseup", () => {
    const selectedText = window.getSelection()?.toString().trim();

    if (!selectedText) {
      return;
    }

    console.log("[Malayalam WhatsApp Translator] Selected text:", selectedText);
  });
})();
