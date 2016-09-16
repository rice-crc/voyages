function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            var csrftoken = Cookies.get('csrftoken');
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function maximizeContent(hideLeftMenu) {
    var $leftMenu = $('#left-menu');
    var occupiedWidth = 40 + $leftMenu.width();
    if (hideLeftMenu) {
        occupiedWidth = 20;
        $leftMenu.hide();
    }
    $("#center-content").css('width', 'calc(100% - ' + occupiedWidth + 'px)');
}