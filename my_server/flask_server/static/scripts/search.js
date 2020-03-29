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
    }

    hide() {
        this.node.classList.add("hidden");
    }

    show() {
        this.node.classList.remove("hidden");
    }
}

function initializePage(imageList, columns, images, searchTagList=null) {
    const columnWidth = columns[0].self.offsetWidth;
    columns.forEach(column => column.height = 0)
    if(!searchTagList) {
        for(let i = 0; i < imageList.length; i++) {
            let minHeight = 10000;
            let currentColumn = null;
            columns.forEach(column => (column.height < minHeight)? [minHeight, currentColumn] = [column.height, column]: null);

            images.push(new Image(imageList[i], imageList[i]));
            currentColumn.addImage(images[i].node);

            currentColumn.changeHeight(imageList[i].htwRatio * columnWidth);
        }
    } else {
        if(searchTagList.length) {
            images.forEach(image => image.node.remove())
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
}

let promise = new Promise(function(resolve, reject) {
    $.ajax({
        type: 'POST',
        url: '/ajax',
        success: function(data) {
            imageList = data;
            resolve('result');
        },
        error: function() {
            reject(new Error("Произошла ошибка( Попробуйте перезагрузить страницу."));
        }
    })
})
promise.catch(error => alert(error));
promise.then(
    result => initializePage(imageList, columns, images)
);

let columns = [new Column("img_column1"),
               new Column("img_column2"),
               new Column("img_column3"),
               new Column("img_column4")];
let images = [];
const checkboxes = document.getElementsByClassName("upload_checkbox");
const searchButton = document.getElementById("search_button");

[].forEach.call(checkboxes, function(checkbox) {
    checkbox.addEventListener('click', () => {
        if(checkbox.classList.contains("active_checkbox")) checkbox.classList.remove("active_checkbox")
        else checkbox.classList.add("active_checkbox");
        let searchTagList = [];
        let activeCheckboxes = document.querySelectorAll(".active_checkbox");
        for(let checkbox of activeCheckboxes) {
            searchTagList.push(checkbox.value);
        }
        initializePage(imageList, columns, images, searchTagList);
    });
});
