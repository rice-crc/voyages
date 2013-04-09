var section_prefix = "assessment";
var selectedClass = "assessment_selected";

var wrappername = "essays-intro00";
var templateprefix = "essays-intro";
var enableCollapse = true; 

/* The first page to be loaded */
var currentid = "chapter01_section01_page01";

var sectionToc = [
	{"mainid" : "section01", "hasSubsection" : true, "wrappername": "essays-intro00",},
	{"mainid" : "essays-seasonality", "hasSubsection" : true, "wrappername": "essays-seasonality00", },
	{"mainid" : "essays-grandio", "hasSubsection" : false,},
	{"mainid" : "essays-solomon", "hasSubsection" : false,},
	{"mainid" : "essays-mulgrave", "hasSubsection" : false,},
	{"mainid" : "essays-applied-history", "hasSubsection" : false,},
]

$(document).ready(function() {
	/* Set up handling for each subsection */
	setupleftmenu();
	
	/* Load the first page */
	$("#center-content-inner").load(currentid + ".html");
	$("#prev-page").hide();
	
	/* The first page has a link to the next page */
	updatelinktext(currentid);
	$("#next-page").show();
	$(".secondary-menu-subitems-0").addClass("hidden");
	$("#" + wrappername).removeClass("hidden");
});