async function changeImage(data) {
    const path = await eel.returnImg(data)();
    setImage(path);
}

function setImage(path) {
    document.getElementById("image").src = path;
}
eel.expose(setImage);  
