var attr_selected_class = "attribute-selected";

$(document).ready(function() {
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
    $("#" + elem_id + " .var-checkbox").prop('checked', true);
}

function uncheckAllBoxes(elem_id) {
    $("#" + elem_id + " .var-checkbox").prop('checked', false);
}

function collapseCheckBoxes(elem_id) {
    $("#" + elem_id + " .query-select-selected-text").text("");
    var selectedItems = []

    $("#" + elem_id + " .var-checkbox").each(function () {
        if ($(this).prop("checked")) {
            selectedItems.push($(this).attr('value'));
        }
    });
    if (selectedItems.length == 0) {
        $("#" + elem_id + " .query-select-selected-text").text("[nothing selected]");
    } else {
        $("#" + elem_id + " .query-select-selected-text").text(formatArray(selectedItems));
    }

    $("#" + elem_id).children(".query-select-initial").removeClass("hidden");
    $("#" + elem_id).children(".query-select-full").addClass("hidden");

    function formatArray(selectedItems) {
        var i;
        var result = ""

        for(i = 0; i < selectedItems.length - 1; i++) {
            result += selectedItems[i] + ", ";
        }
        result += selectedItems[i];

        if (result.length >= 70) {
            result = result.substr(0, 69) + "...";
        }

        return result;
    }
}

function move_box_up(label) {
    var $cur_box_parent = $("#" + label).parent();
    var $prev_parent_sibling = $cur_box_parent.prev();

    if (($prev_parent_sibling.length) != 0 ) {
        /* Has a sibling to swap */
        $cur_box_parent.after($prev_parent_sibling);
    }
}

function move_box_down(label) {
    var $cur_box_parent = $("#" + label).parent();
    var $next_parent_sibling = $cur_box_parent.next();

    if (($next_parent_sibling.length) != 0 ) {
        /* Has a sibling to swap */
        $cur_box_parent.before($next_parent_sibling);
    }
}

function delete_box(label, varname) {
    $("#" + varname).removeClass(attr_selected_class);
    $("#" + label).parent().remove();
}

function update_numeric_field(label) {
    var $cur_select_elem = $("#" + label);

    $cur_select_elem.parent().children(".range_field").each(function() {
        if ($cur_select_elem.val() == "between") {
            if ($(this).hasClass('between_field')) {
                $(this).removeClass('hidden');
            } else {
                $(this).addClass('hidden');
            }
        } else {
            if ($(this).hasClass('threshold_field')) {
                $(this).removeClass('hidden');
            } else {
                $(this).addClass('hidden');
            }
        }
    });
}

function filter_edit_list(label) {
    var text_to_search = $("#" + label + " .quick-query-builder-text").val().toLowerCase();

    if (text_to_search == "") {
        $("#" + label + " .var-checkbox").each(function() {
           $(this).parent().removeClass("hidden");
        });
    } else {
        $("#" + label + " .var-checkbox").each(function() {
           if ($(this).val().toLowerCase().indexOf(text_to_search) >= 0) {
               $(this).parent().removeClass("hidden");
           } else {
               $(this).parent().addClass("hidden");
           }
        });
    }
}