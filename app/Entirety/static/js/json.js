function prettyJSON(elementId) {
    var ugly = document.getElementById(elementId).value;
    var obj = JSON.parse(ugly);
    var pretty = JSON.stringify(obj, undefined, 4);
    document.getElementById(elementId).value = pretty;
}
