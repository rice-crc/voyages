/* Return a HTML code containing links to previous and next page in the menu list */
function getprevnext(toc_dictionary, hrefprefix, styleprefix) {
	/* Dependent on breadcrumb section */
	var filename = elem[maxIdx];
	var hreflength = filename.length;
	
	/* The filename is in the format: hrefprefix-##.html*/
	var pageNum = parseInt(filename.substring(hreflength - 7, hreflength - 5), 10);

	var prevnextlinks = "<table class=\"" + styleprefix + "-prev-next\"><tr>";
	/* Set previous link */
	if (pageNum == 1) {
		prevnextlinks += "<td class=\"" + styleprefix + "-prev\">&nbsp;</td>";
	} else if (pageNum > 1 && pageNum <= 10) {
		prevnextlinks += "<td class=\"" + styleprefix + "-prev\"><a href=\"" + hrefprefix + "-0" + (pageNum - 1) + ".html\">" + toc_dictionary["0" + (pageNum - 1)] + "</a></td>";
	} else {
		prevnextlinks += "<td class=\"" + styleprefix + "-prev\"><a href=\"" + hrefprefix + "-" + (pageNum - 1) + ".html\">" + toc_dictionary["" + (pageNum - 1)] + "</a></td>";
	}

	/* Set next link */
	if (pageNum == Object.keys(toc_dictionary).length) {
		prevnextlinks += "<td class=\"" + styleprefix + "-next\">&nbsp;</td>";
	} else if (pageNum >= 1 && pageNum <= 8) {
		prevnextlinks += "<td class=\"" + styleprefix + "-next\"><a href=\"" + hrefprefix + "-0" + (pageNum + 1) + ".html\">" +  toc_dictionary["0" + (pageNum + 1)] + "</a></td>";
	} else {
		prevnextlinks += "<td class=\"" + styleprefix + "-next\"><a href=\"" + hrefprefix + "-" + (pageNum + 1) + ".html\">" +  toc_dictionary["" + (pageNum + 1)] + "</a></td>";
	}

	prevnextlinks += "</tr></table>";
	
	return prevnextlinks;
}



