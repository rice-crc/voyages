/* Append some other headers */
var section_prefix = "assessment";
var maxNum = $("#essays-intro00 a").size();
var templateprefix = "essays-intro-";
var currentid = "essays-intro-01";
var wrappername = "essays-intro00";
var selectedClass = "assessment_selected";

$(document).ready(function() {
	/* Default loading of the first page */
	$("#center-content-inner").load(currentid+ ".html");
	$("#prev-page").hide();
	$("#next-page").hide();
	$("#inner-content-header").hide();	
});