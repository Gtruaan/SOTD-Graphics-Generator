/*
    I need to check if the image is loaded before taking a screenshot.

    This is a temporary solution.
*/
document.querySelector("#track-image").addEventListener("load", () => {
    let checkDiv = document.createElement("div");
    document.querySelector("#main").appendChild(checkDiv);
    checkDiv.id = "load-checker";
});