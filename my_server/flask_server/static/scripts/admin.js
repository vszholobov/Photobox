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
        //let divImageContainer = document.createElement("div");

        //divImageContainer.classList.add("img_container");
        //divImageContainer.append(image);

        this.self.append(image);
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

let images = [];

let userList = [];

let userAvatars = [];

let columns = [new Column("img_column1"),
               new Column("img_column2")]

let password = prompt("Введите пароль еще раз", "");
if(password == "1") {
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
                if(images.length) {
                    images = [];
                    // !!!!!!!!!!!!!!!!!!
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
}









