;(function () {
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));

    const url = window.location.pathname;

    const sidebarItems = document.querySelectorAll('.btn-sidebar');
    [...sidebarItems].forEach(el => {
        if(el.getAttribute("href") === url){
            el.classList.add("active")
        }
        else if (!el.classList.contains("hi-ignore")) {
            let regEx = new RegExp(`^${el.getAttribute("href")}.*$`, "i")
            if (regEx.test(url))
                el.classList.add('active')
        }
    })
})()


document.addEventListener("DOMContentLoaded", function () {

    document.querySelectorAll(".dropdown-menu").forEach(menu => {
        menu.addEventListener("click", e => e.stopPropagation());
    });

    document.querySelectorAll(".dropdown").forEach(dropdown => {

        const selectAll = dropdown.querySelector(".select-all");
        const items = dropdown.querySelectorAll(".item-checkbox");

        if (!selectAll || !items.length) return;

        selectAll.addEventListener("change", function () {
            items.forEach(cb => {
                if (!cb.disabled) {
                    cb.checked = this.checked;
                }
            });

            selectAll.indeterminate = false;
        });

        items.forEach(cb => {
            cb.addEventListener("change", function () {

                const enabledItems = [...items].filter(i => !i.disabled);

                const allChecked = enabledItems.every(i => i.checked);
                const noneChecked = enabledItems.every(i => !i.checked);

                selectAll.checked = allChecked;
                selectAll.indeterminate = !allChecked && !noneChecked;
            });
        });

    });


    document.querySelectorAll(".search-input").forEach(input => {

        input.addEventListener("input", function () {

            const query = this.value.toLowerCase().trim();

            const dropdown = this.closest(".dropdown");
            if (!dropdown) return;

            const rows = dropdown.querySelectorAll(".item-checkbox");

            console.log("rows found:", rows.length);

            for (let i = 0; i < rows.length; i++) {

                const cb = rows[i];
                const row = cb.closest(".form-check");
                if (!row) continue;

                if (row.classList.contains("select-all-row")) {
                    row.classList.remove("hidden-item");
                    continue;
                }

                const label = row.querySelector("label");
                const text = (label?.innerText || "").toLowerCase();

                if (text.includes(query)) {
                    row.classList.remove("hidden-item");
                } else {
                    row.classList.add("hidden-item");
                }
            }

        });

    });

    document.querySelectorAll(".select-all-row").forEach(row => {
        const checkbox = row.querySelector(".select-all");

        row.addEventListener("click", function (e) {
            if (e.target.tagName.toLowerCase() === "input") return;

            checkbox.checked = !checkbox.checked;
            checkbox.dispatchEvent(new Event("change"));
        });
    });

});
