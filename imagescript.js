var xhr = new XMLHttpRequest();
xhr.open("GET", "https://en.wikipedia.org/w/api.php?action=query&titles=Main%20Page&prop=revisions&rvprop=content&format=json", false)
xhr.send();
console.log(xhr.status);
console.log(xhr.statusText);
