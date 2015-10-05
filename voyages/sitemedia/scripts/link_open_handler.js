$(document).ready(function() {
	$("a").click(function(ev) {
		if (this.href.indexOf(".pdf") > -1 || this.href.indexOf(".ppt") > -1) {
			/* Website internal links open page in the parent window
			 * except for Help pages open in the same window */
			ev.preventDefault();
			window.open($(this).attr("href"));
		}
	});
}); 