document.getElementById("liked").addEventListener("click", function() {
    var buttonState = this.getAttribute("data-state") === "true";
    // Toggle button state
    buttonState = !buttonState;
    this.setAttribute("data-state", buttonState.toString());

    // Send button state to Django
    sendLiked(buttonState);

    // Change image based on button state
    var imageUrl = buttonState ? "static/icons/favourite.png" : "static/icons/favourite (1).png";
    document.getElementById("likedImg").src = imageUrl;
    console.log('clicked');
});

document.getElementById("watch_later").addEventListener("click", function() {
    var buttonState = this.getAttribute("data-state") === "true";
    // Toggle button state
    buttonState = !buttonState;
    this.setAttribute("data-state", buttonState.toString());

    // Send button state to Django
    sendWatchLater(buttonState);

    // Change image based on button state
    var imageUrl = buttonState ? "static/icons/tag.png" : "static/icons/tag (1).png";
    document.getElementById("laterImg").src = imageUrl;
});

function sendLiked(state) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "{% url 'update_button_state' %}", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            console.log(xhr.responseText);
        }
    };
    xhr.send(JSON.stringify({ state: state }));
}

function sendWatchLater(state) {
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "{% url 'update_button_state' %}", true);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                console.log(xhr.responseText);
            }
        };
        xhr.send(JSON.stringify({ state: state }));
}