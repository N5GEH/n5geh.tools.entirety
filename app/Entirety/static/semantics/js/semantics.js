//generates cytoscape elements in main Graph right at the beginning
const clickedNodeColor = "blue";
const parantsNodeColor = "yellow";
const childrensNodeColor = "orange";
const edgesNodeColor = "red";
const defaultnodecolor = 'gray'; // pick the default node color
const defaultedgecolor = '#ccc'; // pick the default edge color
const searchcolor = 'red'; // pick the default color for search highlights
var previousInput = "" //safe previous input in search field
var currentlyClickedNode = "" //currently clicked Node
var currentNodeType = ""
console.log(data)

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
                label: 'data(label)', // default label: name of entity
                'background-color': defaultnodecolor,
            }
        },
        {
            selector: 'edge',
            style: {
                'line-color': defaultedgecolor,
                'target-arrow-color': defaultedgecolor,
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
var entIndex; // index of node in the order posted on orion
nodeArray = [];
nodeArray = cy.nodes().map(x => x.id());

function handleClick(event) {
    var div = document.getElementById('entity');
    var h3 = div.querySelector('h3');
    currentlyClickedNode = event.target.id()
    currentNodeType = event.target.classes()[0]
    create_detail_level(event.target.id(), event.target);
    getEntity(event.target.id());
    entIndex = Array.from(nodeArray).indexOf(event.target.id());
    //shows entity table and adds node id to headder
    h3.textContent = 'Node ID: ' + event.target.id();
    div.style.display = 'block';
    clickedNodeStyling(event.target)

}

function clickedNodeStyling(clickedNode) {
    var clickedNodeSelector = "";
    var childSelector = [];
    var childEdgeSelector = [];
    var parentsEdge = [];
    var parentsSelector = [];
    var childrenEdge = [];

    if (typeof clickedNode.data('children') === 'object' && clickedNode.data('children') !== null && Array.isArray(clickedNode.data('children'))) {

        clickedNode.data('children').forEach(function (element) {
            // element: current element in the array of children id´s
            childSelector.push("#" + escapeColons(element))

            var escapedEdgeId = escapeColons(clickedNode.data('id') + element);
            //var edgeSelector = `edge[source="${escapeColons(clickedNode.data('id'))}"][target="${escapeColons(element)}"]`;
            //childEdgeSelector.push(edgeSelector);
            childEdgeSelector.push("#" + escapeColons(clickedNode.data('id') + element));
        });
    }
    //check if clickedNode has parents
    if (typeof clickedNode.data('parents') === 'object' && clickedNode.data('parents') !== null && Array.isArray(clickedNode.data('parents'))) {

        clickedNode.data('parents').forEach(function (element) {
            // element: current element in the array of children id´s
            parentsEdge.push(get_nodes_by_id(element + currentlyClickedNode));//appends edge between parents and center
            parentsSelector.push(get_nodes_by_id(element)); //appends parent nodes to the detail level
        });
    }
    if (childEdgeSelector.length === 0) {
        console.log("Die Liste ist leer.");
    } else {
        console.log("Die Liste ist nicht leer.");
    }

    console.log("childedgeSelector1: " + childrenEdge)
    //console.log(cy.$("#" + escapeColons(currentlyClickedNode)))
    console.log("childEdge:" + childEdgeSelector)
    //console.log("childSelector" + childSelector)
    //console.log("parentsEdge" + parentsEdge)
    //console.log("parentsSelector" + parentsSelector)
    childSelector.forEach(function (selector) {
        console.log("child "+ selector)
        cy.style()
            .selector(selector)
            .style("background-color", childrensNodeColor)
            .style("color", childrensNodeColor)
            .update();
    });
    childEdgeSelector.forEach(function (selector) {
        console.log("selector 4: "+ selector)
        cy.style()
            .selector(cy.$(selector))
            .style("line-color", edgesNodeColor)
            .update();
    });
    cy.style()
            .selector("#"+ escapeColons(currentlyClickedNode))
            .style("background-color", clickedNodeColor)
            .style("color", clickedNodeColor)
            .update();
    cy.style()
            .selector(cy.$("#urn\\:ngsi-ld\\:Product\\:001urn\\:ngsi-ld\\:Shelf\\:unit001"))
            .style("line-color", edgesNodeColor)
            .update();

}


/**
 * creates all detail elements in such manner: (parents->center->children) takes
 * the clickedNode_id as center and then looks for parents and children as well
 * as the corresponding edges
 * @param clickedNode_id
 * @param clickedNode
 */
function create_detail_level(clickedNode_id, clickedNode) {
    var detailElements = [];
    // Remove all existing nodes in the detail level
    detail.remove(detail.nodes());
    detailElements.push(get_nodes_by_id(clickedNode_id));

    //check if clickedNode has children
    if (typeof clickedNode.data('children') === 'object' && clickedNode.data('children') !== null && Array.isArray(clickedNode.data('children'))) {

        clickedNode.data('children').forEach(function (element) {
            // element: current element in the array of children id´s
            detailElements.push(get_nodes_by_id(clickedNode_id + element));//appends edge between center and children
            detailElements.push(get_nodes_by_id(element)); //appends children nodes to the detail level
        });
    }
    //check if clickedNode has parents
    if (typeof clickedNode.data('parents') === 'object' && clickedNode.data('parents') !== null && Array.isArray(clickedNode.data('parents'))) {

        clickedNode.data('parents').forEach(function (element) {
            // element: current element in the array of children id´s
            detailElements.push(get_nodes_by_id(element + clickedNode_id));//appends edge between parents and center
            detailElements.push(get_nodes_by_id(element)); //appends parent nodes to the detail level
        });
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
        {title: "Name", field: "Name", formatter: "textarea"},
        {title: "Value", field: "Value", formatter: "textarea"},
        {title: "Type", field: "Type", formatter: "textarea"},
        {title: "Metadata", field: "Metadata", formatter: "textarea"}
    ];

    // Create Tabulator table
    var table = new Tabulator("#table", {

        layout: "fitDataFill",
        columns: columns,
        height: "300px",
        verticalFillMode: "fill"
    });

    // Set data after table is built
    table.on("tableBuilt", function () {
        table.setData(entity);
    });
}

// Pick node and edge colors to be displayed first
const colors = ['#57C5B6', '#feb236', '#0dcaf0', '#D14D72', '#107cad', '#6CDB42', '#ff7b25', '#bea0d7', '#B70404', '#F9F54B', '#9A1663', '#9F8772', '#FF8787']
const tcheckboxes = document.querySelectorAll('input[name="typecheckbox"]');
const rcheckboxes = document.querySelectorAll('input[name="relcheckbox"]');
const numAdditionalColors = tcheckboxes.length;

// Generates as many additional random colors as there are entities in orion
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
    colors.push(randomColor);
}


function add_type_legend() {
    // If the checkbox is checked, create a new dropdown item and add it to the new dropdown menu
    if (this.checked && this.name == 'typecheckbox') {
        const label = this.closest('.dropdown-item').querySelector('.form-check-label').textContent;
        const newItem = document.createElement('li');
        const nodeindex = Array.from(this.closest('.dropdown-menu').querySelectorAll('.form-check-input')).indexOf(this);
        const nodecolor = colors[nodeindex];
        newItem.innerHTML = '<a class="dropdown-item" href="#">' + '<i class="bi bi-circle-fill" style="color: ' + nodecolor + '"></i>' + label + '</a>';
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
    if (this.checked && this.name == 'relcheckbox') {
        const label = this.closest('.dropdown-item').querySelector('.form-check-label').textContent;
        const newItem = document.createElement('li');
        const relindex = Array.from(this.closest('.dropdown-menu').querySelectorAll('.form-check-input')).indexOf(this);
        const relcolor = colors[relindex];
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

// Handle search button click
function handleSearch(event) {
    event.preventDefault();

    var searchField = document.querySelector('.form-control');
    var input = searchField.value;
    var selectedValue = null;
    var activeDropdownItem = document.querySelector('.dropdown-menu.dropdown-menu-right .dropdown-item.active');
    if (activeDropdownItem) {
        selectedValue = activeDropdownItem.getAttribute('data-value');
    }

    // Call the corresponding function based on the selected value
    if (selectedValue === null) {
        addWarning('Please select a search Option!')
    } else if (selectedValue === 'id1') {
        handleIdSearch(input);
    } else if (selectedValue === 'type1') {
        handleTypeSearch(input);
    } else if (selectedValue === 'relationship1') {
        handleRelationshipSearch(input);
    }
}

// Function to escape ':' in the id of a node
function escapeColons(str) {
    if (typeof str === 'undefined') {
        console.log("übergebener Wert ist nicht definiert funktion escapeColons")
        return str; // Wenn der Wert undefined ist, wird er unverändert zurückgegeben
    }
    return str.replace(/:/g, '\\:');
}

function clearSearchHighlight(input) {
    var element = escapeColons(input)
    var idSelector = cy.$("#" + element)
    var relSelector = `edge[label = "${input}"]`
    cy.style()
        .selector(idSelector + ", ." + input + "," + relSelector)
        .style('background-color', defaultnodecolor)
        .style('line-color', defaultedgecolor)
        .update();
    previousInput = '';
}

function checkInputEmpty() {
    var searchField = document.querySelector('.form-control');
    var input = searchField.value;
    if (input.trim() === '') {
        clearSearchHighlight(previousInput)
    }
}

// Function for handling ID option
function handleIdSearch(inputValue) {

    var node = get_nodes_by_id(inputValue)
    if (node) {
        var element = escapeColons(inputValue)
        if (inputValue !== previousInput) {
            clearSearchHighlight(previousInput)
        }
        cy.style() // changes node style by filterung for selectors
            .selector(cy.$('#' + element))
            .style('background-color', searchcolor)
            .update();
        previousInput = inputValue
    } else {
        addWarning("No matching Entity ID found")

    }
}

// Function for handling Type option
function handleTypeSearch(inputValue) {
    //var lowerCaseTypes = types.map(function (item) {
    //    return item.toLowerCase();
    //});
    if (types.includes(inputValue)) {
        const typeSelector = `.${inputValue}`;
        if (inputValue !== previousInput) {
            clearSearchHighlight(previousInput)
        }
        cy.style() // changes node style by filterung for selectors
            .selector(typeSelector)
            .style('background-color', searchcolor)
            .update();
        previousInput = inputValue

    } else {
        addWarning('No matching Type found')
    }
}

// Function for handling Relationship option
function handleRelationshipSearch(inputValue) {
    //var lowerCaseRels = relationships.map(function (item) {
    //    return item.toLowerCase();
    //});
    if (relationships.includes(inputValue)) {
        const relSelector = `edge[label = "${inputValue}"]`;
        if (inputValue !== previousInput) {
            clearSearchHighlight(previousInput)
        }
        cy.style() // changes node style by filterung for selectors
            .selector(relSelector)
            .style('line-color', searchcolor)
            .update();
        previousInput = inputValue

    } else {
        addWarning('No matching Relationship found')
    }
}

function addWarning(warningText) {
    var alertHtml = '<div class="alert alert-danger d-none" role="alert" id="searchAlert">' +
        '<div>' +
        '</div>' +
        '</div>';
    var warningWrapper = document.getElementById('warning_Wrapper');
    warningWrapper.innerHTML = ''; // Clear previous content
    warningWrapper.insertAdjacentHTML('beforeend', alertHtml); // Add the alert HTML

    var searchAlert = document.getElementById("searchAlert");
    searchAlert.classList.remove("d-none");
    searchAlert.textContent = warningText;

    setTimeout(function () {
        searchAlert.classList.add("d-none");
    }, 4000);

}

// Colors corresponding node if checkbox is checked
function colorNodes() {
    const nodecheckboxes = document.querySelectorAll('input[name="typecheckbox"]:checked');
    const originalColors = [];

    for (const checkbox of nodecheckboxes) {
        const id = `.${checkbox.id}`;
        const nodeindex = Array.from(tcheckboxes).indexOf(checkbox);
        const color = colors[nodeindex];
        cy.style() // changes node style by filterung for selectors
            .selector(id)
            .style('background-color', color)
            .update();
        detail.style()
            .selector(id)
            .style('background-color', color)
            .update();
        originalColors.push({id, color});
    }
    // set nodes back to gray by unchecking the checkbox
    const checkboxes = document.querySelectorAll('input[name="typecheckbox"]');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            const id = `.${checkbox.id}`;
            const originalColorIndex = originalColors.findIndex(item => item.id === id);
            if (originalColorIndex !== -1) {
                const originalColor = originalColors[originalColorIndex];
                cy.style()
                    .selector(id)
                    .style('background-color', checkbox.checked ? originalColor.color : defaultnodecolor)
                    .update();
                detail.style()
                    .selector(id)
                    .style('background-color', checkbox.checked ? originalColor.color : defaultnodecolor)
                    .update();

                if (!checkbox.checked) {
                    originalColors.splice(originalColorIndex, 1);
                }
            }
        });
    });
}

// Colors corresponding edge if checkbox is checked
function colorEdges() {
    const edgecheckboxes = document.querySelectorAll('input[name="relcheckbox"]:checked');
    const originalColors = [];

    for (const checkbox of edgecheckboxes) {
        const label = `edge[label = "${checkbox.id}"]`;
        const edgeindex = Array.from(rcheckboxes).indexOf(checkbox);
        const color = colors[edgeindex];
        cy.style() // changes edge style by filterung for selectors
            .selector(label)
            .style('line-color', color)
            .update();
        detail.style()
            .selector(label)
            .style('line-color', color)
            .update();
        originalColors.push({label, color});
    }
    // set edges back to gray by unchecking the checkbox
    const checkboxes = document.querySelectorAll('input[name="relcheckbox"]');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            const label = `edge[label = "${checkbox.id}"]`;
            const originalColorIndex = originalColors.findIndex(item => item.label === label);
            if (originalColorIndex !== -1) {
                const originalColor = originalColors[originalColorIndex];
                cy.style()
                    .selector(label)
                    .style('line-color', checkbox.checked ? originalColor.color : defaultedgecolor)
                    .update();
                detail.style()
                    .selector(label)
                    .style('line-color', checkbox.checked ? originalColor.color : defaultedgecolor)
                    .update();

                if (!checkbox.checked) {
                    originalColors.splice(originalColorIndex, 1);
                }
            }
        });
    });
}

// Adapts node labels as selected, otherwise default value name is set
function changeLabel(labelName) {
    var label;
    switch (labelName) {
        case "id":
            cy.style().selector('node').style({label: 'data(id)'}).update();
            break;
        case "name":
            cy.style().selector('node').style({label: 'data(label)'}).update();
            break;
        case "none":
            cy.style().selector('node').style({label: ""}).update();
            break;
    }
}


// Colors edges temporary when nodes are grabbed
cy.$('node').on('grab', function (e) {
    var ele = e.target;
    ele.connectedEdges().style({'line-color': 'dimgray'});
});
cy.$('node').on('free', function (e) {
    var ele = e.target;
    ele.connectedEdges().style({'line-color': defaultedgecolor});
});

// Adapts layout as selected
function changeLayout(layoutName) {
    var layout;
    switch (layoutName) {
        case "circle":
            layout = {name: "circle"};
            break;
        case "grid":
            layout = {name: "grid"};
            break;
        default:
            layout = {
                name: "breadthfirst",
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
                }
            }; // transform a given node position. Useful for changing flow direction in discrete layouts
    }
    cy.layout(layout).run();
}

// By clicking the icon: creates next Entity in table and detail view according to the order of posted entities in orion
function nextEntity() {
    if (entIndex < nodeArray.length - 2) {
        ++entIndex;
    } else {
        entIndex = 0;
    }
    var newEntity = nodeArray[entIndex];
    let newTarget = null;
    cy.nodes().forEach(node => {
        if (node.id() == newEntity) {
            newTarget = node;
            return false;
        }
    });
    getEntity(newEntity);
    create_detail_level(newEntity, newTarget);
}

function editEntity() {
    entitiesUrl = currentUrl.split('/semantics/')[0]
    var newUrl = entitiesUrl + "/entities/" + currentlyClickedNode + "/" + currentNodeType + "/update/";
    //window.open(newUrl, 'Popup-Fenster', 'width=800,height=600')
    window.location.href = newUrl;

}