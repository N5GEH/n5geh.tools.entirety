;(function () {
    let addButton = document.querySelectorAll(".add-entity");

    addButton.forEach(function (elem) {
        elem.addEventListener("click", function (event) {
            event.preventDefault();
            alert('add clicked')
        });
    });
})()
