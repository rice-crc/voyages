
$(document).ready(function () {
            $("#toplinks > li").hover(function () {
                $("#toplinks > li > a").not(this).parent().removeClass('hover');
                $(this).toggleClass('hover');
                return true;
            }, function () {
                $("#toplinks >li").removeClass('hover');
            });
        }
     	);