var attr_selected_class = "attribute-selected";

$(document).ready(function() {
    /* Handler for changing tabs */
    $(".tab-menu-item").click(function(){
        submitWithValue($(this).attr('id'));
        return false;
	});

    /* Collapsible boxes */
    $(".box-header .box-button").click(function(){
		$(this).parent().parent().toggleClass("box-collapsed box-expanded");
	});

    $(".collapseCheckBoxButton").trigger('click');

    /* Update text content for places */
    $(".place_collapse_button").trigger('click');

    /* Collapse same section search boxes when one expands */
    $(".box-header-head .box-button, .box-header-tail .box-button").click(function(ev){
        var curBox = $(this).parent().parent();
        var $list_exp = curBox.parent().children("input");
        $list_exp.prop("disabled", !$list_exp.prop("disabled"));

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
    $(".query-builder-label").each(function() {
        var tmpVar = $(this).attr("id");

    });

    /* Update numeric field */
    $(".select_field").each(function() {
        update_numeric_field($(this).parent().children().first().attr("id"), "range_field");
    });

    $(".select_field").change(function() {
        update_numeric_field($(this).parent().children().first().attr("id"), "range_field");
    });



    /* Update date field */
    $(".date_field").each(function() {
         update_numeric_field($(this).parent().children().first().attr("id"), "date_field_wrapper");
    });
    $(".date_field").change(function() {
         update_numeric_field($(this).parent().children().first().attr("id"), "date_field_wrapper");
    });

    $(".month-list").children("span").click(function(ev) {
        $(this).toggleClass("month-toggled month-untoggled");

        if ($(this).children("input").prop('disabled')) {
            $(this).children("input").prop('disabled', false);
        } else{
            $(this).children("input").prop('disabled', true);
        }
    });

    $(".menu-popup-submenu-item").click(function(ev){
        if (!($(this).hasClass(attr_selected_class))) {
        $(".query-builder-label").each(function(){
            });
	    var varname = $(this).attr('name');
	    show_search_form_by_name(varname);
            return true;
        }
	});

    /* Tool tip for sources */
    /*$(".source_entry").qtip({
        content: "Tooltip here"
    }); */

    if ($(".search-panel").children().length > 0) {
        $('.source_entry').qtip({
        content: {
           text: function (api) {
               return $(this).next().html();
           }
        },
        position: {
            my: 'top left',
            target: 'mouse',
            viewport: $(window), // Keep it on-screen at all times if possible
            adjust: {
                x: -300, y: 10
            }
        },
        delay: 0,
        });
    }

    $(".close-link-box").click(endBlackout); // close if close btn clicked

    /* Go through search boxes and see which ones should be displayed and in what order */
    var hidden_search_forms = $("#search_form_hide").children().each(function() {
	if($(this).find("input[id$='-is_shown_field']").attr('value')) {
	    var varname = $(this).find("[id$='-var_name_field']").val();
	    show_search_form_noedit(varname);
	}
    });
    sort_search_forms();
});

function sort_search_forms() {
    var shown_search_forms = $("#search_form_show").children();
    for (var i = 0; i < shown_search_forms.length; i++) {
	$("#search_form_show").find("[id$='-is_shown_field'][value='" + i + "']").parent().appendTo("#search_form_show");
    }
}

function show_search_form_noedit(varname) {
    $('#search_form_box_'+varname).appendTo("#search_form_show");
    $(".menu-popup-submenu-item[name='" + varname + "']").addClass(attr_selected_class);
}

function show_search_form_by_name(varname) {
    $('#search_form_box_'+varname).appendTo("#search_form_show");
    $(".menu-popup-submenu-item[name='" + varname + "']").addClass(attr_selected_class);
    $("#id_"+varname+"-is_shown_field").val($("#search_form_box_"+varname).index());
    
}

/* Renumber search boxes when they are moved */
function renumber_search_boxes() {
    var search_form_list = $("#search_form_show").children().each(function () {
	$(this).find("[id$='-is_shown_field']").val($(this).index())
    });
}

/* Support functions */
function set_elem(elemname, value) {
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
    renumber_search_boxes();
}

function move_box_down(label) {
    var $cur_box_parent = $("#" + label).parent();
    var $next_parent_sibling = $cur_box_parent.next();

    if (($next_parent_sibling.length) != 0 ) {
        /* Has a sibling to swap */
        $cur_box_parent.before($next_parent_sibling);
    }
    renumber_search_boxes();
}

function delete_box(label, varname) {
    $(".menu-popup-submenu-item[name='" + varname + "']").removeClass(attr_selected_class);
    $('#search_form_box_'+varname).appendTo("#search_form_hide");
    $("#id_"+varname+"-is_shown_field").removeAttr('value');
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
        return;
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
                    $(this).parent().removeClass("hidden");
                } else {
                    $(this).addClass("hidden");
                }
            });
            if (foundInner) {
                $(this).removeClass("hidden");
                $(this).parent().removeClass("hidden");
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

function config_change_group(group_id) {
    /* Configure to display only this value */

    /* Deselect current values */
    $(".voyage_config_all_list option:selected").prop('selected', false);
    $(".voyage_config_all_list select").addClass("hidden");
    $("#" + group_id).removeClass("hidden");
}

function getxlsDownload(pageNum) {
    $('#form').append("<input id='xls_download_submit_val' type='hidden' name='submitVal' value='download_xls_current_page' />");
    $("#form").submit();
    $('#form').append("<input id='xls_download_page_num' type='hidden' name='pageNum' value='" + pageNum + "' />");
    $("#form").submit();
    $('#xls_download_submit_val').remove()
    $('#xls_download_page_num').remove()
    return false;
}

function submitWithValue(submitVal) {
    $('#form').append("<input type='hidden' name='submitVal' value='" + submitVal + "' />");
    $("#form").submit();
    return false;
}

function applyConfig() {
    /* Select all options so the form submit all values */
    $('#configure_visibleAttributes option').prop('selected', true);
    return submitWithValue('applyConfig');
}

/* Add variables to the display list */
function add_var_to_display() {
    var $newly_selected_vals = $(".voyage_config_all_list option:selected");

    /* List currently selected */
    var cur_selected_text = []

    var $currently_selected = $("#configure_visibleAttributes option");
    $currently_selected.each(function() {
       cur_selected_text.push($(this).val());
    });

    $newly_selected_vals.each(function() {
        /* Check if the current variable is already in the list*/
        if (cur_selected_text.length == 0 ||
            $.inArray($(this).val(), cur_selected_text) == -1) {
            $("#configure_visibleAttributes option:last").parent().append($(this));
        }
    });
}

function remove_from_display() {
    $("#configure_visibleAttributes option:selected").remove();
}

/* Move variables up and down in the display column */
function move_var(direction) {
    var $selected_elem = $("#configure_visibleAttributes option:selected");
    if (direction == 'up') {
        $selected_elem.first().prev().before($selected_elem);
    } else {
        $selected_elem.last().next().after($selected_elem);
    }
}

function retrieve_page(page_elem) {
    /* Enable the button with desired page to be submitted */
    $('#' + page_elem).prop('disabled', false);
    submitWithValue('retrieve_page');
    return false;
}


function formatArray(selectedItems) {
    /* Return a comma-separated list */
    var i;
    var result = "";

    for(i = 0; i < selectedItems.length - 1; i++) {
        result += selectedItems[i] + ", ";
    }
    result += selectedItems[i];

    if (result.length >= 70) {
        result = result.substr(0, 69) + "...";
    }
    return result;
}

function endBlackout(){
    $(".blackout").css("display", "none");
    $(".msgbox").css("display", "none");
}

/* This is the function that closes the pop-up */
function strtBlackout(){
    $(".msgbox").css("display", "block");
    $(".blackout").css("display", "block");
}
