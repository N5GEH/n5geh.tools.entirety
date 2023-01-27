function prettyJSON() {
    var ugly = document.getElementById('id_entity_json').value;
    var obj = JSON.parse(ugly);
    var pretty = JSON.stringify(obj, undefined, 4);
    document.getElementById('id_entity_json').value = pretty;
}
