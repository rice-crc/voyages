/* List of possible elem[3] extracted from current href 
 * Names of the major sections used by breadcrumb.js to display the section name */
var majorSectionName = {
	"voyage" : "Voyages Database",
	"assessment" : " Assessing the Slave Trade",
	"resources" : "Resources",
	"education" : "Educational Materials",
	"about" : "About the Project",
	"contribute" : "Contribute",
}

/* Call breadcrumb handler in breadcrumb.js to update the breadcrumb section
 * and set up event handlers for help-links */
$(document).ready(function() {
	/* Update the breadcrumb text and link */
	if (typeof writebreadcrumb == 'function') { 
  		$(".secondary-bar-breadcrumb").html(writebreadcrumb());
	}
	
	/* Highlight the menu section that is being currently selected */
	if (typeof maybeObject !='undefined') {	
		$("#" + elem[3]).addClass("main_nav-selected");
	}
	
	
	/* Secondary menu event handler */
	$(".secondary-bar-help-link a").click(function(ev){
		ev.preventDefault(); /* Disable the default/nothing action */
		openPopup(this.href); /* Open the pop up window */
	});
});

/* Display a new pop-up window for help-links when the user clicks on it*/
function openPopup(pageUrl) {
window.open( pageUrl,
	"tastPopupHelp",
	"resizable=yes, " +
	"location=no, " +
	"status=no, " +
	"scrollbars=yes, " +
	"width=700, " +
	"height=680").focus();
} 