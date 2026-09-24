/* VisionJev project site — progressive enhancement only.
   The page reads completely without this file. The only enhancement is the
   BibTeX copy button, which stays hidden unless the Clipboard API is actually
   usable, so no-JS and insecure-context visitors never see a dead control. */
(function () {
  'use strict';

  var button = document.getElementById('copy-bibtex');
  var status = document.getElementById('copy-status');
  if (!button || !status) return;

  var target = document.getElementById(button.getAttribute('data-copy-target'));
  if (!target) return;

  if (!navigator.clipboard || typeof navigator.clipboard.writeText !== 'function' || !window.isSecureContext) {
    return; // Leave the button hidden; the code block stays manually selectable.
  }

  button.hidden = false;

  function selectTarget() {
    var range = document.createRange();
    range.selectNodeContents(target);
    var selection = window.getSelection();
    if (!selection) return;
    selection.removeAllRanges();
    selection.addRange(range);
  }

  button.addEventListener('click', function () {
    navigator.clipboard.writeText(target.textContent).then(function () {
      status.textContent = '已复制 BibTeX 到剪贴板。';
    }, function () {
      selectTarget();
      status.textContent = '自动复制失败，已为你选中文本，请按 Ctrl / Cmd + C 复制。';
    });
  });
})();
