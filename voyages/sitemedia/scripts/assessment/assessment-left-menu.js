$(document).ready(function() {
    $("tr .checkbox-list-item-0").hover(
        function() {
            $(this).toggleClass("checkbox-list-item-0 checkbox-list-item-0-active");
            $(this).children().eq(2).children().show()
        }, function() {
            $(this).toggleClass("checkbox-list-item-0-active checkbox-list-item-0");
            $(this).children().eq(2).children().hide()
        }
    );

//    $("tr .checkbox-list-item-1").hover(
//        function() {
//            $(this).toggleClass("checkbox-list-item-0 checkbox-list-item-0-active");
//            $(this).children().eq(2).children().show()
//        }, function() {
//            $(this).toggleClass("checkbox-list-item-0-active checkbox-list-item-0");
//            $(this).children().eq(2).children().hide()
//        }
//    );
});