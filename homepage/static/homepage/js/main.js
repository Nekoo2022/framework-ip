document.addEventListener("DOMContentLoaded", function () {
    var path = window.location.pathname;
    var links = document.querySelectorAll("[data-nav]");

    links.forEach(function (link) {
        var prefix = link.getAttribute("data-nav");
        var matched = prefix === "/"
            ? path === "/"
            : path.indexOf(prefix) === 0;
        if (matched) {
            link.classList.add("active");
        }
    });

    var status = document.getElementById("js-status");
    if (status) {
        status.textContent = "Скрипт интерфейса выполнен";
    }
});
