$(document).ready(function() {
  var footerHeight = $("footer").height();
  $("body").css("margin-bottom", footerHeight+"px");
});

$(window).resize(function() {
  var footerHeight = $("footer").height();
  $("body").css("margin-bottom", footerHeight+"px");
});
