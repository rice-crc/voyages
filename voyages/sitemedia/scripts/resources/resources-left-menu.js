$(document).ready(function() {
    /* Collapsible boxes */
    $("div .box-button").click(function(ev){
	    $('#middle').toggleClass('row-expanded row-collapsed');
        $('#bottom').toggleClass('row-expanded row-collapsed');
    })
});
