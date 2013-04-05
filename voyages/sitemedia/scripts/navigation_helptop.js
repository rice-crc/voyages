

$(document).ready(function() {
	var href = document.location.href;
	var elem = href.split("=");
	var maxIdx = elem.length - 1;
	var currentid = elem[maxIdx];
	
	$(".top-bar-menu > ul > li > a").each(function() {
		/* load the page on click */
		$("#" + this.id).click(function(ev) {
			ev.preventDefault();
			currentid = this.id;
			updatepage();
		});
	});
	if (currentid.charAt(currentid.length - 1) == "#") {
		currentid = currentid.substring(0, currentid.length);
	}
	
	updatepage();

	function updatepage() {
		$("#main-content").load("page_" + currentid + ".html");
		document.title = $("#" + currentid).text();
		$("#help-section-title").text(document.title);
		$(".top-bar-menu > ul > li > a").removeClass("top-bar-menu-selected");
		$("#" + currentid).addClass("top-bar-menu-selected");
	}
});

/* Support function for sitemap */
function openPage(url) {
	if (window.opener)
		window.opener.location.href = url;
	else
		window.open(url);
}
