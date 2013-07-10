$(document).ready(function() {

    /* Collapsible boxes */
    $(".box-button").click(function(ev){
		$(this).parent().parent().toggleClass("box-collapsed box-expanded");
	});


    /* Fly-out menus */
    $(".menu-popup-item-main, .menu-popup-item-main-last").hover(function() {
		$(this).children(".menu-popup-submenu-frame").removeClass("hidden");
		return true;
	}, function() {
        $(this).children(".menu-popup-submenu-frame").addClass("hidden");
	});


});
