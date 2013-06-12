$(document).ready(function() {
	var top_selected_class = "top-bar-menu-selected";
	var anchor_link_selector = ".top-bar-menu > ul > li > a";
	var pagetitle_id = "help-section-title";

	/* Update page title */
	$("#" + pagetitle_id).text(document.title);
	
	/* Update highlighting for the current page */
	var str = location.href.toLowerCase();
	$(anchor_link_selector).removeClass(top_selected_class);
	$(anchor_link_selector).each(function() {
		if (str.indexOf(this.href.toLowerCase()) > -1) {
		 	$(this).addClass(top_selected_class);
		}
	 });
});

/* Support function: open the given url in the parent window */
function openPage(url) {
	if (window.opener)
		window.opener.location.href = url;
	else
		window.open(url);
}
