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

                if(image.description.length) {
                    descriptionTextArea.value = image.description;
                }
            }
        });
    });

});
promise.catch(error => alert(error));
