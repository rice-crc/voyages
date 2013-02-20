$(document).ready(function() {
	
	/* $("#mycontent").load("defhome.html"); */
	$("#" + key).click(function(){
		$("#mycontent").load("tmpPage.html");
	});

	var listNav = {
			"item01" : "database/index.html",
			"item01a" : "database/guide.html",
			"item01b" : "database/search.html",
			"item01c" : "database/download.html",
			"item01d" : "database/submission-login.html",
			
			"item02" : "assessment/index.html",
			"item02a" : "assessment/essays-intro.html",
			"item02b" : "assessment/estimates.html",
			"item02c" : "assessment/intro-maps.html",
			
			"item03" : "resources/index.html",
			"item03a" : "resources/images.html",
			"item03b" : "resources/origins.html",
			
			"item04" : "assessment/index.html",
			"item04a" : "assessment/lessons-plans.html",
			"item04b" : "assessment/others.html",
			
			"item05" : "about/index.html",
			"item05a" : "about/history.html",
			"item05b" : "about/team.html",
			"item05c" : "about/data.html",
			"item05d" : "about/acknowledgements.html",
			"item05e" : "about/origins.html",
			"item05f" : "about/contacts.html",

		}
		
	
	/*
	
	$.each(listNav, function(key, value) {
		alert("key is " + key + "and value = " + value);
		// load about page on click
		$("#" + key).click(function(){
			
			$("#mycontent").load(value);
		});
	}); 
	*/
	
	/*
	<script type="text/javascript">
		$("#item2").click(function(){
			$("#mycontent").load("tmpPage.html");
			alert("Done with loading");
		});
		
	</script>
	*/
});