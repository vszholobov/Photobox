"use strict"
const dropArea = document.getElementsByClassName("drag_zone")[0];
const fileInput = document.getElementById("file-input");
const fileName = document.getElementById("file-name");
const boxImage = document.getElementById("box-image");
const imagesRoute = "/static/uploadImages/";
const json = document.getElementsByClassName("json")[0];
const imageList = ["404.jpg", "boxFilled1.png", "boxFilled2.png", "boxFilled3.png", "boxFilled4.png"];
const allowedTypes = ["image/jpeg", "image/jpg", "image/png"];

['dragenter', 'dragover'].forEach(eventName => {
  dropArea.addEventListener(eventName, highlight, false);
});
['dragleave', 'drop'].forEach(eventName => {
  dropArea.addEventListener(eventName, unhighlight, false);
});
function highlight() {
  dropArea.classList.add('highlight');
}
function unhighlight() {
  dropArea.classList.remove('highlight');
}

fileInput.onchange = function() {
  if(!fileInput.files || !fileInput.files.length) {
    boxImage.src = imagesRoute + imageList[0];
    dropArea.classList.remove("highlight");
    fileName.textContent = "";
  }
  else {
    for(let file of fileInput.files) {
      if(!allowedTypes.includes(file.type)) {
        fileInput.value = "";
        fileName.textContent = "";
        boxImage.src = imagesRoute + imageList[0];
        json.classList.remove("json");
        setTimeout(function() {
          json.classList.add("json")
        }, 3000);
      }
    }
    if(fileInput.value) {
      let countFiles = fileInput.files.length;
      let imageName = (countFiles < 4)? imageList[countFiles]: imageList[4];
      boxImage.src = imagesRoute + imageName;
      fileName.textContent = Array.from(fileInput.files).map(item => item.name).join(" ");
    }
  }
}