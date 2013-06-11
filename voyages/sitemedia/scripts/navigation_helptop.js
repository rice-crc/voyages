var top_selected_class = "top-bar-menu-selected";

$(document).ready(function() {
	var href = document.location.href;
	var elem = href.split("=");
	var maxIdx = elem.length - 1;
	var currentid = elem[maxIdx];
	
	if (currentid == "page_faqs") {
		return;
	} else {
	
	/* Remove the pound sign as necessary */
	var pound_sign_pos = currentid.indexOf("#");
	if (pound_sign_pos >= 0) {
		currentid = currentid.substring(0, pound_sign_pos);
	}
	
	/* Event handler for loading pages on click from the top navigation */
	$(".top-bar-menu > ul > li > a").each(function() {
		/* load the page on click */
		$("#" + this.id).click(function(ev) {
			ev.preventDefault();
			currentid = this.id;
			updatetitlehighlight();
		});
	});
	
	/* Retrieve the initial title and highlight */
	updatetitlehighlight();

	/* Update the title of the page and highlighted section based on the current location */
	function updatetitlehighlight() {
		$("#main-content").load("page_" + currentid, function() {
			document.title = $("#" + currentid).text();
			$("#help-section-title").text(document.title);
			$(".top-bar-menu > ul > li > a").removeClass(top_selected_class);
			$("#" + currentid).addClass(top_selected_class);
			reloadhandlers(currentid);
		});
	}

	/* Load AJAX event handler for specific section */
	function reloadhandlers(pagename) {
		if (pagename == "demos") {
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
		} else if (pagename =="sitemap") {
			/* Let the link on sitemap page opens a new page in the parent window */
			$("#toplinks a").click(function(ev){
				ev.preventDefault();
				openPage($(this).attr("href"));
			}); 
		} else if (pagename == "faqs") {
			$(".faq-answer a").click(function(ev){
				if ( this.href.indexOf("/help/help?section=") == -1
					&& (this.href).indexOf(window.location.hostname) >= 0) {
					/* Website internal links open page in the parent window
					 * except for Help pages open in the same window */
					ev.preventDefault();
					openPage($(this).attr("href"));
				}
			});
		}
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
