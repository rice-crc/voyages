/* Dependent on breadcrumb section */
var filename = elem[maxIdx];
var pageNum = parseInt(filename.substr(12, 14));

var prevnextlinks = "<table class=\"method-prev-next\"><tr>";
/* Set previous link */
if (pageNum == 1) {
	prevnextlinks += "<td class=\"method-prev\">&nbsp;</td>";
} else if (pageNum > 1 && pageNum <= 10) {
	prevnextlinks += "<td class=\"method-prev\"><a href=\"methodology-0" + (pageNum -1) + ".html\">" + listNavVoyageSection["0" + (pageNum -1)] + "</a></td>";
} else {
	prevnextlinks += "<td class=\"method-prev\"><a href=\"methodology-" + (pageNum -1) + ".html\">" + listNavVoyageSection["" + (pageNum -1)] + "</a></td>";
}

/* Set next link */
if (pageNum == 22) {
	prevnextlinks += "<td class=\"method-next\">&nbsp;</td>";
} else if (pageNum > 1 && pageNum <= 8) {
	prevnextlinks += "<td class=\"method-next\"><a href=\"methodology-0" + (pageNum + 1) + ".html\">" + listNavVoyageSection["0" + (pageNum + 1)] + "</a></td>";
} else {
	prevnextlinks += "<td class=\"method-next\"><a href=\"methodology-" + (pageNum + 1) + ".html\">" + listNavVoyageSection["" + (pageNum + 1)] + "</a></td>";
}

prevnextlinks += "</tr></table>";
document.writeln(prevnextlinks);	
