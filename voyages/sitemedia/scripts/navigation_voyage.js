/* Append some other headers */
var section_prefix = "voyage";
var templateprefix = "method-";
var currentid = "method-01";
var wrappername = "methodology00";
var selectedClass = "voyage_selected";

$(document).ready(function() {
	/* Default loading of the first page */
	$("#center-content-inner").load("/voyage/guideintro.html");
	$("#prev-page").hide();
	$("#next-page").hide();
	$("#inner-content-header").hide();	
});