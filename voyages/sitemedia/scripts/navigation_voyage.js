/* Manage links  for the navigation left menu in the Methodology section of the Voyage section */
var methodology_toc = {
	"01": "Introduction", 
	"02": "Coverage of the Slave Trade", 
	"03": "Nature of Sources", 
	"04": "Cases and Variables", 
	"05": "Data Variables", 
	"06": "Age Categories", 
	"07": "Dates", 
	"08": "Names", 
	"09": "Imputed Variables", 
	"10": "Geographic Data", 
	"11": "Imputed Voyage Dates", 
	"12": "Classification as a Trans-Atlantic Slaving Voyage", 
	"13": "Voyage Outcomes", 
	"14": "Inferring Places of Trade", 
	"15": "Imputing Numbers of Slaves", 
	"16": "Regions of Embarkation and Disembarkation", 
	"17": "Age and Gender Ratios", 
	"18": "National Carriers", 
	"19": "Tonnage", 
	"20": "Resistance and Price of Slaves", 
	"21": "Appendix", 
	"22": "Notes", 
}

$(document).ready(function() {
	/* Append some other headers */
	var section_prefix = "voyage";
	
	/* Append some other headers */
	$("#left-menu").append(get_html_left_mainlink("/voyage/methodology.html", "Guide", "guide-main-00"));
	
	$.each(methodology_toc, function(key, value) {
		/* load the page on click */
		$("#left-menu").append(get_html_left_link(key, value, "intro"));
		
	});
	
	/* Default loading of the first page */
	$("#center-content-inner").load("/voyage/guideintro.html");
	$("#prev-page").hide();
	$("#next-page").hide();
	$("#inner-content-header").hide();
	$("guide-main-00").click(function() {
		$("#inner-content-header").hide();
		$("#center-content-inner").load("/voyage/guideintro.html");
	});
	
	$.each(methodology_toc, function(key, value) {
		/* load the page on click */
		$("#intro" + key).click(function(){
			$("#center-content-inner").load("/voyage/method-"+ key + ".html", 
				pagecallback(key, Object.keys(methodology_toc).length, methodology_toc, "method-")	
			);
		});
	});
});


function pagecallback(currentpagenum, maxNum, toc_dictionary, templateprefix) {
	$("#inner-content-header").show();
	$("#center-content-inner").resize();
	
	$(".secondary-menu-item-1 a").removeClass("voyage_selected");
	$("#intro" + currentpagenum).addClass("voyage_selected");

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