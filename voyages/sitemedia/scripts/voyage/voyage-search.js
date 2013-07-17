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
            var $new_box = $(".query-builder").children().last()
            $new_box.load("/voyage/varbox/" + this.id, function() {
                    $new_box.children().first().text(var_full_name);
                    $(".query-builder").resize();
                }
            );
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

function expandChoices(elem_id) {
    $("#" + elem_id).children(".query-select-initial").addClass("hidden");
    $("#" + elem_id).children(".query-select-full").removeClass("hidden");
}

function checkAllBoxes(elem_id) {
    $("#" + elem_id).children(".query-select-full .query-builder-edit-list").attr('checked', 'checked');
}