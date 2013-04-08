

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
		$("#main-content").load("page_" + currentid + ".html", function() {
			document.title = $("#" + currentid).text();
			$("#help-section-title").text(document.title);
			$(".top-bar-menu > ul > li > a").removeClass("top-bar-menu-selected");
			$("#" + currentid).addClass("top-bar-menu-selected");
			reloadhandlers(currentid);
		});
	}

	function reloadhandlers(pagename) {
		if (pagename == "demos") {
			/* Navigation for demos */
			$(".demo-links > ul > li > a").click(function(evt) {
				evt.preventDefault();
				$("#demos-inner-content").load("page_" + $(this).parent().attr("id") + ".html");
				$(".demo-links > ul > li > a").removeClass("demo-link-active");
				$(this).addClass("demo-link-active");
			});
			
			/* Default loading */
			$(".demo-links > ul > li > a").first().addClass("demo-link-active");
			$("#demos-inner-content").load("page_" + $(".demo-links > ul > li").first().attr("id") + ".html");
		} else {
		}
	}

});

/* Support function for sitemap */
function openPage(url) {
	if (window.opener)
		window.opener.location.href = url;
	else
		window.open(url);
}
