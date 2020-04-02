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
            let image = images[i];
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
            let image = images[i];

            let minHeight = 10000;
            let currentColumn = null;
            columns.forEach(column => (column.height < minHeight)? [minHeight, currentColumn] = [column.height, column]: null);

            currentColumn.addImage(images[i].node);

            currentColumn.changeHeight(images[i].htwRatio * columnWidth);
        }
    }
}

// Создаеи список тегов для поиска. Используется при вызове SearchImages.
function createSearchTagList() {
    // Обнуляется в случае, если фото в данный момент открыто и пользователь нажал на checkbox.
    current_active_element = null;

    let searchTagList = [];
    let activeCheckboxes = document.querySelectorAll(".active_checkbox");

    // Берет значение следующего за checkbox'ом span'а.
    for(let checkbox of activeCheckboxes) {
        searchTagList.push(checkbox.nextElementSibling.innerText);
    }

    return searchTagList;
}

// Добавляет обработчик на нажатие чекбоксов.
function addSearchListenerToCheckboxes(checkboxes) {
    [].forEach.call(checkboxes, function(checkbox) {
        checkbox.addEventListener('click', function() {
            if(checkbox.classList.contains("active_checkbox")) checkbox.classList.remove("active_checkbox")
            else checkbox.classList.add("active_checkbox");

            searchImages(columns, images, createSearchTagList());
        });
    });
}

// При нажатии на тег из области фотографии передвигает его на панель поиска и запускает поиск.
function moveTagToPanel(checkbox, columns, images) {
    // Создание списка тегов для проверки наличия нажатого тега в панели.
    let listOfCheckboxes = Array.from(document.querySelectorAll(".upload_checkbox"));
    listOfCheckboxes = listOfCheckboxes.filter(node => !node.classList.contains("photo_checkbox"));
    let listOfTags = listOfCheckboxes.map(checkbox => checkbox.nextElementSibling.innerText);
    let tagText = checkbox.nextElementSibling.innerText;

    if(!listOfTags.includes(tagText)) {
        // Копируем div с тегом, на который нажали
        let appendedTagContainer = checkbox.closest(".checkbox_div").cloneNode(true);
        // Добавляем его на панель поиска
        document.querySelector(".checkbox_container").append(appendedTagContainer);

        // Удаление класса photo_checkbox у нового тега в списке и добавление класса active_checkbox
        let listOfCheckboxes = Array.from(document.querySelectorAll(".photo_checkbox"));
        let currentCheckbox = listOfCheckboxes[listOfCheckboxes.length - 1];
        currentCheckbox.classList.remove("photo_checkbox");
        currentCheckbox.classList.add("active_checkbox");

        addSearchListenerToCheckboxes(new Array(currentCheckbox));
        searchImages(columns, images, createSearchTagList());
    } else {
        let currentPanelCheckbox = listOfCheckboxes[listOfTags.indexOf(tagText)];
        currentPanelCheckbox.classList.add("active_checkbox");
        currentPanelCheckbox.checked = true;

        // Запуск поиска
        searchImages(columns, images, createSearchTagList());
    }
}

// Создание зоны описания при раскрытии фотографии.
function createDescriptionDiv(image) {
    let descriptionDiv = document.createElement("div");
    descriptionDiv.classList.add("description_zone");

    // Создание области с фотографией пользователя, его именем и датой создания фотографии.
    let authorDiv = document.createElement("div");
    authorDiv.classList.add("top_div");

    let authorAvatar = document.createElement("img");
    authorAvatar.src = userList[image.userId - 1][1];
    authorAvatar.classList.add("author_avatar");
    authorDiv.append(authorAvatar);

    let authorDateAndNameDiv = document.createElement("div");
    authorDateAndNameDiv.classList.add("author_date_name");

    let authorNameSpan = document.createElement("p");
    authorNameSpan.innerText = userList[image.userId - 1][0];
    authorDateAndNameDiv.append(authorNameSpan);

    let imageCreationDate = document.createElement("p");
    imageCreationDate.innerText = image.creationDate;
    authorDateAndNameDiv.append(imageCreationDate);

    authorDiv.append(authorDateAndNameDiv);
    descriptionDiv.append(authorDiv);

    // Создание области с описанием фотографии
    let textDescriptionDiv = document.createElement("div");
    textDescriptionDiv.classList.add("text_description");
    textDescriptionDiv.classList.add("scroll");

    let description = document.createElement("p");
    description.innerText = image.description;
    textDescriptionDiv.append(description);

    descriptionDiv.append(textDescriptionDiv);

    // Создание области с тегами фотографии.
    let tagsDiv = document.createElement("div");
    tagsDiv.classList.add("tags_zone");
    tagsDiv.classList.add("scroll");

    // Вывод тегов по одному
    for(let tag of image.tagList) {
        let tagContainer = document.createElement("div");
        tagContainer.classList.add("aside_center");
        tagContainer.classList.add("checkbox_div");

        let tagLabel = document.createElement("label");

        let tagCheckbox = document.createElement("input");
        tagCheckbox.type = "checkbox";
        tagCheckbox.classList.add("upload_checkbox");
        tagCheckbox.classList.add("photo_checkbox");
        tagLabel.append(tagCheckbox);

        let tagSpan = document.createElement("span");
        tagSpan.classList.add("checkbox_span");
        tagSpan.innerText = tag;
        tagLabel.append(tagSpan);

        tagContainer.append(tagLabel);
        tagsDiv.append(tagContainer);
    }
    descriptionDiv.append(tagsDiv);

    return descriptionDiv;
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

// Список нужных полей пользователей(Имя пользователя и имя файла его аватара).
let userList = [];

// Хранит в себе объект текущего открытого div'a с изображением.
let current_active_element = null;

// Список объектов чекбоксов. Используются при поиске.
const checkboxes = document.getElementsByClassName("upload_checkbox");

// Promise на получение фотографий с сервера при открытии страницы
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
    // Создает фотографии на странице
    initializePage(imageList, columns, images);

    // Добавляет листенеры на чекбоксы. При нажатии запускается поиск.
    addSearchListenerToCheckboxes(checkboxes);
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

            // Создание зоны описания
            current_active_element.append(createDescriptionDiv(images[index]));

            [].forEach.call(document.querySelectorAll(".photo_checkbox"), function(checkbox) {
                checkbox.addEventListener('click', () => moveTagToPanel(checkbox, columns, images));
            });

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
