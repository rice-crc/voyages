import Ember from 'ember';

export default Ember.Controller.extend({

  didInsertElement: function() {
    // WORK IN PROGRESS - not functional
    // jQuery for page scrolling feature - requires jQuery Easing plugin
    Ember.$('a.page-scroll').bind('click', function(event) {
      var $anchor = $(this);
      $('html, body').stop().animate({
        scrollTop: ($($anchor.attr('href')).offset().top - 50)
      }, 1250, 'easeInOutExpo');
      event.preventDefault();
    });

    // Highlight the top nav as scrolling occurs
    Ember.$('body').scrollspy({
      target: '.navbar-fixed-top',
      offset: 51
    });

    // Closes the Responsive Menu on Menu Item Click
    Ember.$('.navbar-collapse ul li a').click(function() {
      $('.navbar-toggle:visible').click();
    });

    // Offset for Main Navigation
    Ember.$('#mainNav').affix({
      offset: {
        top: 100
      }
    })
  },
});
