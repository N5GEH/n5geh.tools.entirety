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

document.addEventListener('DOMContentLoaded', function() {
    const searchListPairs = [
        { search: 'viewerSearch', list: 'viewerList' },
        { search: 'userSearch', list: 'userList' },
        { search: 'maintainerSearch', list: 'maintainerList' }
    ];

    searchListPairs.forEach(function(pair) {
        const searchElement = document.getElementById(pair.search);
        const listElement = document.getElementById(pair.list);

        searchElement.addEventListener('input', function() {
            const query = this.value.toLowerCase();
            const checkboxes = listElement.querySelectorAll('.form-check');

            checkboxes.forEach(function(checkbox) {
                const label = checkbox.querySelector('label').textContent.toLowerCase();
                checkbox.style.display = label.includes(query) ? 'block' : 'none';
            });
        });
    });
});
