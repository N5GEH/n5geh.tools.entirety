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
                label: "",
                'background-color': 'gray',
            }
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
        },
       /* {
            selector: 'edge[Attribute="refShelf"]',
            style: {
                'line-color': 'yellow',
            }
        },
        {
            selector: 'Attribute = refStore',
            style: {
                'line-color': 'blue',
            }
        }*/
        
    ],
    maxZoom: 2,
    minZoom: 0.5,
    wheelSensitivity: 0.2,
    layout: {
        name: 'breadthfirst',
        fit: true, // whether to fit the viewport to the graph
        directed: true, // whether the tree is directed downwards (or edges can point in any direction if false)
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

});


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
    //console.log(event.target)
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
    // Remove all existing nodes in the detail level
    detail.remove(detail.nodes());
    detailElements.push(get_nodes_by_id(clickedNode_id));

    //check if clickedNode has children
    if (typeof clickedNode.data('children') === 'object' && clickedNode.data('children') !== null && Array.isArray(clickedNode.data('children'))) {
        console.log(clickedNode.data('children'))
        clickedNode.data('children').forEach(function (element) {
            // element: current element in the array of children id´s
            detailElements.push(get_nodes_by_id(clickedNode_id + element));//appends edge between center and children
            detailElements.push(get_nodes_by_id(element)); //appends children nodes to the detail level
        });
    } else {
        console.log("no children");
    }
    //check if clickedNode has parents
    if (typeof clickedNode.data('parents') === 'object' && clickedNode.data('parents') !== null && Array.isArray(clickedNode.data('parents'))) {
        console.log('parents'+ clickedNode.data('parents'))
        clickedNode.data('parents').forEach(function (element) {
            // element: current element in the array of children id´s
            detailElements.push(get_nodes_by_id(element + clickedNode_id));//appends edge between parents and center
            detailElements.push(get_nodes_by_id(element)); //appends parent nodes to the detail level
        });
    } else {
        console.log("no parents");
    }
    detail.add(detailElements)
    detail.layout({
        name: 'breadthfirst',
        fit: true, // whether to fit the viewport to the graph
        directed: true, // whether the tree is directed downwards (or edges can point in any direction if false)
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
    }).run();
}

/**
 * Takes an id as input and searces for the node in all data wich matches the input id
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
        headers['X-CSRFToken'] = document.querySelector('[name=csrfmiddlewaretoken]').value
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

    let data = await makeRequest(baseUrl + '/ngsiv2/', 'post', JSON.stringify({nodeID: nodeID}))
    var entity = await data['entity']
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

// Pick random node colors to start with
const nodecolors = ['#feb236', '#57C5B6', '#146C94', '#D14D72', '#ff7b25', '#0ad3ff', '#6CDB42']
const tcheckboxes = document.querySelectorAll('input[name="typecheckbox"]');
const numAdditionalColors = tcheckboxes.length;
// Generates additional colors
function generateRandomColor() {
  const letters = '0123456789ABCDEF';
  let color = '#';
  for (let i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}
for (let i = 0; i < numAdditionalColors; i++) {
  const randomColor = generateRandomColor();
  nodecolors.push(randomColor);
}


function add_type_legend() {
    // If the checkbox is checked, create a new dropdown item and add it to the new dropdown menu
    if (this.checked && this.name == 'typecheckbox') {
        const label = this.closest('.dropdown-item').querySelector('.form-check-label').textContent;
        const newItem = document.createElement('li');
        const nodeindex = Array.from(this.closest('.dropdown-menu').querySelectorAll('.form-check-input')).indexOf(this);
        const nodecolor = nodecolors[nodeindex];
        newItem.innerHTML = '<a class="dropdown-item" href="#">' + '<i class="bi bi-check-circle-fill" style="color: ' + nodecolor + '"></i>' + label + '</a>';
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

// Pick random edge colors to start with
const relcolors = ['#f44336', '#faff00', '#c90076', '#2986cc', '#1ad70f', '#f89c05'];

function add_rel_legend() {
    // If the checkbox is checked, create a new dropdown item and add it to the new dropdown menu
    if (this.checked && this.name == 'relcheckbox') {
        const label = this.closest('.dropdown-item').querySelector('.form-check-label').textContent;
        const newItem = document.createElement('li');
        const relindex = Array.from(this.closest('.dropdown-menu').querySelectorAll('.form-check-input')).indexOf(this);
        const relcolor = relcolors[relindex];
        newItem.innerHTML = '<a class="dropdown-item" href="#">' + '<i class="bi bi-dash-lg" style="color: ' + relcolor + '"></i>' + label + '</a>';
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


// Colors corresponding node if checkbox is checked
function colorNodes() {
    const nodecheckboxes = document.querySelectorAll('input[name="typecheckbox"]:checked');
    const originalColors = [];
  
    for (const checkbox of nodecheckboxes) {
      const id = `.${checkbox.id}`;
      const nodeindex = Array.from(tcheckboxes).indexOf(checkbox);
      const color = nodecolors[nodeindex];
      cy.style()
        .selector(id)
        .style('background-color', color)
        .update();
      originalColors.push({ id, color });
    }
  
    const checkboxes = document.querySelectorAll('input[name="typecheckbox"]');
    checkboxes.forEach(checkbox => {
      checkbox.addEventListener('change', () => {
        const id = `.${checkbox.id}`;
        const originalColorIndex = originalColors.findIndex(item => item.id === id);
        if (originalColorIndex !== -1) {
          const originalColor = originalColors[originalColorIndex];
          cy.style()
            .selector(id)
            .style('background-color', checkbox.checked ? originalColor.color : 'gray')
            .update();
  
          if (!checkbox.checked) {
            originalColors.splice(originalColorIndex, 1);
          }
        }
      });
    });
}

// Adds selected labels
function changelabelid () {
    cy.style().selector('node').style({ label: 'data(id)' }).update();
}
function changelabelname () {
    cy.style().selector('node').style({ label: 'data(label)' }).update();
}
function changelabelnone () {
    cy.style().selector('node').style({ label: "" }).update();
}

// Colors edges temporary when nodes are grabbed
cy.$('node').on('grab', function (e) {
    var ele = e.target;
    ele.connectedEdges().style({ 'line-color': 'dimgray' });
});
cy.$('node').on('free', function (e) {
    var ele = e.target;
    ele.connectedEdges().style({ 'line-color': '#ccc' });
});