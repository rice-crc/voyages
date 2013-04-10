
/* Names of the major sections */
var majorSectionName = {
	"voyage" : "Voyages Database",
	"assessment" : " Assessing the Slave Trade",
	"resources" : "Resources",
	"education" : "Educational Materials",
	"about" : "About the Project",
}

$(document).ready(function() {
	$("#" + elem[3]).addClass("main_nav-selected");
	
	$(".secondary-bar-breadcrumb").html(writebreadcrumb());
	
	/* Secondary menu */
	$(".secondary-bar-help-link > a").click(function(ev){
		ev.preventDefault();
		openPopup("/help/help?section=" + this.id);
	});
	/*
	$.each(listNav, function(key, value) {
				// load about page on click
		$("#" + key).click(function(){
			
			$("#mycontent").load(value, function() {
				 $("#mycontent") .resize();
				}	
			);
			
		});
	}); 
	*/
	/*
	$.each(listNav, function(key, value) {
				// load about page on click
		$("#" + key).click(function(){
			window.location = value;
		});
	});
	*/ 
});

function openPopup(pageUrl) {
window.open( pageUrl,
	"tastPopupHelp",
	"resizable=yes, " +
	"location=no, " +
	"status=no, " +
	"scrollbars=yes, " +
	"width=680, " +
	"height=680").focus();
} 