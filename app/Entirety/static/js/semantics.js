//generates cytoscape elements in main Graph right at the beginning
const clickedNodeColor = "#2fa1ce";

const defaultnodecolor = '#6c757d'; // pick the default color for all nodes
const defaulttextcolor = '#343a40'; // pick the default color for the node label
const defaultedgecolor = '#6c757d'; // pick the default color for all edges
const searchcolor = 'red'; // pick the default color for search highlights

var previousInput = "" //safe previous input in search field
var currentlyClickedNode = "" //currently clicked Node
var previousClickedNode = "" // previous clicked Node
var currentNodeType = ""

// for highlighting nodes
const parantsNodeColor = "yellow";
const childrensNodeColor = "orange";
const edgesNodeColor = "red";

var currentStyleCy = {
    styleSheets: [
        {
            selector: 'node',
            style: {
                width: '20px',
                height: '20px',
                shape: 'ellipse',
                label: 'data(label)',
                backgroundColor: defaultnodecolor,
                color: defaulttextcolor
            }
        },
        {
            selector: 'edge',
            style: {
                lineColor: defaultedgecolor,
                color: defaulttextcolor,
                width: '1px',
                targetArrowColor: defaultedgecolor,
                targetArrowShape: 'vee',
                curveStyle: 'bezier',
                label: 'data(label)'
            }
        }
    ]
};
var currentStyleDetail = {
    styleSheets: [
        {
            selector: 'node',
            style: {
                width: '20px',
                height: '20px',
                shape: 'ellipse',
                label: 'data(label)',
                'color': defaulttextcolor,
            },
        },
        {
            selector: 'edge',
            style: {
                'width': '1px',
                'target-arrow-shape': 'vee',
                'curve-style': 'bezier',
                'color': defaulttextcolor,
                label: 'data(label)'
            }
        }
    ],

}

var cy = cytoscape({
    container: document.getElementById('main_graph'),
    elements: data,
    maxZoom: 2,
    minZoom: 0.5,
    wheelSensitivity: 0.2,
    userZoomingEnabled: false,
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
//this part enables zooming and shows an alert message to teach the user how to Zoom
var containerMainGraph = document.getElementById('main_graph');
var alertShownMainGraph = false;
containerMainGraph.addEventListener('wheel', function (event) {
    if (!cy.userZoomingEnabled() && !alertShownMainGraph) {
        document.getElementById("scrollAlert").classList.remove("d-none");
        setTimeout(function () {
            document.getElementById("scrollAlert").classList.add("d-none");
        }, 5000);
        alertShownMainGraph = true;
    }
});
document.addEventListener('keydown', function (event) {
    if (event.key === 'Control') {
        cy.userZoomingEnabled(true);
    }
});
document.addEventListener('keyup', function (event) {
    if (event.key === 'Control') {
        cy.userZoomingEnabled(false);
    }
});
cy.style(currentStyleCy.styleSheets).update();

var detail = cytoscape({
    container: document.getElementById('detail_level'),
    elements: [],
    maxZoom: 1.7,
    minZoom: 0.5,
    userZoomingEnabled: false,
    wheelSensitivity: 0.2,

});
//this part enables zooming and shows an alert message to teach the user how to Zoom
var containerDetail = document.getElementById('detail_level');
var alertShownDetail = false;
containerDetail.addEventListener('wheel', function (event) {
    if (!detail.userZoomingEnabled() && !alertShownDetail) {
        document.getElementById("scrollAlertDetail").classList.remove("d-none");
        setTimeout(function () {
            document.getElementById("scrollAlertDetail").classList.add("d-none");
        }, 5000);
        alertShownDetail = true;
    }
});
document.addEventListener('keydown', function (event) {
    if (event.key === 'Control') {
        detail.userZoomingEnabled(true);
    }
});
document.addEventListener('keyup', function (event) {
    if (event.key === 'Control') {
        detail.userZoomingEnabled(false);
    }
});
detail.style(currentStyleCy.styleSheets).update();

detail.style(currentStyleDetail.styleSheets).update();

function removeStyleBySelector(targetGraph, selector) {
    if (targetGraph === 'mainGraph') {
        var indexToRemoveCy = currentStyleCy.styleSheets.findIndex(function (styleObject) {
            return styleObject.selector === selector;
        });

        if (indexToRemoveCy !== -1) {
            currentStyleCy.styleSheets.splice(indexToRemoveCy, 1);
            cy.style(currentStyleCy.styleSheets).update();
        }
    }
    if (targetGraph === 'detail') {
        var IndexToRemoveDetail = currentStyleDetail.styleSheets.findIndex(function (styleObject) {
            return styleObject.selector === selector;
        });

        if (IndexToRemoveDetail !== -1) {
            currentStyleDetail.styleSheets.splice(IndexToRemoveDetail, 1);
            detail.style(currentStyleDetail.styleSheets).update();
        }
    }
}

/**
 * Clears the highlighting of search results in the graph and resets it to default value
 * @param input - The input or label to be cleared.
 */
function clearSearchHighlight(input) {
    var element = escapeColons(input)
    var idSelector = 'node#' + element
    var relSelector = `edge[label = "${input}"]`
    var nameSelector = `node[label = "${input}"]`
    removeStyleBySelector('mainGraph', idSelector)
    removeStyleBySelector('mainGraph', "." + input)
    removeStyleBySelector('mainGraph', relSelector)
    removeStyleBySelector('mainGraph', nameSelector)
    cy.style(currentStyleCy.styleSheets).update();
    previousInput = '';
    console.log('clear')
}

/**
 * handels actions when a node has been clicked in the main graph
 * @param event
 */
function handleClick(event) {
    previousClickedNode = currentlyClickedNode
    var div = document.getElementById('entity');
    var nodeIdText = document.getElementById('nodeIdText');
    currentlyClickedNode = event.target.id()
    currentNodeType = event.target.classes()[0]
    create_detail_level(event.target.id(), event.target);
    getEntity();

    nodeIdText.textContent = 'Additional information on Node ID: ' + event.target.id();
    div.style.display = 'block';
    window.scrollBy(0, 1);
    clickedNodeStyling()
}

/**
 * This function highlights the clicked nodes.
 * For future highliting of parents and childrens of clicked Node: the functionalities are already implemented but buggy
 * @param clickedNode
 */
function clickedNodeStyling(clickedNode) {
    //styles clicked Node
    removeStyleBySelector('mainGraph', "#" + escapeColons(previousClickedNode))
    removeStyleBySelector('detail', "#" + escapeColons(previousClickedNode))

    var newStyleMainGraphe = {
        "selector": "#" + escapeColons(currentlyClickedNode),
        style: {
            "background-color": clickedNodeColor
        }
    }
    currentStyleCy.styleSheets.push(newStyleMainGraphe);
    cy.style(currentStyleCy.styleSheets).update();

    var newStyleDetail = {
        "selector": "#" + escapeColons(currentlyClickedNode),
        style: {
            "background-color": clickedNodeColor
        }
    }
    currentStyleDetail.styleSheets.push(newStyleDetail);
    detail.style(currentStyleDetail.styleSheets).update();
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

/**
 *  Makes an asynchronous HTTP request with Fetch to the specified URL with the given method and body.

 * @param url (str): The URL to send the request to.
 * @param method (str): The HTTP method to use for the request (e.g., 'GET', 'POST', 'PUT', etc.).
 * @param body (str): The request body data, formatted as JSON
 * @returns {Promise<*>} (dict): The response data received from the server, parsed as JSON.
 */
async function makeRequest(url, method, body) {

    let headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/json'
    }
    if (method === 'post') {
        headers['X-CSRFToken'] = document.querySelector('[name=csrfmiddlewaretoken]').value
    }
    let response = await fetch(baseUrl + '/semantics/', {
        method: method,
        headers: headers,
        body: body,

    })
        .then((response) => response.json())

    return await response
}

/**
 *Retrieves an entity from the server based on the provided node ID and displays it in a Tabulator table.
 * @param nodeID (str): The ID of the node to retrieve the entity for.
 * @returns {Promise<void>}
 */
async function getEntity() {

    let data = await makeRequest(baseUrl + '/semantics/', 'post', JSON.stringify({nodeID: currentlyClickedNode}), null)
    var entity = await data['entity']

    entity.forEach(entry => {
        if (entry['Value']) {
            try {
                const parsedValue = JSON.parse(entry['Value']);
                entry['Value'] = JSON.stringify(parsedValue, null, 4).trim();
            } catch (error) {
                entry['Value'] = entry['Value'].replace(/'/g, '"');

            }
        }
    });

    // Define columns
    var columns = [
        {title: "Name", field: "Name", formatter: "textarea", widthGrow: 1},
        {title: "Value", field: "Value", formatter: "textarea", widthGrow: 2},
        {title: "Type", field: "Type", formatter: "textarea", widthGrow: 1},
        {title: "Metadata", field: "Metadata", formatter: "textarea", widthGrow: 2}
    ];

    // Create Tabulator table
    var table = new Tabulator("#table", {
        layout: "fitColumns",
        columns: columns,
        height: "300px",
        verticalFillMode: "fill",
        horizontalFillMode: "fill",
        columnVertAlign: true,
    });

    // Set data after table is built
    table.on("tableBuilt", function () {
        table.setData(entity);
    });
}

// Pick node and edge colors to be displayed first
const colors = ['#feb236', '#0dcaf0', '#D14D72', '#00FF00', '#107cad', '#57C5B6', '#6CDB42', '#ff7b25', '#bea0d7', '#B70404', '#F9F54B', '#9A1663', '#9F8772', '#FF8787']
const tcheckboxes = document.querySelectorAll('input[name="typecheckbox"]');
const rcheckboxes = document.querySelectorAll('input[name="relcheckbox"]');
const numAdditionalColors = tcheckboxes.length;

/*
Generates as many additional random colors as there are entities in orion
 */
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

/**
 * Inserts an endtry in the Dropdown menu in the main graph, which contains the color legends for types filter
 */
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

/**
 * Inserts an endtry in the Dropdown menu in the main graph, which contains the color legends for relationships filter
 */
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

function autoComplete(event) {
    var currentFocus;
    event.addEventListener("input", function (e) {

        var selectedOption = document.querySelector('.form-select-sm[name="searchOptions"] option:checked');
        var selectedValue = selectedOption.getAttribute('data-value');
        var arr = getData(selectedValue)

        var a, b, i, val = this.value
        closeAllLists();
        if (!val) {
            return false;
        }
        currentFocus = -1;
        a = document.createElement("DIV")
        a.setAttribute("id", this.id + "autocomplete-list")
        a.setAttribute("class", "autocomplete-items");
        var inputwidth = document.getElementById('searchentity');


        this.parentNode.appendChild(a)
        for (i = 0; i < arr.length; i++) {
            if (arr[i].substring(0, val.length).toUpperCase() === val.toUpperCase()) {
                b = document.createElement("DIV");
                b.innerHTML = "<strong>" + arr[i].substring(0, val.length) + "</strong>";
                b.innerHTML += arr[i].substring(val.length);
                b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
                b.addEventListener("click", function (e) {
                    event.value = this.getElementsByTagName("input")[0].value;
                    closeAllLists();
                });
                var container = document.querySelector('.autocomplete-items');
                container.style.width = inputwidth.offsetWidth + 'px';
                console.log(inputwidth.offsetWidth + 'px')
                a.appendChild(b);
            }
        }
    });
    event.addEventListener("keydown", function (e) {
        var x = document.getElementById(this.id + "autocomplete-list");
        if (x) x = x.getElementsByTagName("div");
        if (e.keyCode === 40) {
            currentFocus++;
            addActive(x);
        } else if (e.keyCode === 38) {
            currentFocus--;
            addActive(x);
        } else if (e.keyCode === 13) {
            e.preventDefault();
            if (currentFocus > -1) {
                if (x) x[currentFocus].click();
            }
        }
    });

    function addActive(x) {
        /*a function to classify an item as "active":*/
        if (!x) return false;
        /*start by removing the "active" class on all items:*/
        removeActive(x);
        if (currentFocus >= x.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = (x.length - 1);
        /*add class "autocomplete-active":*/
        x[currentFocus].classList.add("autocomplete-active");
    }

    function removeActive(x) {
        /*a function to remove the "active" class from all autocomplete items:*/
        for (var i = 0; i < x.length; i++) {
            x[i].classList.remove("autocomplete-active");
        }
    }

    function closeAllLists(elmnt) {
        /*close all autocomplete lists in the document,
        except the one passed as an argument:*/
        var x = document.getElementsByClassName("autocomplete-items");
        for (var i = 0; i < x.length; i++) {
            if (elmnt != x[i] && elmnt != event) {
                x[i].parentNode.removeChild(x[i]);
            }
        }
    }

    function getData(selectedValue) {
        if (selectedValue === 'id1') {
            return entity_ids
        } else if (selectedValue === 'type1') {
            return types
        } else if (selectedValue === 'relationship1') {
            return relationships
        } else if (selectedValue === 'name1') {
            return entity_names
        }
    }

    document.addEventListener("click", function (e) {
        closeAllLists(e.target);
    });
}

/**
 *Handles the search functionality based and calls the designated function based on the selected search option.
 * @param event event (Event): The event object triggered by the search action.
 */
function handleSearch(event) {
    event.preventDefault();
    var searchField = document.getElementById('searchentity')
    var input = searchField.value;
    var selectedOption = document.querySelector('.form-select-sm[name="searchOptions"] option:checked');
    var selectedValue = selectedOption.getAttribute('data-value');

    // Call the corresponding function based on the selected value
    if (selectedValue === null) {
        addWarning('Please select a search option!')
    } else if (selectedValue === 'id1') {
        handleIdSearch(input);
    } else if (selectedValue === 'type1') {
        handleTypeSearch(input);
    } else if (selectedValue === 'relationship1') {
        handleRelationshipSearch(input);
    } else if (selectedValue === 'name1') {
        handleNameSearch(input)
    }
}

/**
 * Function to escape ':' in the id of a node
 * @param str (str): The string which ':' are escapted
 * @returns {*} (str): escaped string or unchanged string
 */
function escapeColons(str) {
    if (typeof str === 'undefined') {
        console.log("übergebener Wert ist nicht definiert funktion escapeColons")
        return str; // Wenn der Wert undefined ist, wird er unverändert zurückgegeben
    }
    return str.replace(/:/g, '\\:');
}

/**
 * Checks if search field is empty
 */
function checkInputEmpty() {
    var searchField = document.querySelector('.form-control');
    var input = searchField.value;
    if (input.trim() === '') {
        clearSearchHighlight(previousInput)
    }
}

/**
 * This function handles the search by ID if this option is selected
 * @param inputValue (str): input string from the search field
 */
function handleIdSearch(inputValue) {

    var node = get_nodes_by_id(inputValue)
    if (node) {
        var element = escapeColons(inputValue)
        if (inputValue !== previousInput) {
            clearSearchHighlight(previousInput)
        }
        var newStyle = {
            "selector": 'node#' + element,
            style: {
                'background-color': searchcolor,
                'color': searchcolor
            }
        }
        currentStyleCy.styleSheets.push(newStyle);
        cy.style(currentStyleCy.styleSheets).update();
        previousInput = inputValue
    } else {
        addWarning("No matching Entity ID found. Perhaps you want to use another search option?")
    }
}

/**
 * This function handles the search by Type if this option is selected
 * @param inputValue (str): input string form search field
 */
function handleTypeSearch(inputValue) {
    if (types.includes(inputValue)) {
        const typeSelector = `.${inputValue}`;
        if (inputValue !== previousInput) {
            clearSearchHighlight(previousInput)
        }
        var newStyle = {
            "selector": typeSelector,
            style: {
                'background-color': searchcolor,
                'color': searchcolor
            }
        }
        currentStyleCy.styleSheets.push(newStyle);
        cy.style(currentStyleCy.styleSheets).update();
        previousInput = inputValue

    } else {
        addWarning('No matching Type found. Perhaps you want to use another search option?')
    }
}

/**
 * This function handles the search by Relationship if this option is selected
 * @param inputValue (str): input string form search field
 */
function handleRelationshipSearch(inputValue) {
    //var lowerCaseRels = relationships.map(function (item) {
    //    return item.toLowerCase();
    //});
    if (relationships.includes(inputValue)) {
        const relSelector = `edge[label = "${inputValue}"]`;
        if (inputValue !== previousInput) {
            clearSearchHighlight(previousInput)
        }
        var newStyle = {
            "selector": relSelector,
            style: {
                'line-color': searchcolor,
                'color': searchcolor
            }
        }
        currentStyleCy.styleSheets.push(newStyle);
        cy.style(currentStyleCy.styleSheets).update();
        previousInput = inputValue

    } else {
        addWarning('No matching Relationship found. Perhaps you want to use another search option?')
    }
}

/**
 * This function handles the search by name if this option is selected
 * @param inputValue (str): input string form search field
 */
function handleNameSearch(inputValue) {
    //var lowerCaseRels = relationships.map(function (item) {
    //    return item.toLowerCase();
    //});
    var foundObject = null;

    for (var i = 0; i < data.length; i++) {
        if (data[i].data && data[i].data.label === inputValue) {
            foundObject = data[i];
            break;
            //if at least one name is found the highlighting will be executed
        }
    }
    if (foundObject) {
        const nameSelector = `node[label = "${inputValue}"]`;
        if (inputValue !== previousInput) {
            clearSearchHighlight(previousInput)
        }
        var newStyle = {
            "selector": nameSelector,
            style: {
                'background-color': searchcolor,
                'color': searchcolor
            }
        }
        currentStyleCy.styleSheets.push(newStyle);
        cy.style(currentStyleCy.styleSheets).update();
        previousInput = inputValue

    } else {
        addWarning('No matching Name found. Perhaps you want to use another search option?')
    }
}

/**
 * This function adds a warning div if something went wrong during the search
 * @param warningText
 */
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

/**
 * This function colors corresponding node if checkbox is checked
 */
function colorNodes() {
    const nodecheckboxes = document.querySelectorAll('input[name="typecheckbox"]:checked');
    const originalColors = [];

    for (const checkbox of nodecheckboxes) {
        const id = `.${checkbox.id}`;
        const nodeindex = Array.from(tcheckboxes).indexOf(checkbox);
        const color = colors[nodeindex];
        cy.style() // changes node style by filtering for selectors
        var newStyle = {
            "selector": id,
            style: {
                'background-color': color,
            },
        }
        currentStyleCy.styleSheets.push(newStyle);
        cy.style(currentStyleCy.styleSheets).update();
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
                removeStyleBySelector('mainGraph', id)
                cy.style(currentStyleCy.styleSheets).update();

                if (!checkbox.checked) {
                    originalColors.splice(originalColorIndex, 1);
                }
            }
        });
    });
}

/**
 * This function colors corresponding edge if checkbox is checked
 */
function colorEdges() {
    const edgecheckboxes = document.querySelectorAll('input[name="relcheckbox"]:checked');
    const originalColors = [];

    for (const checkbox of edgecheckboxes) {
        const label = `edge[label = "${checkbox.id}"]`;
        const edgeindex = Array.from(rcheckboxes).indexOf(checkbox);
        const color = colors[edgeindex];
        var newStyle = {
            "selector": label,
            style: {
                "line-color": color,
            }
        }
        currentStyleCy.styleSheets.push(newStyle);
        cy.style(currentStyleCy.styleSheets).update();
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
                removeStyleBySelector('mainGraph', label)
                cy.style(currentStyleCy.styleSheets).update()
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


/**
 * This function adapts node labels as selected, otherwise default value name is set
 */
function changeLabel(labelName) {
    var nodeStyleMainGraph = currentStyleCy.styleSheets.find(function (styleObject) {
        return styleObject.selector === 'node';
    });
    var nodeStyleDetail = currentStyleDetail.styleSheets.find(function (styleObject) {
        return styleObject.selector === 'node';
    });

    switch (labelName) {
        case "id":
            nodeStyleMainGraph.style.label = 'data(id)';
            nodeStyleDetail.style.label = 'data(id)';
            break;
        case "name":
            nodeStyleMainGraph.style.label = 'data(label)';
            nodeStyleDetail.style.label = 'data(label)';
            break;
        case "none":
            nodeStyleMainGraph.style.label = '';
            nodeStyleDetail.style.label = '';
            break;
    }
    cy.style(currentStyleCy.styleSheets).update();
    detail.style(currentStyleDetail.styleSheets).update();
}

/**
 * This function adapts the layout as selected
 */
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

/**
 * This function redirects the user to the Entity page if he/she clicked on the "edit" button
 */
function editEntity() {
    entitiesUrl = currentUrl.split('/semantics/')[0]
    var newUrl = entitiesUrl + "/entities/" + currentlyClickedNode + "/" + currentNodeType + "/update/";
    //window.open(newUrl, 'Popup-Fenster', 'width=800,height=600')// idea for popup window instead of redirection
    window.location.href = newUrl;

}

/**
 * This function creates a contextmenu with attributes and actions at right clicked mouse event
 */
var selectionmenu = {
    menuRadius: function (ele) {
        return 100;
    },
    minSpotlightRadius: 18,
    fillColor: 'rgba(0, 0, 0, 0.75)',
    activeFillColor: 'rgba(1, 105, 217, 0.75)',
    selector: 'node',
    commands: [ // add actions or functions for the contextmenu to commands
        {
            content: 'Remove node from graph',
            select: function (ele) {
                ele.remove();
            }
        },
        {
            content: 'Add entity',
            select: function () {
                createUrl = currentUrl.split('/semantics/')[0]
                var newUrl = createUrl + "/entities/create/";
                window.location.href = newUrl;
            }
        },
        /* Adds a parent node to the graph, which has the selected node as a target
        * This is only a frontend solution
        * For creating an entity in the backend, the JSON has to be passed to Orion
        {
            content: 'Add parent node',
            select: function (ele) {
                var childrenNode = ele.id();
                console.log(childrenNode);
                var newEntityData = {
                    id: 'urn:ngsi-ld:newEntity',
                    label: 'newEntity',
                    children: {
                            group: 'nodes',
                            data: {
                                id: childrenNode,
                                label: ele.data('label'),
                            }
                        }
                }
                cy.add({
                    group: 'nodes',
                    data: newEntityData,
                });
                cy.add({
                    group: 'edges',
                    data: {
                      id: 'edgeId',
                      source: cy.getElementById('urn:ngsi-ld:newEntity').id(),
                      target: childrenNode,
                    },
                  });
            }
        },*/
        {
            content: 'Edit this entity',
            select: function (ele) {
                currentlyClickedNode = ele.id();
                currentNodeType = ele.classes()[0];
                editEntity();
            }
        },
        {
            content: 'Show Attributes',
            select: async function (ele) {
                var nodeID = ele.id();
                currentlyClickedNode = get_nodes_by_id(nodeID);
                currentNodeType = ele.classes()[0];
                let requestBody = JSON.stringify({nodeID});
                let response = await makeRequest(baseUrl + '/semantics/', 'post', requestBody);
                var attributes = response.entity;
                var attributesListHTML = '';
                for (var i = 0; i < attributes.length; i++) {
                    var attribute = attributes[i];
                    attributesListHTML += '<p>' + attribute.Name + ': ' + attribute.Value + '</p>';
                }
                document.getElementById("attributesList").innerHTML = attributesListHTML;
                var modal = document.getElementById("myModal");
                modal.style.display = "block";
                var closeBtn = document.getElementsByClassName("close")[0];
                closeBtn.onclick = function () {
                    modal.style.display = "none";
                };
                window.onclick = function (event) {
                    if (event.target === modal) {
                        modal.style.display = "none";
                    }
                }
            }
        }
    ],
};
cy.cxtmenu(selectionmenu);

document.addEventListener("contextmenu", function (event) {
    var modal = document.getElementById("myModal");
    var isInsideModal = false;
    var targetElement = event.target;
    while (targetElement) {
        if (targetElement === modal || targetElement.id === "attributesList" || targetElement.id === "myModal") {
            isInsideModal = true;
            break;
        }
        targetElement = targetElement.parentElement;
    }
    if (isInsideModal) {
        event.preventDefault();
    }
});

/**
 * This function resets the graph after moving/deleting nodes
 */
function refreshGraph() {
    cy.elements().remove();
    cy.add(data);
    changeLayout('breadthfirst');
}

/**
 * This function adapts the display area
 */
function scrollToDetail() {
    var detialview = document.getElementById("detail_level");
    detialview.scrollIntoView({behavior: "smooth"});
}

function scrollToMain() {
    window.scrollTo({top: 0, behavior: "smooth"});
}


