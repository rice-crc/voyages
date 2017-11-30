$(document).ready(function() {
  $('[data-toggle="offcanvas"]').click(function() {
    $('.row-offcanvas').toggleClass('active')
  });
});

$(window).resize(function() {
  var offcanvasHeight = $(".sidebar-offcanvas").height();
  if (offcanvasHeight > $(".container-new").height()) {
    $(".container-new").height(offcanvasHeight);
  }
});

$(document).ready(function() {
  var offcanvasHeight = $(".sidebar-offcanvas").height();
  if (offcanvasHeight > $(".container-new").height()) {
    $(".container-new").height(offcanvasHeight);
  }
});
