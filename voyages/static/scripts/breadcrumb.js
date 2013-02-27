var href = document.location.href;
	
var s = href.split("/");
path = "<a href=\"" + href.substring(0, href.indexOf("/" + s[2]) + s[2].length + 1) + "/\">" + "Home"  + "</a>"; 
for (var i = 3; i < s.length - 1; i++) {
	path += "<a href=\"" + href.substring(0, href.indexOf("/" + s[i]) + s[i].length + 1) + "/\">" + s[i] + "</a>" +
	"<img src=\"/static/images/breadcrumb/breadcrumb-separator.png \" /> ";
}
	
		
i = s.length - 1;						
path += "<a href=\"" + href.substring(0, href.indexOf(s[i]) + s[i].length) + "\">" + s[i] + "</a>";						
document.writeln(path);
