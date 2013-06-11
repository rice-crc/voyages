var top_selected_class = "top-bar-menu-selected";

$(document).ready(function() {
	var href = document.location.href;
	var elem = href.split("=");
	var maxIdx = elem.length - 1;
	var currentid = elem[maxIdx];
	
	/* Update page title */
	$("#help-section-title").text(document.title);
	
	/* Update highlighting for section name */
	var str = location.href.toLowerCase();
	
	$(".top-bar-menu > ul > li > a").removeClass(top_selected_class);
	$(".top-bar-menu > ul > li > a").each(function() {
		if (str.indexOf(this.href.toLowerCase()) > -1) {
		 	$(this).addClass(top_selected_class);
		}
	 });
});

/* Support function for sitemap */
function openPage(url) {
	if (window.opener)
		window.opener.location.href = url;
	else
		window.open(url);
}
