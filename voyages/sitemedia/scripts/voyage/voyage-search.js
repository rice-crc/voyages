var attr_selected_class = "attribute-selected";

$(document).ready(function() {
    /* Collapsible boxes */
    $(".box-header .box-button").click(function(ev){
		$(this).parent().parent().toggleClass("box-collapsed box-expanded");
	});

    /* Collapse same section search boxes when one expands */
    $(".box-header-head .box-button, .box-header-tail .box-button").click(function(ev){
        var curBox = $(this).parent().parent();
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

            $(".menu-popup-submenu-item[name='" + $(this).attr('name') + "']").addClass(attr_selected_class);

            $(".query-builder").append("<div class=\"side-box\"></div>");
            var $new_box = $(".query-builder").children().last()
            $new_box.load("/voyage/varbox/" + $(this).attr('name'), function() {
                    $new_box.children().first().text(var_full_name);
                    $(".query-builder").resize();


                    /* Add event handler for numeric fields */
                    if ($(".select_field:last").hasClass("newly_inserted")) {
                        $(".select_field:last").removeClass("newly_inserted");
                        $(".select_field:last").change(function() {
                            update_numeric_field($(this).parent().children().first().attr("id"), "range_field");
                        });
                    }

                    if ($(".date_field:last").hasClass("newly_inserted")) {
                        $(".date_field:last").removeClass("newly_inserted");
                        $(".date_field:last").change(function() {
                            update_numeric_field($(this).parent().children().first().attr("id"), "date_field_wrapper");
                        });

                        $(".month-list:last").children("span").click(function(ev) {

                            $(this).toggleClass("month-toggled month-untoggled");
                        });
                    }
                }
            );
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

function collapseCheckBoxes(elem_id, boxclassname) {
    $("#" + elem_id + " .query-select-selected-text").text("");
    var selectedItems = []

    $("#" + elem_id + " ." + boxclassname).each(function () {
        if ($(this).prop("checked")) {
            selectedItems.push($.trim($(this).parent().text()));
        }
    });
    if (selectedItems.length == 0) {
        $("#" + elem_id + " .query-select-selected-text").text("[nothing selected]");
    } else {
        $("#" + elem_id + " .query-select-selected-text").text(formatArray(selectedItems));
    }

    $("#" + elem_id).children(".query-select-initial").removeClass("hidden");
    $("#" + elem_id).children(".query-select-full").addClass("hidden");
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

function update_numeric_field(label, fieldname) {
    var $cur_select_elem = $("#" + label).parent();

    $cur_select_elem.children("." + fieldname).each(function() {
        if ($cur_select_elem.children("select").val() == 1) {
            /* Between = 1 */
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
           $(this).parent().parent().removeClass("hidden");
        });
    } else {
        $("#" + label + " .var-checkbox").each(function() {

           if ($(this).parent().text().toLowerCase().indexOf(text_to_search) >= 0) {
               $(this).parent().parent().removeClass("hidden");
           } else {
               $(this).parent().parent().addClass("hidden");
           }
        });
    }
}

function expandOrCollapse(input_id) {
    var $label_id = $("#" + input_id).parent();
    if ($label_id.prev().hasClass('query-builder-list-item-collapsed')) {
        /* Is already collapsed */
        $label_id.prev().toggleClass('query-builder-list-item-collapsed query-builder-list-item-expanded')
        $label_id.next().removeClass('hidden');
    } else {
        /* Is already expanded */
        $label_id.prev().toggleClass('query-builder-list-item-collapsed query-builder-list-item-expanded')
        $label_id.next().addClass('hidden');
    }
}

function click_select_checkbox(input_id, parent_id, hasChildren) {
    if ($("#" + input_id).prop('checked')) {
        /* Box became checked */
        /* Check parent if all siblings items are checked */
        if (parent_id != null) {
            var $children = $("#" + parent_id).parent().next().children("li").children("label");
            if ($children.children(".var-checkbox:checked").length
                == $children.children(".var-checkbox").length) {
                /* Highlight parent if all siblings are checked */
                $("#" + parent_id).prop('checked', true);

                /* Highlight the grandparent if all its children are checked */
                var $grandparent =  $("#" + parent_id).parent().parent().parent();
                var $parent_siblings = $grandparent.children("li").children("label");
                if ($parent_siblings.children(".var-checkbox:checked").length
                    == $parent_siblings.children(".var-checkbox").length) {
                     /* Highlight parent if all siblings are checked */
                    $grandparent.prev().children(".var-checkbox").prop('checked', true);
                }
            }
        }
        if (hasChildren) {
            /* Check all children */
            $children = $("#" + input_id).parent().next().children("li").children("label");
            $children.children(".var-checkbox").prop('checked', true);

            /* Check all grandchildren */
            $children.next().each(function() {
                $(this).children("li").children("label").children(".var-checkbox").prop('checked', true)
            });
        }
    } else {
        /* Box got unchecked so uncheck the parent*/
        if (parent_id != null) {
            $("#" + parent_id).prop('checked', false);

            /* Uncheck grandparent */
        }
        if (hasChildren) {
            /* Uncheck also all children */
            var $children = $("#" + input_id).parent().next().children("li").children("label");
            $children.children(".var-checkbox").prop('checked', false);

            /* Uncheck also all grandchildren */
            $children.next().each(function() {
                $(this).children("li").children("label").children(".var-checkbox").prop('checked', false);
            })
        }
    }
}

function filter_hierarchical_list(label) {
    var text_to_search = $("#" + label + " .quick-query-builder-text").val().toLowerCase();

    if (text_to_search == "") {
        /* Expand all items */
        $("#" + label + " ul").removeClass("hidden");
        $("#" + label + " li").removeClass("hidden");
    }
    $("#" + label + " .query-builder-list-item-collapsed").each(function() {
           $(this).toggleClass('query-builder-list-item-collapsed query-builder-list-item-expanded')
    });

    $("#" + label + " .checkbox-layer0").each(function() {
        var found = false;
        $(this).parent().next().children("li").each(function() {
            var foundInner = false;
            $(this).children("ul").children("li").each(function() {
                if ($(this).children("label").text().toLowerCase().indexOf(text_to_search) > 0) {
                    found = true;
                    foundInner = true;
                    $(this).removeClass("hidden");
                } else {
                    $(this).addClass("hidden");
                }
            });
            if (foundInner) {
                $(this).removeClass("hidden");
            } else {
                $(this).addClass("hidden");
            }
        });
        if (found) {
            $(this).parent().parent().removeClass("hidden");
        } else {
            $(this).parent().parent().addClass("hidden");
        }
    });
}



function formatArray(selectedItems) {
    /* Return a comma-separated list */
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