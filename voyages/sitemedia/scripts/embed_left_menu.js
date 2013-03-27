

/* Update the text on previous and next link */
function updatelinktext(currentpagenum, maxNum, toc_dictionary) {
	$("#inner-content-header").show();
	$("#center-content-inner").resize();
				
	var prevp = getpreviousnum(currentpagenum);
	var nextp = getnextnum(currentpagenum, maxNum);
	if (prevp == -1) {
		$("#prev-page").hide();
		
	} else {
		$("#prev-page").show();
		$("#prev-page").text(toc_dictionary[prevp]);
	}

	if (nextp == -1) {
		$("#next-page").hide();
	} else {
		$("#next-page").show();
		$("#next-page").text(toc_dictionary[nextp]);
	}
}

$(document).ready(function() {
	

	$("#" + wrappername + " div").each(function(key, value) {
		/* load the page on click */

		$("#" + this.id).click(function() {
			$("#inner-content-header").show();
			currentpagenumber = key;
			currentid = this.id;

			$("#center-content-inner").load(this.id + ".html", updatelinktext(currentid));
		});
	});

	/* This only triggers if there is a valid previous page */
	$("#prev-page").click(function() {
		currentid = $("#" + currentid).prev().attr("id");

		$("#center-content-inner").load(currentid + ".html", function() {
			updatelinktext(currentid);
		});
	});

	/* This only triggers if there is a valid next page */
	$("#next-page").click(function() {
		currentid = $("#" + currentid).next().attr("id");

		$("#center-content-inner").load(currentid + ".html", function() {
			updatelinktext(currentid);
		});
	});

});

function updatelinktext(currentid) {
	$("#center-content-inner").resize();
	$("#" + wrappername + " div").removeClass(selectedClass);
	$("#" + currentid).addClass(selectedClass);

	if ($("#" + currentid).prev().length != 0) {
		$("#prev-page").show();
		$("#prev-page").text($("#" + currentid).prev().text());
	} else {
		$("#prev-page").hide();
	}


	if ($("#" + currentid).next().length != 0) {
		$("#next-page").show();
		$("#next-page").text($("#" + currentid).next().text());
	} else {
		$("#next-page").hide();
	}
}
