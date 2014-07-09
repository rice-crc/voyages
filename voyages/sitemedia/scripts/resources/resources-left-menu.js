$(document).ready(function() {
    /* Collapsible boxes */
    $("div .box-button, div .box-button-collapsed").click(function(ev){
	    var curBox = $(this).parent().parent().parent().parent().parent().parent().parent();
        var children = curBox.children();
        if ($(this).hasClass("box-button")){
            expandRow(curBox, $(this))
            $(this).toggleClass("box-button box-button-collapsed");
        } else{
            collapseRow(curBox, $(this))
            $(this).toggleClass("box-button-collapsed box-button");
        }
    })

    $("div.lookup-checkbox-list-item-collapsed").click(function(ev){
        var a = 4;
        var b = $(this).parent().children();
    })
});

function collapseRow(table, button){
    table.children().each(function( index ){
        if ($(this).hasClass("row-collapsed")){
            $(this).toggleClass("row-collapsed row");
        }
    });
    var a = $(button).parent().parent().parent().parent().parent().parent().children();
    if (a.hasClass("box-set-upper-row-bottom-left-collapsed")){
        a.first().removeClass('box-set-upper-row-bottom-left-collapsed').addClass('box-set-upper-row-bottom-left')
        a.eq(1).removeClass('box-set-upper-row-bottom-middle-collapsed').addClass('box-set-upper-row-bottom-middle')
        a.eq(2).removeClass('box-set-upper-row-bottom-right-collapsed').addClass('box-set-upper-row-bottom-right')
    }
    if (a.hasClass("box-upper-row-left-collapsed")){
        a.first().removeClass('box-upper-row-left-collapsed').addClass('box-upper-row-left')
        a.eq(1).removeClass('box-upper-row-middle-collapsed').addClass('box-upper-row-middle')
        a.eq(2).removeClass('box-upper-row-right-collapsed').addClass('box-upper-row-right')
    }

}

function expandRow(table, button){
    table.children().each(function( index ){
        if ($(this).hasClass("row")){
            $(this).toggleClass("row row-collapsed");
        }
    });
    var a = $(button).parent().parent().parent().parent().parent().parent().children();
    if (a.hasClass("box-set-upper-row-bottom-left")){
        a.first().removeClass('box-set-upper-row-bottom-left').addClass('box-set-upper-row-bottom-left-collapsed')
        a.eq(1).removeClass('box-set-upper-row-bottom-middle').addClass('box-set-upper-row-bottom-middle-collapsed')
        a.eq(2).removeClass('box-set-upper-row-bottom-right').addClass('box-set-upper-row-bottom-right-collapsed')
    }
    if (a.hasClass("box-upper-row-left")){
        a.first().removeClass('box-upper-row-left').addClass('box-upper-row-left-collapsed')
        a.eq(1).removeClass('box-upper-row-middle').addClass('box-upper-row-middle-collapsed')
        a.eq(2).removeClass('box-upper-row-right').addClass('box-upper-row-right-collapsed')
    }
}

function filter_edit_list() {
    var text_to_search = $("#query-text-origin").val()
    var items = $('#origin_list').children()

    if (text_to_search == "") {
        items.each(function( index ) {
           $(this).removeClass("hidden");
        });
    } else {
        items.each(function( index ) {
            if ($(this).children().eq(2).text().toLowerCase().indexOf(text_to_search) >= 0) {
                $(this).removeClass("hidden");
            } else {
                $(this).addClass("hidden");
            }
        });
    }
}

function expandable_embarkation(div, id){
    $(div).toggleClass("lookup-checkbox-list-item-collapsed lookup-checkbox-list-item-expanded");
    var a = $(div).parent().parent().parent().find("#tr_" + id + "_child");
    if (a.css('display') == 'none'){
        a.removeAttr('style');
    } else{
        a.css({ 'display': "none" });
    }


    return false;
}

function embarkation_choices(input, id){
    var a = id;
    var regex = new RegExp(/_/g);
    var count = id.toString().match(regex);

    if ($(input).prop('checked')){
        if (count == null) {
            /* clicked on broad region */
            /* Get parent of the entire table */
            var par = $(input).parents().eq(5);

            /* Get all children (Ports) and mark them */
            var children_boxes = "checkbox_" + a + "_";
            $(par).find("input[name^=" + children_boxes.toString() + "]").prop("checked", true);

        } else if (count.length == 1){
            /* Clicked on region */
            /* Get parent of the entire table */
            var par = $(input).parents().eq(8);

            /* Get parent (broad region) of this region and mark it */
            regex = new RegExp(/[0-9]+/g);
            var broad_region = a.toString().match(regex)[0];
            $(par).find("#tr_" + broad_region).children().eq(1).children().eq(0).prop("checked", true);

            /* Get all children (Ports) and mark them */
            var children_boxes = "checkbox_" + a + "_";
            $(par).find("input[name^=" + children_boxes.toString() + "]").prop("checked", true);
        }
        else{
            /* Clicked on port */
            /* Get parent of the entire table */
            var par = $(input).parents().eq(10);

            /* Get parent (region) and grandparent (broad region) of port */
            regex = new RegExp(/[0-9]+/g);
            var region = a.toString().match(regex)[0];
            regex = new RegExp(/[0-9]+_[0-9]+/g);
            var broad_region = a.toString().match(regex)[0];

            /* Set them as marked */
            $(par).find("#tr_" + region).children().eq(1).children().eq(0).prop("checked", true);
            $(par).find("#tr_" + broad_region).children().eq(1).children().eq(0).prop("checked", true);
        }
    } else{
        if (count == null){
            /* clicked on broad region */
            /* Get parent of the entire table */
            var par = $(input).parents().eq(5);

            /* Get all children (Ports) and unmark them */
            var children_boxes = "checkbox_" + a + "_";
            $(par).find("input[name^=" + children_boxes.toString() + "]").prop("checked", false);
        } else if (count.length == 1){
            /* Clicked on region */
            /* Get parent of the entire table */
            var par = $(input).parents().eq(10);

            /* Get parent (broad region) of this region */
            regex = new RegExp(/[0-9]+/g);
            var broad_region = a.toString().match(regex)[0];

            /* Get all children (Ports) and unmark them */
            var children_boxes = "checkbox_" + a + "_";
            $(par).find("input[name^=" + children_boxes.toString() + "]").prop("checked", false);

            /* Get all neighbors of region */
            regex = new RegExp(/[0-9]+_/g);
            var neighbors = "checkbox_" + a.toString().match(regex)[0];
            var broad_region_all_children = $(par).find("input[name^=" + neighbors.toString() + "]")

            /* Count how many of regions are still checked */
            var count_checked = 0;
            regex = new RegExp(/_/g);
            broad_region_all_children.each(function( index ){
                var name = $(this).val();
                count = name.toString().match(regex).length;
                if (count == 1 && $(this).prop('checked')){
                    count_checked++;
                }
            })

            if (count_checked == 0){
                /* if no more regions checked, uncheck the broad region */
                $(par).find("input[name^=checkbox_" + broad_region.toString() + "]").prop("checked", false);
            }
        } else{
            /* Clicked on port */
            /* Get parent of the entire table */
            var par = $(input).parents().eq(10);

            /* Get parent (region) id and grandparent (broad region) id of this port */
            regex = new RegExp(/[0-9]+_[0-9]+/g);
            var region = a.toString().match(regex)[0];
            regex = new RegExp(/[0-9]+/g);
            var broad_region = a.toString().match(regex)[0];

            /* Get all neighbors of place */
            regex = new RegExp(/[0-9]+_[0-9]+_/g);
            var neighbors = "checkbox_" + a.toString().match(regex)[0];
            var region_all_children = $(par).find("input[name^=" + neighbors.toString() + "]")

            /* Count how many of regions are still checked */
            var count_checked = 0;
            regex = new RegExp(/_/g);
            region_all_children.each(function( index ){
                var name = $(this).val();
                count = name.toString().match(regex).length;
                if (count == 2 && $(this).prop('checked')){
                    count_checked++;
                }
            })

            if (count_checked == 0){
                /* if no more regions checked, uncheck the broad region */
                $(par).find("input[name^=checkbox_" + region.toString() + "]").prop("checked", false);

                /* Check regions as well */
                /* Get all neighbors of region */
                regex = new RegExp(/[0-9]+_/g);
                var neighbors = "checkbox_" + a.toString().match(regex)[0];
                var broad_region_all_children = $(par).find("input[name^=" + neighbors.toString() + "]")

                /* Count how many of regions are still checked */
                count_checked = 0;
                regex = new RegExp(/_/g);
                broad_region_all_children.each(function( index ){
                    var name = $(this).val();
                    count = name.toString().match(regex).length;
                    if (count == 1 && $(this).prop('checked')){
                        count_checked++;
                    }
                })

                if (count_checked == 0){
                    /* if no more regions checked, uncheck the broad region */
                    $(par).find("input[name^=checkbox_" + broad_region.toString() + "]").prop("checked", false);
                }
            }

        }
    }
    return false;
}

function mark_all_children(input, id){


    return false;
}