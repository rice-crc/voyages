$(document).ready(function() {
	/* Let the link on sitemap page opens a new page in the parent window */
	$("#toplinks a").click(function(ev) {
		ev.preventDefault();
		openPage($(this).attr("href"));
	});
});