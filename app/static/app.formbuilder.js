$(document).ready(function() {
  $('#app-form-build-btn').on('click', function () {
    const form = new FormData();
    const rawCode = window.editor.getValue();
    console.log(form);
    form.append('rawCode', rawCode);
    $.ajax({
      url: '/api/form_generate',
      type: 'POST',
      datatype: 'json',
      contentType: false,
      cache: false,
      processData: false,
      data: form,
      success: function(data) {
        console.log(data);
      },
    });
  });
});
