const blocks = document.getElementsByClassName("img");
const close_buttons = document.querySelectorAll(".img_container .close");
let current_active_element;

[].forEach.call(blocks, function(item) {
    item.addEventListener('click', () => {
        if(current_active_element) {
            current_active_element.parentNode.classList.remove('active_container');
        }
        item.parentNode.classList.add('active_container');
        current_active_element = item;
    });
});
[].forEach.call(close_buttons, function(item) {
    item.addEventListener('click', () => {
        document.querySelector(".active_container").classList.remove("active_container");
    });
});