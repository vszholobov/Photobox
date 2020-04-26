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

let currentUserId = 0;

let current_active_element;

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

    //const imagesNodeList = images.map(image => image.node);

    /*
    // Навешиваем обработчик кликов на фотографии. При клике появляется широкая область с описанием фотографии.
    [].forEach.call(imagesNodeList, function(imageNode, index) {
        imageNode.addEventListener('click', function() {



            if(current_active_element) {
                document.querySelector(".description_zone").remove();
                document.querySelector(".close").remove();
                document.querySelectorAll(".arrow").forEach(arrow => arrow.remove());
                document.querySelector(".active_img").classList.remove("active_img");
                current_active_element.classList.remove("active_container");
            }

            // Кнопка крест в правом верхнем углу
            let closeButton = document.createElement("span");
            closeButton.classList.add("close");
            current_active_element.append(closeButton);

            closeButton.addEventListener("click", function(self) {
                document.querySelector(".description_zone").remove();
                document.querySelector(".close").remove();
                document.querySelectorAll(".arrow").forEach(arrow => arrow.remove());
                current_active_element.classList.remove("active_container");

                current_active_element = null;
            });
        });
    });
    */
});
promise.catch(error => alert(error));

