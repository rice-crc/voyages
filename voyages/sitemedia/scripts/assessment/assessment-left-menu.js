$(document).ready(function() {
    $("tr .checkbox-list-item-0-active").hover(function(ev){
        var a = $(this).children().eq(0).children().first()
        $(this).children(".menu-popup-submenu-frame").removeClass("hidden");
    });
});