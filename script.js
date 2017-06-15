function server(data) {
    $.ajax({
    dataType: "json",
    url: "http://128.141.118.216:5000/api/optimiser",
    data: {data: $('select').val().join()},
    success: success
});
}

function success(data) {console.log(data);};