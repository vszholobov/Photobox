"use strict"


class Column {
    constructor(elementId) {
        this.self = document.getElementById(elementId);
        this.height = 0;
    }

    changeHeight(height) {
        this.height += height;
    }

    addImage(image) {
        let mainDiv = document.createElement("div");
        let divImageContainer = document.createElement("div");

        mainDiv.classList.add("img_container");
        divImageContainer.classList.add("left_side_img_container");
        divImageContainer.append(image);
        mainDiv.append(divImageContainer);

        this.self.append(mainDiv);
    }
}

class Image {
    constructor(imageObject) {
        this.node = document.createElement("img");
        this.node.src = `/static/users/${imageObject.user_id}/images/${imageObject.image_file}`;
        this.node.className = "img";

        this.id = imageObject.id;
        this.tagList = imageObject.tag_list;
        this.fileName = imageObject.image_file;
        this.userId = imageObject.user_id;
        this.description = imageObject.description;
        this.creationDate = imageObject.creation_date;
        this.htwRatio = imageObject.htwRatio;
        this.hidden = imageObject.hidden;
    }

    hide() {
        this.node.classList.add("hidden");
    }

    show() {
        this.node.classList.remove("hidden");
    }
}

function initializePage(imageList, columns, images) {
    const columnWidth = columns[0].self.offsetWidth;
    for(let i = 0; i < imageList.length; i++) {
        let minHeight = 10000;
        let currentColumn = null;
        columns.forEach(column => (column.height < minHeight)? [minHeight, currentColumn] = [column.height, column]: null);

        images.push(new Image(imageList[i]));
        currentColumn.addImage(images[i].node);

        currentColumn.changeHeight(imageList[i].htwRatio * columnWidth);
    }
}

// Создает теги, переданные в tagList
function createTags(tagList) {
    const placeToPut = document.querySelector(".add_tags_div");
    let listOfCheckboxes = [];

    for(let tag of tagList) {
        let checkboxDiv = document.createElement("div");
        checkboxDiv.classList.add("aside_center");
        checkboxDiv.classList.add("checkbox_div");
        checkboxDiv.setAttribute("title", tag);

        let checkboxLabel = document.createElement("label");

        let checkbox = document.createElement("input");
        checkbox.classList.add("checkbox");
        checkbox.setAttribute("type", "checkbox");
        checkbox.setAttribute("value", tag);
        checkbox.setAttribute("name", "check");
        checkboxLabel.append(checkbox);

        listOfCheckboxes.push(checkbox);

        let checkboxSpan = document.createElement("span");
        checkboxSpan.classList.add("checkbox_span");
        checkboxSpan.innerText = tag;
        checkboxLabel.append(checkboxSpan);

        checkboxDiv.append(checkboxLabel);
        placeToPut.before(checkboxDiv);
    }
}

// Список столбцов, куда будут добавляться фотографии
let columns = [new Column("img_column1"),
               new Column("img_column2")];

// Список объектов класса Image. Используется при поиске.
let images = [];

// Список питоновских объектов фотографий. Используется при инициализации страницы.
let imageList = [];

// Фотография, которую обрабатывают.
let current_active_element = null;

// Promise на получение фотографий с сервера при открытии страницы
let promise = new Promise(function(resolve, reject) {
    $.ajax({
        type: 'POST',
        url: '/ajax',
        contentType: 'application/json',
        dataType: 'json',
        data: JSON.stringify({"action": "get_my_images"}),
        success: function(data) {
            imageList = data;
            resolve('result');
        },
        error: function() {
            reject(new Error("Произошла ошибка( Попробуйте перезагрузить страницу."));
        }
    });
});
promise.then(function(result) {
    // Создает фотографии на странице
    initializePage(imageList, columns, images);

    const imagesNodeList = images.map(image => image.node);

    let photoZone = document.getElementById("photo_container");
    let tagsZone = document.getElementById("checkbox_container");
    let descriptionTextArea = document.getElementById("description_textarea");

    let column_to_return = null;
    let hideImageButton = document.getElementById("hide_image");
    let saveDescriptionButton = document.getElementById("save_description");
    let deleteTagsButton = document.getElementById("delete_tags");
    let deletePhotoButton = document.getElementById("delete_image");

    [].forEach.call(imagesNodeList, function(imageNode) {
        imageNode.addEventListener("click", function() {
            if(!current_active_element) {
                current_active_element = imageNode;
                column_to_return = imageNode.closest(".img_column");
                photoZone.append(imageNode);
            } else if(current_active_element == imageNode) {
                current_active_element = null;
                column_to_return.append(imageNode);
                column_to_return = null;
            } else {
                column_to_return.append(current_active_element);
                current_active_element = imageNode;
                column_to_return = imageNode.closest(".img_column");
                photoZone.append(imageNode);
            }

            let image = images.find(img => img.node == current_active_element);

            if(tagsZone.children.length) {
                for(let i = 0; i < tagsZone.children.length; i++) {
                    tagsZone.children[i].remove();
                    i--;
                }
            }

            descriptionTextArea.value = "";

            if(image) {
                if(image.tagList.length) {
                    for(let tag of image.tagList) {
                        let checkbox_div = document.createElement("div");
                        checkbox_div.classList.add("aside_center");
                        checkbox_div.classList.add("checkbox_div");
                        checkbox_div.title = tag;

                        let label = document.createElement("label");

                        let checkbox = document.createElement("input");
                        checkbox.type = "checkbox";
                        checkbox.classList.add("checkbox");
                        checkbox.name = "check";
                        checkbox.value = tag;

                        let span = document.createElement("span");
                        span.classList.add("checkbox_span");
                        span.innerText = tag;

                        label.append(checkbox);
                        label.append(span);

                        checkbox_div.append(label);
                        tagsZone.append(checkbox_div);
                    }
                }
                let input_div = document.createElement("div");
                input_div.classList.add("aside_center");
                input_div.classList.add("add_tags_div");

                let input_text = document.createElement("input");
                input_text.id = "inputTags";
                input_text.type = "text";
                input_text.placeholder = "Добавить теги";
                input_text.title = "Пример: #Тег";
                input_text.required = true;

                input_div.append(input_text);

                let input_submit = document.createElement("input");
                input_submit.id = "submitTags";
                input_submit.type = "submit";
                input_submit.value = "Добавить";

                input_div.append(input_submit);

                tagsZone.append(input_div);

                if(image.description.length) {
                    descriptionTextArea.value = image.description;
                }

                let submitButton = document.getElementById("submitTags");
                submitButton.addEventListener("click", function() {
                    let tagsInput = document.getElementById("inputTags");
                    let current_image = images.find(img => img.node == current_active_element);
                    $.ajax({
                        type: 'POST',
                        url: '/ajax',
                        contentType: 'application/json',
                        dataType: 'json',
                        data: JSON.stringify({"action": "addTagsToImage", "tags": tagsInput.value, "imageId": current_image.id}),
                        success: function(data) {
                            if(data.length) {
                                for(let tag of data) {
                                    current_image.tagList.push(tag);
                                }
                                createTags(data);
                            } else {
                                alert("Введеные теги уже есть в вашем списке.");
                            }
                        },
                        error: function() {
                            alert("Произошла ошибка( Попробуйте перезагрузить страницу.");
                        }
                    });
                });

                if(image.hidden) {
                    hideImageButton.innerText = "Сделать общедоступной";
                } else {
                    hideImageButton.innerText = "Скрыть фотографию";
                }
            }
        });
    });

    hideImageButton.addEventListener("click", function() {
        let current_image = images.find(img => img.node == current_active_element);
        if(current_image) {
            $.ajax({
                type: 'POST',
                url: '/ajax',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify({"action": "changeImageHiddenAttr", "hidden": current_image.hidden, "imageId": current_image.id}),
                success: function() {
                    current_image.hidden = !current_image.hidden;
                    if(current_image.hidden) {
                        hideImageButton.innerText = "Сделать общедоступной";
                        alert("Фотография была успешно скрыта");
                    } else {
                        hideImageButton.innerText = "Скрыть фотографию";
                        alert("Фотография была успешно сделана общедоступной");
                    }
                },
                error: function() {
                    alert("Произошла ошибка( Попробуйте перезагрузить страницу.");
                }
            });
        }
    });

    saveDescriptionButton.addEventListener("click", function() {
        let current_image = images.find(img => img.node == current_active_element);
        if(current_image) {
            let textArea = document.getElementById("description_textarea");
            $.ajax({
                type: 'POST',
                url: '/ajax',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify({"action": "changeDescription", "description": textArea.value, "imageId": current_image.id}),
                success: function() {
                    current_image.description = textArea.value;
                    alert("Описание успешно изменено");
                },
                error: function() {
                    alert("Произошла ошибка( Попробуйте перезагрузить страницу.");
                }
            });
        }
    });

    deleteTagsButton.addEventListener("click", function() {
        let current_image = images.find(img => img.node == current_active_element);
        if(current_image) {
            let checkboxes = Array.from(document.querySelectorAll(".checkbox"));
            checkboxes = checkboxes.filter(checkbox => checkbox.checked);
            checkboxes = checkboxes.map(checkbox => checkbox.value);
            $.ajax({
                type: 'POST',
                url: '/ajax',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify({"action": "deleteTagsImage", "tags": checkboxes, "imageId": current_image.id}),
                success: function(data) {
                    let checkboxes = Array.from(document.querySelectorAll(".checkbox"));
                    checkboxes = checkboxes.filter(checkbox => checkbox.checked);
                    checkboxes = checkboxes.map(checkbox => checkbox.closest(".checkbox_div"))
                    for(let div of checkboxes) {
                        div.remove();
                    }
                },
                error: function() {
                    alert("Произошла ошибка( Попробуйте перезагрузить страницу.");
                }
            });
        }
    });

    deletePhotoButton.addEventListener("click", function() {
        let current_image = images.find(img => img.node == current_active_element);
        if(current_image) {
            $.ajax({
                type: 'POST',
                url: '/ajax',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify({"action": "userDeletePhoto", "imageId": current_image.id}),
                success: function(data) {
                    if(data.status == "success") {
                        imageList.splice(imageList.indexOf(current_active_element), 1);
                        images.splice(images.indexOf(current_image), 1);
                        current_active_element.remove();
                        current_active_element = null;
                        alert("Фото успешно удалено.");
                    } else {
                        alert("Произошла ошибка( Попробуйте перезагрузить страницу.");
                    }
                },
                error: function() {
                    alert("Произошла ошибка( Попробуйте перезагрузить страницу.");
                }
            });
        }
    });
});
promise.catch(error => alert(error));
