import Ember from 'ember';

export default Ember.Component.extend({
  filter: Ember.inject.service("voyagesSearch"),

  didInsertElement() {
    var menu = this.$(".dropdown-menu");
    var activateSubmenu = function(row) {
      var $row = $(row),
        submenuId = $row.data("submenuId"),
        $submenu = $("#" + submenuId),
        height = menu.outerHeight(),
        width = menu.outerWidth();

      // Show the submenu
      $submenu.css({
        display: "block",
        top: -3,
        left: width - 6, // main should overlay submenu
        height: height // padding for main dropdown's arrow
      });

      // Keep the currently activated row's highlighted look
      $row.find("a").addClass("maintainHover");
    }

    var deactivateSubmenu = function(row) {
      var $row = $(row),
        submenuId = $row.data("submenuId"),
        $submenu = $("#" + submenuId);
      // Hide the submenu and remove the row's highlighted look
      $submenu.css("display", "none");
      $row.find("a").removeClass("maintainHover");
    }

    this.$(".dropdown-menu").menuAim({
      activate: activateSubmenu,
      deactivate: deactivateSubmenu
    });

    this.$(".dropdown-menu li").click(function(e) {
      e.stopPropagation();
    });

  },
});
