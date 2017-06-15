function buildHtmlTable(response, selector) {

  $(selector).append($('<table/>'));
  selector = selector + ' table';
  $(selector).addClass('centre');

  var columns = addAllColumnHeaders(response, selector);

  for (var i = 0; i < response.items.length; i++) {
    var row$ = $('<tr/>');
    for (var colIndex = 0; colIndex < columns.length; colIndex++) {
      var cellValue = response.items[i][columns[colIndex]];
      if (cellValue == null) cellValue = "";
      row$.append($('<td/>').html(cellValue));
    }
    $(selector).append(row$);
  }
}

function addAllColumnHeaders(response, selector) {
  var columnSet = [];
  var headerTr$ = $('<tr/>');

  for (var i = 0; i < response.items.length; i++) {
    var rowHash = response.items[i];
    for (var key in rowHash) {
      if ($.inArray(key, columnSet) == -1) {
        columnSet.push(key);
        headerTr$.append($('<th/>').html(key));
      }
    }
  }
  $(selector).append(headerTr$);

  return columnSet;
}

function server(data) {
    $.ajax({
    	dataType: "json",
    	url: "http://localhost:5000/api/optimiser",
    	data: {data: $('select').val().join()},
    	success: success
	});
}

function success(data) {
	console.log(data);

	// Clear the results container
	$('div#result-container').html('');

	if (data.valid) {
		buildHtmlTable(data, 'div#result-container');
	}
	else {
		
	}
};