(() => {
  "use strict";

  const MESSAGE_SELECTOR = '[data-testid^="conv-msg-"]';
  const MESSAGE_TEXT_SELECTOR =
    '[data-testid="msg-container"] [data-testid="selectable-text"]';

  function findMessageContainer(node) {
    let current = node instanceof Element ? node : node?.parentElement;

    while (current && current !== document.body) {
      if (current.matches(MESSAGE_SELECTOR)) {
        return current;
      }

      current = current.parentElement;
    }

    return null;
  }

  function extractMessageText(container) {
    if (!container) {
      return "";
    }

    const textElement = container.querySelector(MESSAGE_TEXT_SELECTOR);

    if (!textElement) {
      return "";
    }

    return (textElement.innerText || textElement.textContent || "").trim();
  }

  window.MalayalamTranslatorWhatsAppDOM = {
    findMessageContainer,
    extractMessageText,
  };
})();
