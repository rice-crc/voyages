function getleftmenu(dictionaryname, sectionprefix, prefix)
{
	var htmlcode = "";
	$.each(dictionaryname, function(key, value) {
		// load about page on click
		htmlcode += "<div class=\"secondary-menu-item-1\"><a href=\"/"+ sectionprefix +"/"+ prefix + "-" + key + ".html\">" + value + "</a></div>";
	});
	return htmlcode;
}


