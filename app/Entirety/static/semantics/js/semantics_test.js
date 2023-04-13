var cy = cytoscape({
    container: document.getElementById('main_graph'),
    elements: data,
    style: [
        {
            selector: 'node',
            style: {
                width: '20px',
                height: '20px',
                shape: 'ellipse',
                label: 'data(id)',
            },
        },
        {
            selector: 'edge',
            style: {
                'line-color': '#ccc',
                'target-arrow-color': '#ccc',
                'target-arrow-shape': 'triangle',
                'curve-style': 'bezier'
            }
        }
    ],
    layout: {
        name: 'grid',
        rows: 3
    }
});

cy.ready(function(event) {
    try {
        // Loop through all edges
        cy.edges().forEach(function(edge) {
            var targetId = edge.target().id();
            // Check if target node exists, if not, create a simple node with target as ID
            if (!cy.getElementById(targetId).length) {
                cy.add({
                    data: {
                        id: targetId
                    }
                });
            }
        });
    } catch (error) {
        console.error('An error occurred:', error);
    }
});


//show entity on node click
function handleClick(event) {
    console.log('clicked Node', event.target.id());
    var div = document.getElementById('entity');
    var h3 = div.querySelector('h3');
    var clickedNode = event.target;
    console.log(clickedNode);
    console.log('Children of node ' + children + ':');
    var children = clickedNode.data('children'); // Access the 'children' attribute from the node's data
    console.log(children);


    h3.textContent = 'Node ID: ' + event.target.id();
    div.style.display = 'block';
}
