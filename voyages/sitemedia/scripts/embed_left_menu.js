function setupleftmenu ()	{
	/* Initialization for section with subsections/pages */
	$.each(sectionToc, function(i, value) {
		if (value["hasSubsection"] == true) {
				ajaxsetupload(value["wrappername"]);
		}
	});
	
	/* Set up event handlers */
	$.each(sectionToc, function(i, value) {
		if (value["hasSubsection"] == true) {
			$("#" + value["mainid"]).click(function() {
				wrappername = value["wrappername"];
				templateprefix = value["templateprefix"];
				currentid = $("#" + wrappername + " div").first().attr("id");;

				$("#prev-page").hide();
				$("#next-page").show();
				$("#center-content-inner").load(currentid + ".html");
				
				updatebreadcrumb($("#" + value["mainid"]).first().text());
				
				if (enableCollapse) {
					/* Hide other submenus */
					$(".secondary-menu-subitems-0").addClass("hidden");
					$("#" + value["wrappername"]).removeClass("hidden");
				}
			});
		} else {
			$("#" + value["mainid"]).click(function() {
				if (enableCollapse) {
					/* Hide other submenus */
					$(".secondary-menu-subitems-0").addClass("hidden");
					
				}
				updatebreadcrumb($("#" + value["mainid"]).first().text());
				
				currentid = value["mainid"];
				$("#prev-page").hide();
				$("#next-page").hide();
				$("#center-content-inner").load(value["mainid"] + ".html");
			});
		}
	});
	setupnextprev();
}

function ajaxsetupload(wrappername2) {
	$("#" + wrappername2 + " div").each(function() {
		/* load the page on click */
		$("#" + this.id).click(function() {
			currentid = this.id;
			updatebreadcrumb($(this).parent().prev().text());
			
			$("#breadcrumb-lastelem").text(current_section_name);
			$("#center-content-inner").load(this.id + ".html", updatelinktext(currentid));
		});
	});
}

function setupnextprev() {
	/* This only triggers if there is a valid previous page */
	$("#prev-page").click(function() {
		currentid = $("#" + currentid).prev().attr("id");
		$("#center-content-inner").load(currentid + ".html", function() {
			updatelinktext(currentid);
		});
	});

	/* This only triggers if there is a valid next page */
	$("#next-page").click(function() {
		currentid = $("#" + currentid).next().attr("id");

		$("#center-content-inner").load(currentid + ".html", function() {
			updatelinktext(currentid);
		});
	});
}

function updatelinktext(currentid) {
	$("#center-content-inner").resize();
	
	$("#" + wrappername + " div").removeClass(selectedClass);
	$("#" + currentid).addClass(selectedClass);

	if ($("#" + currentid).prev().length != 0) {
		$("#prev-page").show();
		$("#prev-page").text($("#" + currentid).prev().text());
	} else {
		$("#prev-page").hide();
	}

	if ($("#" + currentid).next().length != 0) {
		$("#next-page").show();
		$("#next-page").text($("#" + currentid).next().text());
	} else {
		$("#next-page").hide();
	}
}

function updatebreadcrumb(newpagename) {
	current_section_name = newpagename;
	document.title = current_section_name;
	$("#breadcrumb-lastelem").text(current_section_name);
}
