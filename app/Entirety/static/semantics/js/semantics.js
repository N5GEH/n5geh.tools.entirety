//generates cytoscape elements in main Graph right at the beginning

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
                'curve-style': 'bezier',
                label: 'data(label)'
            }
        }
    ],
    maxZoom: 1.7,
    minZoom: 0.5,
    wheelSensitivity: 0.2,
    layout: {
        name: 'grid',
        rows: 3
    }
});
var detail = cytoscape({
    container: document.getElementById('detail_level'),
    elements: [],
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
                'curve-style': 'bezier',
                label: 'data(label)'
            }
        }
    ],
    maxZoom: 1.7,
    minZoom: 0.5,
    wheelSensitivity: 0.2,
    layout: {
        name: 'grid',
        rows: 3
    }
});


/**
 * handels actions when a node has been clicked in the main graph
 * @param event
 */
function handleClick(event) {
    //console.log('clicked Node id', event.target.id());
    var div = document.getElementById('entity');
    var h3 = div.querySelector('h3');
    // call function to create detail Level
    create_detail_level(event.target.id(), event.target);
    getEntity(event.target.id())
    //shows entity table and adds node id to headder
    h3.textContent = 'Node ID: ' + event.target.id();
    div.style.display = 'block';


}

/**
 * creates all detail elements in such manner: (parents->center->children) takes
 * the clickedNode_id as center and then looks for parents and children as well
 * as the corresponding edges
 * @param clickedNode_id
 * @param clickedNode
 */
function create_detail_level(clickedNode_id, clickedNode) {
    //console.log("create_detail_level() function is being called.")
    //detailElements.length = 0;
    var detailElements = [];

    detailElements.push(get_nodes_by_id(clickedNode_id));

    //check if clickedNode has children
    if (typeof clickedNode.data('children') === 'object' && clickedNode.data('children') !== null && Array.isArray(clickedNode.data('children'))) {

        clickedNode.data('children').forEach(function (element) {
            // element: current element in the array of children id´s
            detailElements.push(get_nodes_by_id(clickedNode_id + element));//appends edge between center and children
            detailElements.push(get_nodes_by_id(element)); //appends children nodes to the detail level

        });
    } else {
        //console.log("Array is not present or not defined");
    }
    //check if clickedNode has parents
    if (typeof clickedNode.data('parents') === 'object' && clickedNode.data('parents') !== null && Array.isArray(clickedNode.data('parents'))) {
        clickedNode.data('parents').forEach(function (element) {
            // element: current element in the array of children id´s
            detailElements.push(get_nodes_by_id(element + clickedNode_id));//appends edge between parents and center
            detailElements.push(get_nodes_by_id(element)); //appends parent nodes to the detail level
        });
    } else {
        //console.log("Array is not present or not defined");
    }
    detail.add(detailElements)


}

/**
 * Takes an id as input and searces for the node in all data wich maches the input id
 * @param nodeID
 * @returns {node}
 */
function get_nodes_by_id(nodeID) {

    for (var i = 0; i < data.length; i++) {

        if (data[i].data && data[i].data.id === nodeID) {
            foundObject = data[i]; // Store the found object
            break; // Exit the loop when the target object is found
        }
    }

    if (foundObject) {
        //console.log('Found object:', foundObject);
        return foundObject
    } else {
        //console.log('Object with ID', targetId, 'not found.');
    }
}

async function makeRequest(url, method, body) {

    let headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/json'
    }
    if (method === 'post') {
        console.log('post')
        headers['X-CSRFToken'] = document.querySelector('[name=csrfmiddlewaretoken]').value
        console.log(headers)
    }
    let response = await fetch(baseUrl + '/ngsiv2/', {
        method: method,
        headers: headers,
        body: body,

    })
        .then((response) => response.json())
    console.log('hello1')

    return await response
}

async function getEntity(nodeID) {
    console.log(nodeID)

    let data = await makeRequest(baseUrl + '/ngsiv2/', 'post', JSON.stringify({nodeID: nodeID}))
    let entity = document.getElementById('table')
    let li = document.createElement('li')
    li.innerText= await data['entity']
    entity.appendChild(li)
    console.log(data)
}



