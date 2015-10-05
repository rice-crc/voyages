$(document).ready(function() {
	/* Navigation for demos */
	$(".demo-links > ul > li > a").click(function(evt) {
		evt.preventDefault();
		$("#demos-inner-content").load("page_" + $(this).parent().attr("id"));
		$(".demo-links > ul > li > a").removeClass("demo-link-active");
		$(this).addClass("demo-link-active");
	});

	/* Default loading */
	$(".demo-links > ul > li > a").first().addClass("demo-link-active");
	$("#demos-inner-content").load("page_" + $(".demo-links > ul > li").first().attr("id"));
});
