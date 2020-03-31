/*
const blocks = document.getElementsByClassName("img");
const close_buttons = document.querySelectorAll(".img_container .close");
let current_active_element;

[].forEach.call(blocks, function(item) {
    item.addEventListener('click', () => {
        if(current_active_element) {
            current_active_element.closest(".img_container").classList.remove('active_container');
        }
        item.closest(".img_container").classList.add('active_container');
        current_active_element = item;
    });
});
[].forEach.call(close_buttons, function(item) {
    item.addEventListener('click', () => {
        document.querySelector(".active_container").classList.remove("active_container");
        current_active_element = null;
    });
});*/
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

function searchImages(columns, images, searchTagList) {
    const columnWidth = columns[0].self.offsetWidth;

    // Обнуление колонки перед поиском
    columns.forEach(function(column) {
        column.height = 0;
        column.divNumber = 0;
        for(let i = 0; i < column.self.childElementCount; i++) {
            column.self.children[i].remove();
            i--;
        }
    });
    if(searchTagList.length) {
        //images.forEach(image => image.node.remove())
        for(let i = 0; i < images.length; i++) {
            image = images[i];
            let MatchingTags = image.tagList.filter(tag => searchTagList.includes(tag)? true: false);

            if(MatchingTags.length && image.tagList.length) {
                let minHeight = 10000;
                let currentColumn = null;
                columns.forEach(column => (column.height < minHeight)? [minHeight, currentColumn] = [column.height, column]: null);

                currentColumn.addImage(images[i].node);

                currentColumn.changeHeight(images[i].htwRatio * columnWidth);
            }
        }
    } else {
        for(let i = 0; i < images.length; i++) {
            image = images[i];

            let minHeight = 10000;
            let currentColumn = null;
            columns.forEach(column => (column.height < minHeight)? [minHeight, currentColumn] = [column.height, column]: null);

            currentColumn.addImage(images[i].node);

            currentColumn.changeHeight(images[i].htwRatio * columnWidth);
        }
    }
}

// Список столбцов, куда будут добавляться фотографии
let columns = [new Column("img_column1"),
               new Column("img_column2"),
               new Column("img_column3"),
               new Column("img_column4")];

// Список объектов класса Image. Используется при поиске.
let images = [];

// Список питоновских объектов фотографий. Используется при инициализации страницы.
let imageList = [];

// Список юзеров.
let userList = [];

// Хранит в себе объект текущего открытого div'a с изображением.
let current_active_element = null;

// Список объектов чекбоксов. Используются при поиске.
const checkboxes = document.getElementsByClassName("upload_checkbox");

let promise = new Promise(function(resolve, reject) {
    $.ajax({
        type: 'POST',
        url: '/ajax',
        contentType: 'application/json',
        dataType: 'json',
        data: JSON.stringify({"action": "init"}),
        success: function(data) {
            imageList = data[0];
            userList = data[1];
            resolve('result');
        },
        error: function() {
            reject(new Error("Произошла ошибка( Попробуйте перезагрузить страницу."));
        }
    });
});
promise.then(function(result) {
    initializePage(imageList, columns, images);
    const imagesNodeList = images.map(image => image.node);

    // Навешиваем обработчик кликов на фотографии. При клике появляется широкая область с описанием фотографии.
    [].forEach.call(imagesNodeList, function(imageNode, index) {
        imageNode.addEventListener('click', function() {
            if(current_active_element) {
                document.querySelector(".description_zone").remove();
                document.querySelector(".close").remove();
                document.querySelector(".active_img").classList.remove("active_img");
                current_active_element.classList.remove("active_container");
            }
            imageNode.classList.add("active_img");
            current_active_element = imageNode.closest(".img_container");
            current_active_element.classList.add("active_container");

            // Зона описания
            let descriptionDiv = document.createElement("div");
            descriptionDiv.classList.add("description_zone");

            let authorAvatar = document.createElement("img");
            authorAvatar.src = userList[images[index].userId - 1][1];
            authorAvatar.classList.add("author_avatar");
            descriptionDiv.append(authorAvatar);

            let authorNameSpan = document.createElement("span");
            authorNameSpan.innerText = userList[images[index].userId - 1][0];
            descriptionDiv.append(authorNameSpan);

            current_active_element.append(descriptionDiv);

            // Кнопка крест в правом верхнем углу
            let closeButton = document.createElement("span");
            closeButton.classList.add("close");
            current_active_element.append(closeButton);

            closeButton.addEventListener("click", function(self) {
                document.querySelector(".description_zone").remove();
                document.querySelector(".close").remove();
                current_active_element.classList.remove("active_container");

                current_active_element = null;
            });
        });
    });
});
promise.catch(error => alert(error));

[].forEach.call(checkboxes, function(checkbox) {
    checkbox.addEventListener('click', () => {
        // Обнуляется в случае, если фото в данный момент открыто и пользователь нажал на checkbox.
        current_active_element = null;

        if(checkbox.classList.contains("active_checkbox")) checkbox.classList.remove("active_checkbox")
        else checkbox.classList.add("active_checkbox");

        let searchTagList = [];
        let activeCheckboxes = document.querySelectorAll(".active_checkbox");
        for(let checkbox of activeCheckboxes) {
            searchTagList.push(checkbox.value);
        }
        searchImages(columns, images, searchTagList);
    });
});
