(function() {
  const appTextArea = document.getElementById('src-code-textarea');
  const editor = CodeMirror.fromTextArea(appTextArea, {
    lineNumbers: true,
    styleActiveLine: true,
    matchBrackets: true,
    mode: 'formlang',
  });
  window.editor = editor;
})();
