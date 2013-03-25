function getleftmenu(dictionaryname, sectionprefix, prefix) {
	var htmlcode = "";
	$.each(dictionaryname, function(key, value) {
		// load about page on click
		htmlcode += "<div class=\"secondary-menu-item-1\"><a id=#" + sectionprefix + key + "\" href=\"/" + sectionprefix + "/" + prefix + "-" + key + ".html\">" + value + "</a></div>";
	});
	return htmlcode;
}

function get_html_left_link(linknum, linkcontent, prefix) {
	return "<div class=\"secondary-menu-item-1\"><a id=\"" + prefix + linknum + "\" href=\"#\">" + linkcontent + "</a></div>";
}

function get_html_left_mainlink(linkurl, linkcontent, elemid) {
	return "<div class=\"secondary-menu-item-0\"><a id=\"" + elemid + "\" href=\"" + linkurl + "\">" + linkcontent + "</a></div>";
}


/* Return a number DD where DD = currentNum - 1*/
function getpreviousnum(currentNum) {
	var pageNum = parseInt(currentNum, 10);
	if (pageNum == 1) {
		return -1;
	} else if (pageNum <= 10) {
		return "0" + (pageNum - 1);
	} else {
		return pageNum - 1;
	}
}

/* Return a number DD where DD = currentNum + 1*/
function getnextnum(currentNum, max) {
	var pageNum = parseInt(currentNum, 10);
	if (pageNum == max) {
		return -1;
	} else if (pageNum <= 8) {
		return "0" + (pageNum + 1);
	} else {
		return pageNum + 1;
	}
}

