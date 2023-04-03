function loadGraph() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/ngsiv2/');
    xhr.onload = function() {
        var elements = JSON.parse(xhr.responseText);
        var cy = cytoscape({
            container: document.getElementById('cy'),
            elements: elements,
            style: [
                {
                    selector: 'node',
                    style: {
                        'background-color': '#666',
                        'label': 'data(label)'
                    }
                },
                {
                    selector: 'edge',
                    style: {
                        'width': 3,
                        'line-color': '#ccc'
                    }
                }
            ],
            layout: {
                name: 'preset'
            }
        });
    };
    xhr.send();
}
