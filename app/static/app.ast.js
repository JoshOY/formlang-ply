function newTreantDiagram(ASTData) {
  const chartConfig = {
    chart: {
      container: '#chart-container',
      levelSeparation: 35,
      rootOrientation: 'WEST',
      nodeAlign: 'BOTTOM',
      connectors: {
        type: 'step',
        style: {
          'stroke-width': 2,
        },
      },
      node: {
        HTMLclass: 'ast-node',
      },
    },

    nodeStructure: ASTData,
  };
  window.ASTDiagram = new Treant(chartConfig);
}

$(document).ready(function() {
  $('#app-parse-btn').on('click', function () {
    const form = new FormData();
    const rawCode = window.editor.getValue();
    console.log(form);
    form.append('rawCode', rawCode);
    $.ajax({
      url: '/api/ast_generate',
      type: 'POST',
      datatype: 'json',
      contentType: false,
      cache: false,
      processData: false,
      data: form,
      success: function(data) {
        console.log(data);
        newTreantDiagram(data.result);
      },
    });
  });
});
