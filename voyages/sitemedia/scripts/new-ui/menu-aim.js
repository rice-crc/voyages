// MENU AIM //
var $menu = null;
// jQuery-menu-aim: </meaningful part of the example>

// jQuery-menu-aim: the following JS is used to show and hide the submenu
// contents. Again, this can be done in any number of ways. jQuery-menu-aim
// doesn't care how you do this, it just fires the activate and deactivate
// events at the right times so you know when to show and hide your submenus.
function activateSubmenu(row) {
		var $row = $(row),
				submenuId = $row.data("submenuId"),
				$submenu = $("#" + submenuId),
				height = $menu.outerHeight(),
				width = $menu.outerWidth();

		var parentWidth = $row.width();

		// Show the submenu
		$submenu.css({
				display: "block",
				top: -1,
				left: parentWidth + 47 // main should overlay submenu
				// height: height - 4  // padding for main dropdown's arrow
		});

		// Keep the currently activated row's highlighted look
		$row.addClass("maintainHover");
}

function deactivateSubmenu(row) {
		var $row = $(row),
				submenuId = $row.data("submenuId"),
				$submenu = $("#" + submenuId);

		// Hide the submenu and remove the row's highlighted look
		$submenu.css("display", "none");
		$row.removeClass("maintainHover");
}

$( document ).ready(function() {
	$menu = $(".search-menu");

	// jQuery-menu-aim: <meaningful part of the example>
	// Hook up events to be fired on menu row activation.
	$menu.menuAim({
			activate: activateSubmenu,
			deactivate: deactivateSubmenu
	});

	// Bootstrap's dropdown menus immediately close on document click.
	// Don't let this event close the menu if a submenu is being clicked.
	// This event propagation control doesn't belong in the menu-aim plugin
	// itself because the plugin is agnostic to bootstrap.
	$(".dropdown-menu li").click(function(e) {
			e.stopPropagation();
	});

	$(document).click(function() {
			// Simply hide the submenu on any click. Again, this is just a hacked
			// together menu/submenu structure to show the use of jQuery-menu-aim.
			$(".popover").css("display", "none");
			$("a.maintainHover").removeClass("maintainHover");
	});

});
