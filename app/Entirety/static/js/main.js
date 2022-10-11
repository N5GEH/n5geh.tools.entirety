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
