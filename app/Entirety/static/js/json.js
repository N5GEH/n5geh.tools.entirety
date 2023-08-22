function prettyJSON() {
    var ugly = document.getElementById('id_json_field').value;
    var obj = JSON.parse(ugly);
    var pretty = JSON.stringify(obj, undefined, 4);
    document.getElementById('id_json_field').value = pretty;
}
