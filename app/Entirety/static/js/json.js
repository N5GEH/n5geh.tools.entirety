function prettyJSON(element_id) {
    var ugly = document.getElementById(element_id).value;
    var obj = JSON.parse(ugly);
    var pretty = JSON.stringify(obj, undefined, 4);
    document.getElementById(element_id).value = pretty;
}
