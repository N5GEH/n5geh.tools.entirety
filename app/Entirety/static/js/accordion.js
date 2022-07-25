const attrForm = document.getElementsByClassName("d_attr_form");
const mainForm = document.querySelector("#form-container");
const addButton = document.querySelector("#add-form");
const totalForms = document.querySelector("#id_form-TOTAL_FORMS");

let formCount = attrForm.length - 1;

addButton.addEventListener("click", function (event) {
    event.preventDefault();

    const newAttrForm = attrForm[0].cloneNode(true);
    const formRegex = RegExp(`div_id_form-(\\d){1}-`, 'g');

    formCount++;

    newAttrForm.innerHTML = newAttrForm.innerHTML.replace(formRegex, `div_id_form-${formCount}-`);
    mainForm.append(newAttrForm);

    let removeChildButton = newAttrForm.querySelector('.remove-form');
    removeChildButton.addEventListener("click", function () {
        removeChildButton.parentElement.remove();
    })

});


let removeButton = document.querySelectorAll(".remove-form");
removeButton.forEach(function (elem) {
    elem.addEventListener("click", function () {
        //elem.preventDefault();
        elem.parentElement.remove();
    });
});
