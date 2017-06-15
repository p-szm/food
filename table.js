var response = {
  "valid": true,
  "items": [
  	{
  		"food_id": 1,
  		"name": "salad",
  		"calories": 65,
  		"quantity": 1.5,
  		"fiber": 565
  	},
  	{
  		"food_id": 2,
  		"name": "tomato",
  		"calories": 645,
  		"quantity": 1.1,
  		"fiber": 5
  	},
    {
  		"food_id": 3,
  		"name": "corn",
  		"calories": 6665,
  		"quantity": 0.9,
  		"fiber": 56
  	},
  	{
  		"food_id": 3,
  		"name": "bread",
  		"calories": 6665,
  		"quantity": 0.9,
  		"fiber": 56
  	}
  ]
};
function buildHtmlTable(selector) {
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
