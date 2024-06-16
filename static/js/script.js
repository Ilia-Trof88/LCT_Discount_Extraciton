function auto_grow(element) {
    element.style.height = "5px";
    element.style.height = (element.scrollHeight)+"px";
    };
document.querySelector("form").onsubmit = function(e) {
    e.preventDefault();
    var phrase = document.querySelector(".textarea").value; // получить фразу
    var xhr = new XMLHttpRequest(); // инициализация запроса
    xhr.open("POST", "/input", true);
    xhr.setRequestHeader("Content-Type", "application/json"); // тип содержимого
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    xhr.onreadystatechange = function() {
        if (xhr.status == 200 && xhr.readyState == 4) {
            let respond = JSON.parse(xhr.responseText);
            document.querySelector("#result").innerHTML = respond["message"];
        }
    };
    xhr.onloadend = function() {
        document.documentElement.style.setProperty("--color-form-submit-bg", "#0fa134");
    };
    xhr.onloadstart = function() {
        document.documentElement.style.setProperty("--color-form-submit-bg", "#0fa13379");
    };
    xhr.send(JSON.stringify({"phrase" : phrase})); // отправка запроса



};
