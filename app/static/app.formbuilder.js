window.FORM_LEN_LAST = 0;

function getParsedString(str) {
  if (str[0] === '\"') {
    return {
      category: 'raw',
      value: '<span>' + str.slice(1, -1) + '</span>',
      trimmed: str.slice(1, -1),
    };
  } else if (str[0] === '`') {
    const v = window.markdown.toHTML(str.slice(3, -3).trim());
    console.log('v =', v);
    return {
      category: 'markdown',
      value: v,
      trimmed: str.slice(3, -3),
    };
  } else {
    return {
      category: 'normal',
      value: str,
      trimmed: str,
    };
  }
}

function createFormElement(question, idx) {
  const formContainer = $('#form-container');
  // console.log('formContainer =', formContainer);
  const textAreaHeight = question.lineNumber ? (question.lineNumber * 24) + 'px' : '48px';
  const description = question.description ? getParsedString(question.description).value : '';
  const name = question.name ? getParsedString(question.description).trimmed : '';
  const options = question.options;
  if (options) {
    console.info(options);
  }
  let isRequiredDOM = '';
  if (question.isRequired) {
    isRequiredDOM = '<span class="qr">*</span>';
  }
  switch (question.type) {
    case 'Text':
      formContainer.append('<section class="q">' + isRequiredDOM +
        '<h2 class="qn">' + (idx + 1).toString() + '. </h2>' +
        '<span class="q-title">' + getParsedString(question.title).value + '</span>' +
        (description ? `<div class="q-desc">${description}</div>` : '') +
        '</section>');
      return null;
    case 'ShortInput':
      formContainer.append('<section class="q">' + isRequiredDOM +
        '<h2 class="qn">' + (idx + 1).toString() + '. </h2>' +
        '<span class="q-title">' + getParsedString(question.title).value + '</span>' +
        (description ? `<div class="q-desc">${description}</div>` : '') +
        '<div class="input-group" style="margin-top: 16px"> <input class="form-control" style="width: 85%"> </div>' +
        '</section>');
      return null;
    case 'LongInput':
      formContainer.append('<section class="q">' + isRequiredDOM +
        '<h2 class="qn">' + (idx + 1).toString() + '. </h2>' +
        '<span class="q-title">' + getParsedString(question.title).value + '</span>' +
        (description ? `<div class="q-desc">${description}</div>` : '') +
        '<div class="input-group" style="margin-top: 16px">' +
        `<textarea name="${name}" class="form-control" style="width: 85%; height: ${textAreaHeight}"></textarea> ` +
        '</div>' +
        '</section>');
      return null;
    case 'SingleChoice':
      formContainer.append('<section class="q">' + isRequiredDOM +
        '<h2 class="qn">' + (idx + 1).toString() + '. </h2>' +
        '<span class="q-title">' + getParsedString(question.title).value + '</span>' +
        (description ? `<div class="q-desc">${description}</div>` : '') +
        '<div class="input-group" style="margin-top: 16px">' +
        '<form>' +
        (options ? _.map(options, function(o, idx2) {
          return `<input type="radio" name="${name || 'f-${idx}-${idx2}'}" id="f-${idx}-${idx2}"><label for="f-${idx}-${idx2}">${getParsedString(o).trimmed}</label><br>`;
        }).join('') : '') +
        '</form>' +
        '</div>' +
        '</section>');
      return null;
    case 'MultipleChoice':
      formContainer.append('<section class="q">' + isRequiredDOM +
        '<h2 class="qn">' + (idx + 1).toString() + '. </h2>' +
        '<span class="q-title">' + getParsedString(question.title).value + '</span>' +
        (description ? `<div class="q-desc">${description}</div>` : '') +
        '<div class="input-group" style="margin-top: 16px">' +
        '<form>' +
        (options ? _.map(options, function(o, idx2) {
          return `<input type="checkbox" name="${name || 'f-${idx}-${idx2}'}" id="f-${idx}-${idx2}"><label for="f-${idx}-${idx2}">${getParsedString(o).trimmed}</label><br>`;
        }).join('') : '') +
        '</form>' +
        '</div>' +
        '</section>');
      return null;
    default:
      return null;
  }
}

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
        const formArr = data.form.slice(window.FORM_LEN_LAST);
        console.log('formArr = ', formArr);
        window.FORM_LEN_LAST += formArr.length;
        $('#form-container').empty();
        formArr.forEach(function(question, idx) {
          createFormElement(question, idx);
        });
      },
      // END
    });
  });
});
