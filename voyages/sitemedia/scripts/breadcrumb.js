var href = document.location.href;
var seperatorst = "&nbsp; <img src=\"/static/images/breadcrumb/breadcrumb-separator.png \" /> ";
var elem = href.split("/");

/* Parse the link to the home page */
path = "&nbsp;&nbsp;<a href=\"" + href.substring(0, href.indexOf("/" + elem[2]) + elem[2].length + 1) + "/\">" + "Home"  + "</a>"
+ seperatorst;

/* Add successive elements and seperators */
for (var i = 3; i < elem.length - 1; i++) {
	path += "<a href=\"" + href.substring(0, href.indexOf("/" + elem[i]) + elem[i].length + 1) + "/\">" + elem[i] + "</a>" +
	seperatorst;
}

/* Add the last element */
i = elem.length - 1;						
path += "<a href=\"" + href.substring(0, href.indexOf(elem[i]) + elem[i].length) + "\">" + elem[i] + "</a>";						

/* Output the bread crumb */
document.writeln(path);
