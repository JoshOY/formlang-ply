(function() {
  const appTextArea = document.getElementById('src-code-textarea');
  const editor = CodeMirror.fromTextArea(appTextArea, {
    lineNumbers: true,
  });
  window.editor = editor;
})();
