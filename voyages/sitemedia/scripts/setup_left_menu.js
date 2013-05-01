/* HTML DOM const-elements for navigation  */
var lm_section_referral = "mainid";

var lm_suffix_cover = "_cover";
var lm_suffix_wrapper = "_submenu";

var lm_load_to_target_seclect = "#center-content-inner";
var lm_breadcrumb_last_select = "#breadcrumb-lastelem";

var lm_prev_pg_select = "#prev-page";
var lm_next_pg_select = "#next-page";

var lm_sub_menu_cssclass = ".secondary-menu-subitems-0";
var invi_cssclass = "hidden";

var lm_wrappername;
var lm_templateprefix;
var lm_currentid;

$(document).ready(function() {
	var pagehref = document.location.href;
	var pageelem = href.split("=");
	var pagecurrentid = null;
	
	if (pageelem.length == 2) {
		pagecurrentid = pageelem[pageelem.length - 1];
	}
	
	/* Set up handling for each subsection */
	setupleftmenu();
	/* Load the first page */
	if (lm_enableCollapse) {
		/* Hide other submenus */
		$(lm_sub_menu_cssclass).addClass(invi_cssclass);
	}
	defaultsect = lm_sectionToc[0][lm_section_referral];
	if ($("#" + defaultsect + lm_suffix_wrapper + " div").length > 0) {
		$(lm_next_pg_select).show();
		lm_currentid = $("#" + defaultsect + lm_suffix_wrapper + " div").first().attr("id");
		$("#" + defaultsect + lm_suffix_wrapper).removeClass(invi_cssclass);
	} else {
		lm_currentid = defaultsect + lm_suffix_cover;
	}
	/* The first page has a link to the next page */
	updatelinktext(lm_currentid);
	if (typeof(def_page) != 'undefined') {
   		lm_currentid = def_page;
	} else if (pagecurrentid != null) {
		lm_currentid = pagecurrentid;
	}
	$(lm_load_to_target_seclect).load(lm_currentid);
	updatelinktext();
});

function setupleftmenu ()	{
	/* Set up event handlers for each section */
	
	$.each(lm_sectionToc, function(i, value) {
		if ($("#" + value[lm_section_referral] + lm_suffix_wrapper + " div").length > 0) {
			/* Has a submenu */
			
			/* Set up handlers for submenu items */
			ajaxsetupload("#" + value[lm_section_referral] + lm_suffix_wrapper);
		}
	});
	
	$.each(lm_sectionToc, function(i, value) {	
		/* Set up the handler for the current section main item */
		$("#" + value[lm_section_referral] + lm_suffix_cover).click(function() {
			lm_wrappername = value[lm_section_referral] + lm_suffix_wrapper;

			/* Update the highlights */
			$(lm_sub_menu_cssclass + " div").removeClass(selectedClass);

			if ($("#" + value[lm_section_referral] + lm_suffix_wrapper + " div").length > 0) {
				/* Has a submenu */
				lm_wrappername = value[lm_section_referral] + lm_suffix_wrapper;
				lm_currentid = $("#" + lm_wrappername + " div").first().attr("id");;
				$(lm_prev_pg_select ).hide();
				$(lm_next_pg_select ).show();			
				$("#" + lm_currentid).addClass(selectedClass);
			} else {
				/* Has no submenu -> load only the cover page */
				lm_currentid = value[lm_section_referral] + lm_suffix_cover;
				$(lm_prev_pg_select).hide();
				$(lm_next_pg_select).hide();
			}
			
			if (lm_enableCollapse) {
				/* Hide other submenus */
				$(lm_sub_menu_cssclass).addClass(invi_cssclass);
				$("#" + lm_wrappername).removeClass(invi_cssclass);
			}
			
	
			
			updatebreadcrumb($("#" + value[lm_section_referral] + lm_suffix_cover).first().text());
			$(lm_load_to_target_seclect).load(lm_currentid);
		});

	});
	
	/* Set up previous and next navigation event handlers */
	setupnextprev();

	function ajaxsetupload(wrappername2) {
		$(wrappername2 + " div").each(function() {
			/* load the page on click */
			$("#" + this.id).click(function() {
				lm_currentid = this.id;
				updatebreadcrumb($(this).parent().prev().text());

				$(lm_breadcrumb_last_select).text(current_section_name);
				$(lm_load_to_target_seclect).load(this.id, updatelinktext());
			});
		});
	}
	
	function setupnextprev() {
		/* This only triggers if there is a valid previous page */
		$(lm_prev_pg_select).click(function() {
			lm_currentid = $("#" + lm_currentid).prev().attr("id");
			$(lm_load_to_target_seclect).load(lm_currentid, function() {
				updatelinktext();
			});
		});

		/* This only triggers if there is a valid next page */
		$(lm_next_pg_select).click(function() {
			lm_currentid = $("#" + lm_currentid).next().attr("id");
	
			$(lm_load_to_target_seclect).load(lm_currentid, function() {
				updatelinktext();
			});
		});
	}
}

/* Update the text for next-previous link navigation */
function updatelinktext() {
	$(lm_load_to_target_seclect).resize();
	
	$(lm_sub_menu_cssclass + " div").removeClass(selectedClass);
	$("#" + lm_currentid).addClass(selectedClass);

	if ($("#" + lm_currentid).prev().length != 0) {
		$(lm_prev_pg_select).show();
		$(lm_prev_pg_select).text($("#" + lm_currentid).prev().text());
	} else {
		$(lm_prev_pg_select).hide();
	}

	if ($("#" + lm_currentid).next().length != 0) {
		$(lm_next_pg_select).show();
		$(lm_next_pg_select).text($("#" + lm_currentid).next().text());
	} else {
		$(lm_next_pg_select).hide();
	}
}

/* Update the breadcrumb and page title */
function updatebreadcrumb(newpagename) {
	current_section_name = newpagename;
	document.title = current_section_name;
	$(lm_breadcrumb_last_select).text(current_section_name);
}
