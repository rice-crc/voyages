$(document).ready(function() {
  if ( window.location.pathname != '/' ){
    var footerHeight = $("footer").height();
    $("body").css("margin-bottom", footerHeight+"px");
  }
});

$(window).resize(function() {
  if ( window.location.pathname != '/' ){
    var footerHeight = $("footer").height();
    $("body").css("margin-bottom", footerHeight+"px");
  }
});
