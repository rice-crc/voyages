/* Retrieve the href/path to the current page*/
var href = document.location.href;
var seperatorst = "&nbsp; <img src=\"/static/images/breadcrumb/breadcrumb-separator.png \" /> ";
var elem = href.split("/");
var maxIdx = elem.length - 1;

/* Parse the link to the home page */
path = "&nbsp;&nbsp;<a href=\"" + href.substring(0, href.indexOf("/" + elem[2]) + elem[2].length + 1) + "/\">" + "Home"  + "</a>";

/* For landing pages of each section */
if (maxIdx == 3 && elem[3] != "") {
	path += seperatorst + majorSectionName[elem[3]] + "</a>";
}

/* For pages inside each section */
if (maxIdx >= 4 && elem[3] != "") {
	path += seperatorst + "<a href=\"" + href.substring(0, href.indexOf("/" + elem[3]) + elem[3].length + 1) 
			+ "/\">" + majorSectionName[elem[3]] + "</a>";
			
	
	/* Add successive elements and seperators */
	for (var i = 4; i < maxIdx; i++) {
		path += seperatorst + "<a href=\"" + href.substring(0, href.indexOf("/" + elem[i]) + elem[i].length + 1) 
		+ "/\">" + elem[i] + "</a>";
	}
	
	if (elem[maxIdx] != "index.html")
		/* The title of the index page to each section is never included more than once */
		path += seperatorst + document.title;
}
/* Output the bread crumb */
document.writeln(path);
