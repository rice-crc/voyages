function getprevnext(toc_dictionary, prefix) {
	/* Dependent on breadcrumb section */
	var filename = elem[maxIdx];
	var hreflength = filename.length;
	
	/* The filename is in the format: prefix-##.html*/
	var pageNum = parseInt(hreflength - 7, hreflength - 5);

	var prevnextlinks = "<table class=\"" + prefix + "-prev-next\"><tr>";
	/* Set previous link */
	if (pageNum == 1) {
		prevnextlinks += "<td class=\"" + prefix + "-prev\">&nbsp;</td>";
	} else if (pageNum > 1 && pageNum <= 10) {
		prevnextlinks += "<td class=\"" + prefix + "-prev\"><a href=\"" + prefix + "-0" + (pageNum - 1) + ".html\">" + toc_dictionary["0" + (pageNum - 1)] + "</a></td>";
	} else {
		prevnextlinks += "<td class=\"" + prefix + "-prev\"><a href=\"" + prefix + "-" + (pageNum - 1) + ".html\">" + toc_dictionary["" + (pageNum - 1)] + "</a></td>";
	}

	/* Set next link */
	if (pageNum == Object.keys(toc_dictionary).length) {
		prevnextlinks += "<td class=\"" + prefix + "-next\">&nbsp;</td>";
	} else if (pageNum > 1 && pageNum <= 8) {
		prevnextlinks += "<td class=\"" + prefix + "-next\"><a href=\"" + prefix + "-0" + (pageNum + 1) + ".html\">" +  toc_dictionary["0" + (pageNum + 1)] + "</a></td>";
	} else {
		prevnextlinks += "<td class=\"" + prefix + "-next\"><a href=\"" + prefix + "-" + (pageNum + 1) + ".html\">" +  toc_dictionary["" + (pageNum + 1)] + "</a></td>";
	}

	prevnextlinks += "</tr></table>";
	return prevnextlinks;
}

