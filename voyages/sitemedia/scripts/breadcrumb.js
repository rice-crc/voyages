/* Retrieve the href/path to the current page*/
var href = document.location.href;
var seperatorst = "&nbsp; <img src=\"/static/images/breadcrumb/breadcrumb-separator.png \" /> ";
var elem = href.split("/");
var maxIdx = elem.length - 1;

function writebreadcrumb() {
	if (maxIdx == 3 && elem[maxIdx] == "") {
		return "<div class='breadcrumb'>Home</div>";
	}
	
	/* Parse the link to the home page */
	path = "<div class='breadcrumb'><a href=\"" + href.substring(0, href.indexOf("/" + elem[2]) + elem[2].length + 1) + "/\">" + "Home"  + "</a>";

	/* For landing pages of each section */
	if ((maxIdx == 3 && elem[3] != "") || (maxIdx == 4 && elem[maxIdx] == "index.html")
		|| (maxIdx == 4 && elem[maxIdx] == "")) {
		path += seperatorst + majorSectionName[elem[3]];
	} else if (maxIdx >= 4 && elem[3] != "" && elem[4] != "index.html") {

		path += seperatorst + "<a href=\"" + href.substring(0, href.indexOf("/" + elem[3]) + elem[3].length + 1) 
				+ "/\">" + majorSectionName[elem[3]] + "</a>";
		
		/* Remove the pound sign as necessary */
		var pound_sign_pos = elem[4].indexOf("#");
		if (pound_sign_pos >= 0) {
			elem[4] = elem[4].substring(0, pound_sign_pos);
		}		
		
		if (elem[3] == "voyage" && (elem[4] == "understanding-db")) {
			path += seperatorst + "Understanding the Database";
        } else if (elem[3] == "voyage" && (elem[4] == "source")) {
            path += seperatorst + "Understanding the Database";
		} else if (elem[3] == "assessment" && (elem[4] == "essays")) {
			path += seperatorst + "Essays";
        } else if (elem[3] == "resources" && (elem[4] == "images")) {
		}else {
			/* Add successive elements and seperators */
			for (var i = 4; i < maxIdx; i++) {
				path += seperatorst + "<a href=\"" + href.substring(0, href.indexOf("/" + elem[i]) + elem[i].length + 1) 
				+ "/\">" + elem[i] + "</a>";
			}
		}
		
		if (elem[maxIdx] != "index.html") {
			/* The title of the index page to each section is never included more than once */
			path += seperatorst + "<span id=\"breadcrumb-lastelem\">" + document.title + "</span>";
		}
	}
	path += "</div>";
	/* Output the bread crumb */
	return path;
}