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
    maxZoom: 2,
    minZoom: 0.5,
    wheelSensitivity: 0.2,
    layout: {
        name: 'breadthfirst',
        fit: true, // whether to fit the viewport to the graph
        directed: false, // whether the tree is directed downwards (or edges can point in any direction if false)
        padding: 30, // padding on fit
        circle: false, // put depths in concentric circles if true, put depths top down if false
        grid: false, // whether to create an even grid into which the DAG is placed (circle:false only)
        spacingFactor: 1.75, // positive spacing factor, larger => more space between nodes (N.B. n/a if causes overlap)
        boundingBox: undefined, // constrain layout bounds; { x1, y1, x2, y2 } or { x1, y1, w, h }
        avoidOverlap: true, // prevents node overlap, may overflow boundingBox if not enough space
        nodeDimensionsIncludeLabels: false, // Excludes the label when calculating node bounding boxes for the layout algorithm
        roots: undefined, // the roots of the trees
        depthSort: undefined, // a sorting function to order nodes at equal depth. e.g. function(a, b){ return a.data('weight') - b.data('weight') }
        animate: false, // whether to transition the node positions
        animationDuration: 500, // duration of animation in ms if enabled
        animationEasing: undefined, // easing of animation if enabled,
        animateFilter: function (node, i) {
            return true;
        }, // a function that determines whether the node should be animated.  All nodes animated by default on animate enabled.  Non-animated nodes are positioned immediately when the layout starts
        ready: undefined, // callback on layoutready
        stop: undefined, // callback on layoutstop
        transform: function (node, position) {
            return position;
        } // transform a given node position. Useful for changing flow direction in discrete layouts

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
        name: 'breadthfirst',
        fit: true, // whether to fit the viewport to the graph
        directed: false, // whether the tree is directed downwards (or edges can point in any direction if false)
        padding: 30, // padding on fit
        circle: false, // put depths in concentric circles if true, put depths top down if false
        grid: false, // whether to create an even grid into which the DAG is placed (circle:false only)
        spacingFactor: 1.75, // positive spacing factor, larger => more space between nodes (N.B. n/a if causes overlap)
        boundingBox: undefined, // constrain layout bounds; { x1, y1, x2, y2 } or { x1, y1, w, h }
        avoidOverlap: true, // prevents node overlap, may overflow boundingBox if not enough space
        nodeDimensionsIncludeLabels: false, // Excludes the label when calculating node bounding boxes for the layout algorithm
        roots: undefined, // the roots of the trees
        depthSort: undefined, // a sorting function to order nodes at equal depth. e.g. function(a, b){ return a.data('weight') - b.data('weight') }
        animate: false, // whether to transition the node positions
        animationDuration: 500, // duration of animation in ms if enabled
        animationEasing: undefined, // easing of animation if enabled,
        animateFilter: function (node, i) {
            return true;
        }, // a function that determines whether the node should be animated.  All nodes animated by default on animate enabled.  Non-animated nodes are positioned immediately when the layout starts
        ready: undefined, // callback on layoutready
        stop: undefined, // callback on layoutstop
        transform: function (node, position) {
            return position;
        } // transform a given node position. Useful for changing flow direction in discrete layouts

    }


})


/**
 * handels actions when a node has been clicked in the main graph
 * @param event
 */
function handleClick(event) {
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
    var foundObject = null;

    for (var i = 0; i < data.length; i++) {
        if (data[i].data && data[i].data.id === nodeID) {
            foundObject = data[i];
            break;
        }
    }

    if (foundObject) {
        return foundObject;
    } else {
        return null;
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

    return await response
}

async function getEntity(nodeID) {
    console.log('hello')
    let data = await makeRequest(baseUrl + '/ngsiv2/', 'post', JSON.stringify({nodeID: nodeID}))
    var entity = await data['entity']
    console.log(entity)
    // Define columns

    var columns = [
        {title: "Name", field: "Name"},
        {title: "Value", field: "Value"},
        {title: "Type", field: "Type"},
        {title: "Metadata", field: "Metadata"}
    ];

    // Create Tabulator table
    var table = new Tabulator("#table", {

        layout: "fitColumns",
        columns: columns,
        height: "300px",
        verticalFillMode: "fill",
    });

    // Set data after table is built
    table.on("tableBuilt", function () {
        table.setData(entity);

    });
}

function add_type_legend() {
    // If the checkbox is checked, create a new dropdown item and add it to the new dropdown menu
    if (this.checked) {
        const label = this.closest('.dropdown-item').querySelector('.form-check-label').textContent;
        const newItem = document.createElement('li');
        newItem.innerHTML = '<a class="dropdown-item" href="#">' + '<i class="bi bi-dash-lg" style="color: red"></i>' + label + '</a>';
        typelegend.appendChild(newItem);
    }
    // If the checkbox is unchecked, remove the corresponding dropdown item from the new dropdown menu
    else {
        const label = this.closest('.dropdown-item').querySelector('.form-check-label').textContent;
        const items = legend.querySelectorAll('.dropdown-item');
        items.forEach(function (item) {
            if (item.textContent === label) {
                typelegend.removeChild(item.parentElement);
            }
        })
    }
}

function add_rel_legend() {
    // If the checkbox is checked, create a new dropdown item and add it to the new dropdown menu
    if (this.checked) {
        const label = this.closest('.dropdown-item').querySelector('.form-check-label').textContent;
        const newItem = document.createElement('li');
        newItem.innerHTML = '<a class="dropdown-item" href="#">' + '<i class="bi bi-dash-lg" style="color:blue"></i>' + label + '</a>';
        rellegend.appendChild(newItem);
    }
    // If the checkbox is unchecked, remove the corresponding dropdown item from the new dropdown menu
    else {
        const label = this.closest('.dropdown-item').querySelector('.form-check-label').textContent;
        const items = legend.querySelectorAll('.dropdown-item');
        items.forEach(function (item) {
            if (item.textContent === label) {
                rellegend.removeChild(item.parentElement);
            }
        });
    }
}

function handleSearch(event) {
    event.preventDefault(); // prevent the form from submitting and refreshing the page
    var searchText = document.getElementById('searchform').value;
    var node = get_nodes_by_id(searchText)
    if (node) {
        console.log(node);
    } else {
        document.getElementById("searchAlert").classList.remove("d-none");
        setTimeout(function () {
            document.getElementById("searchAlert").classList.add("d-none");
        }, 3000);
    }
}


