// Site video
$('#play-video').on('click', function (e) {
  e.preventDefault();
  $('#video-overlay').addClass('open');
  $("#video-overlay").append('<iframe src="https://player.vimeo.com/video/315957327?autoplay=1" frameborder="0" allow="autoplay; fullscreen" webkitallowfullscreen mozallowfullscreen allowfullscreen ></iframe >');
});

$('.video-overlay, .video-overlay-close').on('click', function (e) {
  e.preventDefault();
  close_video();
});

$(document).keyup(function (e) {
  if (e.keyCode === 27) { close_video(); }
});

function close_video() {
  $('.video-overlay.open').removeClass('open').find('iframe').remove();
};

// Timelapse video
$('#timelapse-video-btn').on('click', function (e) {
  e.preventDefault();
  $('#video-overlay').addClass('open');
  $("#video-overlay").append('<iframe src="https://player.vimeo.com/video/390796627?autoplay=1" frameborder="0" allow="autoplay; fullscreen" allowfullscreen></iframe>');
});

$('.video-overlay, .video-overlay-close').on('click', function (e) {
  e.preventDefault();
  close_video();
});

$(document).keyup(function (e) {
  if (e.keyCode === 27) { close_video(); }
});

function close_video() {
  $('.video-overlay.open').removeClass('open').find('iframe').remove();
};