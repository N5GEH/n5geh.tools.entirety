function prettyJSON(element_id) {
    var ugly = document.getElementById(element_id).value;
    var obj = JSON.parse(ugly);
    var pretty = JSON.stringify(obj, undefined, 4);
    document.getElementById(element_id).value = pretty;
}

function loadSchema(elementId, linkId) {
    var link = document.getElementById(linkId)
    var schema = document.getElementById(elementId)

    $.getJSON(link.value, function (data) {
        schema.value = JSON.stringify(data);
    }).fail(function () {
        alert("Error - could not get json data from service. Use, for example, a raw json github link.");
    });
    document.getElementById(element_id).value = pretty;
}
