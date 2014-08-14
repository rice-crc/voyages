$(document).ready(function() {
    $("tr .checkbox-list-item-0").hover(
        function() {
            if ($(this).children().eq(2).children().length > 0) {
                $(this).toggleClass("checkbox-list-item-0 checkbox-list-item-0-active");
                $(this).children().eq(2).children().show();
            }
        }, function() {
            if ($(this).children().eq(2).children().length > 0) {
                $(this).toggleClass("checkbox-list-item-0-active checkbox-list-item-0");
                $(this).children().eq(2).children().hide();
            }
        }
    );
});