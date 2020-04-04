"use strict"


function addListenerToAddTagButton() {
    const addTagsDiv = document.querySelector(".add_tags_div");
    const submitButton = document.getElementById("submitTags");
    const tagsInput = document.getElementById("inputTags");

    submitButton.addEventListener("click", function() {
        // Проверка ввода
        if(!tagsInput.value.includes("#") || (tagsInput.value.trim().length == 1)) {
            alert("Теги вводятся через #. Пример: #Тег.");
            return null;
        }

        $.ajax({
            type: 'POST',
            url: '/ajax',
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify({"action": "addTags", "tags": tagsInput.value}),
            success: function(data) {
                if(data.length) {
                    createTags(data);
                } else {
                    alert("Введеные теги уже есть в вашем списке.")
                }
            },
            error: function() {
                alert("Произошла ошибка( Попробуйте перезагрузить страницу.");
            }
        });
    });
}

function createTags(tagList) {
    const placeToPut = document.querySelector(".add_tags_div");

    for(let tag of tagList) {
        let checkboxDiv = document.createElement("div");
        checkboxDiv.classList.add("aside_center");
        checkboxDiv.classList.add("checkbox_div");
        checkboxDiv.setAttribute("title", tag);

        let checkboxLabel = document.createElement("label");

        let checkbox = document.createElement("input");
        checkbox.classList.add("upload_checkbox");
        checkbox.setAttribute("type", "checkbox");
        checkbox.setAttribute("value", tag);
        checkbox.setAttribute("name", "check");
        checkbox.setAttribute("form", "upload_form");
        checkboxLabel.append(checkbox);

        let checkboxSpan = document.createElement("span");
        checkboxSpan.classList.add("checkbox_span");
        checkboxSpan.innerText = tag;
        checkboxLabel.append(checkboxSpan);

        checkboxDiv.append(checkboxLabel);
        placeToPut.before(checkboxDiv);
    }
}

const dropArea = document.getElementsByClassName("drag_zone")[0];
const fileInput = document.getElementById("file-input");
const fileName = document.getElementById("file-name");
const boxImage = document.getElementById("box-image");
const imagesRoute = "/static/uploadImages/";
const json = document.getElementsByClassName("json")[0];
const imageList = ["boxFilled0.png", "boxFilled1.png", "boxFilled2.png", "boxFilled3.png", "boxFilled4.png"];
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

//Навешиваем обработчик клика на кнопку "Добавить теги"
document.addEventListener("DOMContentLoaded", addListenerToAddTagButton);
