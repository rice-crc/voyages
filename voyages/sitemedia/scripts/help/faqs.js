$(document).ready(function() {
	$(".faq-answer a").click(function(ev) {
		if (this.href.indexOf("/help/help?section=") == -1 && (this.href).indexOf(window.location.hostname) >= 0) {
			/* Website internal links open page in the parent window
			 * except for Help pages open in the same window */
			ev.preventDefault();
			openPage($(this).attr("href"));
		}
	});
}); 