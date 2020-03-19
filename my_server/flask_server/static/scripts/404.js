const shrek = document.getElementById("shrek");
let x = 0;
let timerId = setInterval(function() {
    x++;
    new_rotate = "rotate(" + x + "deg)"
    shrek.style.transform = new_rotate;
}, 25);