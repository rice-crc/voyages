/* Manage links  for the navigation left menu in the Methodology section of the Voyage section */
var essay_main_toc = {
	"01" : "A Brief Overview of the Trans-Atlantic Slave Trade",
	"02" : "Seasonality in the Trans-Atlantic Slave Trade",
	"03" : "Dobo: A Liberated African in Nineteenth-Century Havana",
	"04" : "Ayuba Suleiman Diallo and Slavery in the Atlantic World",
}

var essay_intro_toc = {
	"01" : "Introduction",
	"02" : "The Enslavement of Africans",
	"03" : "African Agency and Resistance",
	"04" : "Early Slaving Voyages",
	"05" : "Empire and Slavery",
	"06" : "The African Side of the Trade",
	"07" : "The Middle Passage",
	"08" : "The Ending of the Slave Trade",
	"09" : "The Trade’s Influence on Ethnic and Racial Identity",
	"10" : "Eventual Abolition",
	"11" : "Notes",
}

var essay_seasonality_toc = {
	"01" : "Introduction",
	"02" : "Agriculture in the era of the trans-Atlantic slave trade",
	"03" : "Seasonal rainfall in the Atlantic slaving world",
	"04" : "Rainfall, crop type and agricultural calendars",
	"05" : "Agricultural calendars and labor requirements",
	"06" : "Provisioning-slaving seasons",
	"07" : "Slave-trading seasonality: case studies",
	"07" : "Trans-Atlantic pathways and harvest cycles",
	"09" : "Conclusion",
}

$(document).ready(function() {
	/* Append some other headers */
	var section_prefix = "assessment";
	
	/* Append some other headers */
	$("#essays-left-menu").append(get_html_left_mainlink("/assessment/essays.html", essay_main_toc["01"], "essay-intro-main01"));
	
	$.each(essay_intro_toc, function(key, value) {
		/* load the page on click */
		$("#essays-left-menu").append(get_html_left_link(key, value, "intro"));
		
	});
	
	
	$("#essays-left-menu").append(get_html_left_mainlink("/assessment/essays.html", essay_main_toc["02"], "essay-intro-main02") );
	$.each(essay_seasonality_toc, function(key, value) {
		/* load the page on click */
		$("#essays-left-menu").append(get_html_left_link(key, value, "seasonality"));
	});
	
	
	/* Default loading of the first page */
	$("#center-content-inner").load("/assessment/essays-intro-01.html");
	$("#prev-page").hide();
	
	
	$.each(essay_intro_toc, function(key, value) {
		/* load the page on click */
		$("#intro" + key).click(function(){
			$("#center-content-inner").load("/assessment/essays-intro-"+ key + ".html", 
				pagecallback(key, Object.keys(essay_intro_toc).length, essay_intro_toc, "essays-intro-")	
			);
		});
	});
	
	
	
	$.each(essay_seasonality_toc, function(key, value) {
		/* load the page on click */
		$("#seasonality" + key).click(function(){
			$("#center-content-inner").load("/assessment/essays-seasonality-"+ key + ".html", 
				pagecallback(key, Object.keys(essay_seasonality_toc).length, essay_seasonality_toc, "essays-seasonality-")	
			);
		});
	});
	
});


function pagecallback(currentpagenum, maxNum, toc_dictionary, templateprefix) {
	$("#center-content-inner").resize();

	$(".secondary-menu-item-1 a").removeClass("assessment_selected");
	$("#intro" + currentpagenum).addClass("assessment_selected");

	var prevp = getpreviousnum(currentpagenum);
	var nextp = getnextnum(currentpagenum, maxNum);
	if (prevp == -1) {
		$("#prev-page").hide();
		
	} else {
		$("#prev-page").show();
		$("#prev-page").text(toc_dictionary[prevp]);
		/*
		$("#prev-page").click(function(){
			$("#center-content-inner").load(templateprefix + currentpagenum + ".html", 
				pagecallback(prevp, maxNum, toc_dictionary, templateprefix));
		});
		 */
	}

	if (nextp == -1) {
		$("#next-page").hide();
	} else {
		
		$("#next-page").show();
		$("#next-page").text(toc_dictionary[nextp]);
		/*
		$("#next-page").click(function(){
			$("#center-content-inner").load(templateprefix + currentpagenum + ".html", 
				pagecallback(nextp, maxNum, toc_dictionary, templateprefix));
		});
		 */
	}
}