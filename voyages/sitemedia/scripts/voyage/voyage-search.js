$(document).ready(function() {
    var attr_selected_class = "attribute-selected";

    /* Collapsible boxes */
    $(".box-header .box-button").click(function(ev){
		$(this).parent().parent().toggleClass("box-collapsed box-expanded");
	});

    /* Collapse same section search boxes when one expands */
    $(".box-header-head .box-button, .box-header-tail .box-button").click(function(ev){
        curBox = $(this).parent().parent();
		curBox.toggleClass("box-collapsed box-expanded");
        if (curBox.hasClass("box-expanded")) {
            curBox.parent().children().not(curBox).removeClass("box-expanded");
            curBox.parent().children().not(curBox).addClass("box-collapsed");
        }
	});

    /* Fly-out menus */
    $(".menu-popup-item-main, .menu-popup-item-main-last").hover(function() {
		$(this).children(".menu-popup-submenu-frame").removeClass("hidden");
		return true;
	}, function() {
        $(this).children(".menu-popup-submenu-frame").addClass("hidden");
	});

    /* Event handler to highlight adding variables */

    $(".menu-popup-submenu-item").click(function(ev){
        if ($(this).hasClass(attr_selected_class)) {
            /* Deselect the attribute ? */
        } else {
            var var_full_name = $.trim($(this).text());
            $(this).addClass(attr_selected_class);

            $(".query-builder").append("<div class=\"side-box\"></div>");
            var new_box = $(".query-builder").children().last()
            $(".query-builder").children().last().load("/voyage/varbox/" + this.id);
            $(".query-builder").resize();

            /* Attach event handlers for the box */
            /* To be updated */
        }
	});
});

/* Support functions */
function setelem(elemname, value) {
    /* Elements in voyage/search_left_menu.html */
    $("#" + elemname).val(value);
}

function add_variables(elem) {
    animateAttribute(this , function() {
        document.forms['form'].elements['form:attr_selected'].value = 'voyageid';
        document.forms['form'].submit();
        return false;
    })
}