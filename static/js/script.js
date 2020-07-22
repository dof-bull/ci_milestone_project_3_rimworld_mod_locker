$(document).ready(function () {
    $('.collapsible').collapsible();
    $('select').material_select();
    $(".button-collapse").sideNav();
});

//----------Stops the selector needing to be clicked twice. Bug Fix by Simon Castagna----------

$(document).on('mousedown', '#picker-input', function (event) {
    event.preventDefault();
});
$(document).on('change select', (e) => {
    $('select').material_select();
});