$(document).ready(function() {
  $('[data-toggle="offcanvas"]').click(function() {
    $('.row-offcanvas').toggleClass('active')
  });
});

$(window).resize(function() {
  var footerHeight = $("footer").height();
  $("body").css("margin-bottom", footerHeight+"px");
});

$(document).ready(function() {
  var offcanvasHeight = $(".sidebar-offcanvas").height();
  if (offcanvasHeight > $(".container-new").height()) {
    $(".container-new").height(offcanvasHeight);
  }
});
