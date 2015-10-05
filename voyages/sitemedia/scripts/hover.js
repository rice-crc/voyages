$(document).ready(function() {
	$("#toplinks > li").hover(function() {
		$("#toplinks > li > a").not(this).parent().removeClass('hover');
		
		$(this).toggleClass("hover hovered");
		return true;
	}, function() {
		$("#toplinks >li").removeClass("hover hovered");
	});
});
