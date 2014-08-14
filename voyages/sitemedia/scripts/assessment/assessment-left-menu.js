$(document).ready(function() {
    $("tr .checkbox-list-item-0").hover(
        function() {
            /* If len == 2, it's region highlighting */
            if ($(this).children().length == 2){
                $(this).toggleClass("checkbox-list-item-0 checkbox-list-item-0-active");
            }
            /* If len > 0, it's area highlighting */
            else if ($(this).children().eq(2).children().length > 0) {
                $(this).toggleClass("checkbox-list-item-0 checkbox-list-item-0-active");
                $(this).children().eq(2).children().show();
            }
        }, function() {
            if ($(this).children().length == 2){
                $(this).toggleClass("checkbox-list-item-0-active checkbox-list-item-0");
            }
            if ($(this).children().eq(2).children().length > 0) {
                $(this).toggleClass("checkbox-list-item-0-active checkbox-list-item-0");
                $(this).children().eq(2).children().hide();
            }
        }
    );

//    $("tr .checkbox-list-item-1").hover(
//        function() {
//            $(this).toggleClass("checkbox-list-item-1 checkbox-list-item-1-active");
//            $(this).children().eq(2).children().show();
//        }, function() {
//            $(this).toggleClass("checkbox-list-item-1-active checkbox-list-item-1");
//            $(this).children().eq(2).children().hide();
//        }
//    );
});

function regionClick(clicked_input){
    /* Uncheck parent (area) input) */
    var area_parent = $(clicked_input).parents().eq(6);
    $(area_parent).find("input[name^=area-button-]").prop("checked", false);

    return false;
}

function areaClick(clicked_input){
    var area_parent = $(clicked_input).parents().eq(2);
    if ($(clicked_input).prop('checked')){
        /* Check all children */
        $(area_parent).find("input[name^=region-button-]").prop("checked", true);
    } else {
        /* Uncheck all children */
        $(area_parent).find("input[name^=region-button-]").prop("checked", false);
    }

    return false;
}