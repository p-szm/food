function server(data) {
    $.ajax({
    dataType: "json",
    url: 'http://localhost:5000/api',
    data: {data: data},
    success: success
});
}

function success(data) {console.log(data)};