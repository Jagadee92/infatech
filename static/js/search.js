document.addEventListener("DOMContentLoaded", function () {
    var form = document.getElementById("search-form");
    var input = document.getElementById("company");
    var clearButton = document.getElementById("clear-search");
    var box = document.getElementById("suggestions");
    var url = box.dataset.url;
    var timer = null;
    var activeIndex = -1;

    function options() {
        return box.querySelectorAll(".suggestion");
    }

    function showClearButton() {
        clearButton.classList.toggle("show", input.value !== "");
    }

    function closeBox() {
        box.innerHTML = "";
        box.classList.remove("open");
        activeIndex = -1;
    }

    function highlight(index) {
        var items = options();

        if (items.length === 0) {
            return;
        }

        if (index < 0) {
            index = items.length - 1;
        }

        if (index >= items.length) {
            index = 0;
        }

        items.forEach(function (item) {
            item.classList.remove("is-active");
        });

        items[index].classList.add("is-active");
        activeIndex = index;
    }

    function choose(value) {
        input.value = value;
        showClearButton();
        closeBox();
        form.submit();
    }

    function openBox(results) {
        closeBox();

        if (results.length === 0) {
            return;
        }

        results.forEach(function (company) {
            var option = document.createElement("button");

            option.type = "button";
            option.className = "suggestion";

            option.textContent =
                company.name +
                " | Ticker: " +
                company.ticker +
                " | Doc ID: " +
                company.docid +
                " | Org ID: " +
                company.orgid;

            option.addEventListener("click", function () {
                choose(company.name);
            });

            box.appendChild(option);
        });

        box.classList.add("open");
        highlight(0);
    }

    function loadSuggestions() {
        var keyword = input.value.trim();

        if (keyword === "") {
            closeBox();
            return;
        }

        fetch(url + "?q=" + encodeURIComponent(keyword))
            .then(function (response) {
                if (!response.ok) {
                    throw new Error("Search request failed");
                }

                return response.json();
            })
            .then(function (data) {
                openBox(data.results);
            })
            .catch(function () {
                closeBox();
            });
    }

    input.addEventListener("input", function () {
        showClearButton();

        clearTimeout(timer);

        timer = setTimeout(function () {
            loadSuggestions();
        }, 250);
    });

    input.addEventListener("keydown", function (event) {
        var items = options();

        if (event.key === "Escape") {
            closeBox();
            return;
        }

        if (items.length === 0) {
            return;
        }

        if (event.key === "ArrowDown") {
            event.preventDefault();
            highlight(activeIndex + 1);
        } else if (event.key === "ArrowUp") {
            event.preventDefault();
            highlight(activeIndex - 1);
        } else if (event.key === "Enter" && activeIndex >= 0) {
            event.preventDefault();
            choose(items[activeIndex].textContent);
        }
    });

    clearButton.addEventListener("click", function () {
        input.value = "";
        showClearButton();
        closeBox();
        input.focus();
    });

    document.addEventListener("click", function (event) {
        if (!box.contains(event.target) && event.target !== input) {
            closeBox();
        }
    });

    showClearButton();
});