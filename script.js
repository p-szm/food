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
    	url: "http://128.141.118.31:5000/api/optimiser",
    	data: {data: $('select').val().join(), 
    			calories_min: parseInt($('input#min_calories').val()), 
    			calories_max: parseInt($('input#max_calories').val())},
    	success: success
	});
}

function success(data) {
	console.log(data);

	// Clear the results container
	$('div#result-container').html('');

	if (data.status == 0) {
		$('div#result-container').html('Here is the list of the product and optimal quantities:');
		buildHtmlTable(data, 'div#result-container');
	}
	else if (data.status == 1) {
		$('div#result-container').html('Max number of iterations reached');
	}
	else if (data.status == 2) {
		$('div#result-container').html('The problem is too constrained');
	}
	else if (data.status == 3) {
		$('div#result-container').html('Unbounded problem');
	}
	else if (data.status == 4) {
		$('div#result-container').html('Missing nutrients:');
		var missing = data['missing nutrients'];
		var list = '<ul class="myList"><li class="ui-menu-item" role="menuitem"><a class="ui-all" tabindex="-1">' + missing.join('</a></li><li>') + '</li></ul>';
		$('div#result-container').append(list);
	}
};

$('select').select2({
    placeholder: "Select products",
    allowClear: true,
    ajax: {
        type: "GET",
        url: "http://128.141.118.31:5000/api/search",
        dataType: 'json',
        delay: 250,
        data: function (params) {
          return {
            q: params.term, // search term
            page: params.page
          };
        },
        processResults: function (data, params) {
          // parse the results into the format expected by Select2
          // since we are using custom formatting functions we do not need to
          // alter the remote JSON data, except to indicate that infinite
          // scrolling can be used
          params.page = params.page || 1;

          return {
            results: data.items,
            pagination: {
              more: (params.page * 30) < data.total_count
            }
          };
        },
        cache: true
      },
    escapeMarkup: function (markup) { return markup; },
    minimumInputLength: 1,
    templateResult: function(repo) {return repo.name;},
    templateSelection: function(repo) {
      if (repo.name.length > 20) {
        return repo.name.substring(0,20) + '...';
      }
      return repo.name;
    }
  });