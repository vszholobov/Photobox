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
        this.self.append(image);
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

        this.addEventListenerToImage(this.node);
    }

    hide() {
        this.node.classList.add("hidden");
    }

    show() {
        this.node.classList.remove("hidden");
    }

    addEventListenerToImage(node) {
        let self = this;
        let tagList = this.tagList;
        let description = this.description;
        let descriptionTextArea = document.getElementById("description_textarea");
        let tagsZone = document.getElementById("checkbox_container");

        node.addEventListener("click", function() {
            currentActiveElement = self;
            for(let i = 0; i < tagsZone.children.length; i++) {
                tagsZone.children[i].remove();
                i--;
            }
            for(let tag of tagList) {
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
            if(description.length) {
                descriptionTextArea.value = description;
            } else {
                descriptionTextArea.value = " ";
            }
        });
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

let images = [];

let userList = [];

let userAvatars = [];

let columns = [new Column("img_column1"),
               new Column("img_column2")];

let currentActiveElement = null;

let currentActiveUser = null;

let deletePhotoButton = document.getElementById("delete_photo");

let deleteUserButton = document.getElementById("delete_user");

deletePhotoButton.addEventListener("click", function() {
    if(currentActiveElement) {
        $.ajax({
            type: 'POST',
            url: '/ajax',
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify({"action": "adminDeleteUserPhoto", "photoId": currentActiveElement.id}),
            success: function(data) {
                alert("Фото успешно удалено.");
            },
            error: function() {
                reject(new Error("Произошла ошибка( Попробуйте перезагрузить страницу."));
            }
        });
    }
});

deleteUserButton.addEventListener("click", function() {
    if(currentActiveUser) {
        $.ajax({
            type: 'POST',
            url: '/ajax',
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify({"action": "adminDeleteUser", "userId": currentActiveUser.id}),
            success: function(data) {
                alert("Пользователь успешно удален.");
            },
            error: function() {
                reject(new Error("Произошла ошибка( Попробуйте перезагрузить страницу."));
            }
        });
    }
});

let promise = new Promise(function(resolve, reject) {
    $.ajax({
        type: 'POST',
        url: '/ajax',
        contentType: 'application/json',
        dataType: 'json',
        data: JSON.stringify({"action": "admin_init"}),
        success: function(data) {
            userList = data[0];
            userAvatars = data[1];
            resolve('result');
        },
        error: function() {
            reject(new Error("Произошла ошибка( Попробуйте перезагрузить страницу."));
        }
    });
});
promise.then(function(result) {
    let placeToPutUsers = document.getElementById("users_column");
    for(let i = 0; i < userList.length; i++) {
        let userDiv = document.createElement("div");
        userDiv.classList.add("user_div");

        let userImage = document.createElement("img");
        userImage.src = userAvatars[i];
        userImage.classList.add("user_avatar");

        let userName = document.createElement("p");
        userName.innerText = userList[i].username;
        userName.classList.add("user_name");

        userDiv.append(userImage);
        userDiv.append(userName);
        placeToPutUsers.append(userDiv);

        userDiv.addEventListener("click", function() {
            currentActiveUser = userList[i];
            currentActiveElement = null;
            if(images.length) {
                for(let image of images) {
                    image.node.remove();
                    columns.forEach(column => column.height = 0);
                }
                images = [];
            }
            alert(userList[i].username);
            $.ajax({
                type: 'POST',
                url: '/ajax',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify({"action": "adminGetUserPhotos", "user_id": userList[i].id}),
                success: function(data) {
                    initializePage(data, columns, images);
                },
                error: function() {
                    alert("Произошла ошибка( Попробуйте перезагрузить страницу.");
                }
            });
        });
    }
});










