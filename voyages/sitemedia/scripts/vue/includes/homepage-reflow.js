var reflow = function() {
  var coverBandHeight = $(".cover-band").height();
  var window_height = $(window).height();
  var cover_height = $("#bgvid").height();
  var visible_height = $(window.top).height();
  var coverEndHeight = $(".cover-end").height();
  var coverStartBottom = $(".cover-start").position().top + $(".cover-start").height();
  var coverCenterHeight = $(".cover-center").height();

  var offset = 32;

  if (coverBandHeight > visible_height) {
    $("#bgvid-container").height(coverBandHeight + offset);
    $(".cover-center").css("marginTop", "1rem");
  } else {
    $("#bgvid-container").height(visible_height);
    var coverCenterMarginTop = visible_height - coverStartBottom - offset - coverCenterHeight - coverEndHeight;
    if (coverCenterMarginTop < 0) {
      coverCenterMarginTop = 0;
    }
    $(".cover-center").css("marginTop", coverCenterMarginTop);
  }

  var bgvidContainerWidth = $("#bgvid-container").width();
  var bgvidContainerHeight = $("#bgvid-container").height();
  var videoRatio = 1875 / 894;

  if (bgvidContainerWidth / bgvidContainerHeight > videoRatio) {
    $("video#bgvid").width("100%");
    $("video#bgvid").height("");
  } else {
    $("video#bgvid").width("");
    $("video#bgvid").height("100%");
  }
}

$(document).ready(reflow);

window.onresize = function() {
  reflow();
}
