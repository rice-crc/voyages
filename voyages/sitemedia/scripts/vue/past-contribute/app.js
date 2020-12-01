// main app
var pastContribute = new Vue({
    el: "#past-contribute",
    delimiters: ["[[", "]]"],
    data: {
        enslaved: {},
        total_names: 0,
        recordings_content: '',
        audioList: {},
        language_groups: new TreeselectVariable({
            varName: "language_groups",
            label: gettext("Language Group"),
            description: "",
        },{
            op: "is one of",
            searchTerm: [],
        },{
            isImputed: false,
            isadvanced: false
        }),
        filterData: {
          treeselectOptions: {
          }
        },
    },
    created: function() {
        var params = {
            "search_query": {
                "enslaved_id": [
                AFRICAN_ID,
                AFRICAN_ID
                ]
            },
        };

        axios
        .post('/past/api/search', params)
        .then(function(response) {
            pastContribute.enslaved = response.data.data[0];
            var arrivalDateArray = pastContribute.enslaved.voyage__voyage_dates__first_dis_of_slaves ? pastContribute.enslaved.voyage__voyage_dates__first_dis_of_slaves.split([',']) : '';
            var arrivalDate = '';

            if (arrivalDateArray.length == 3) {
                arrivalDate = arrivalDateArray[2];
            } else if (arrivalDateArray.length == 1) {
                arrivalDate = arrivalDateArray[0];
            }
            pastContribute.enslaved.voyage_year = arrivalDate;

            var audiosList = $("<div></div>");
            $.each(pastContribute.enslaved.recordings, function (key, item) {
                $.each(item.langs, function (langKey, langItem) {
                    $.each(langItem.records, function (recordKey, recordItem) {
                        var elementId = (''+recordItem).replace(/\./g, '_');

                        var recordVersion = '';
                        if (langItem.records.length > 1) {
                            recordVersion = ' - v'+recordItem.split('.')[2];
                        }

                        var itemList = $("<div><button data-audio-id='" + elementId + "' class='btn btn-transparent far fa-play-circle mr-1 audio-player px-1'></button>" +
                            key + ' (' + langItem.lang + ')' + recordVersion+"</div>");
                        audiosList.append(itemList);
                    });
                });
            });

            var content = $("<div><div class='audios-"+pastContribute.enslaved.enslaved_id+"'></div></div>");
            content.find(".audios-"+pastContribute.enslaved.enslaved_id).append(audiosList);
            pastContribute.recordings_content = content.html();
            return;
        })
        .catch(function(error) {
            return error;
        });
    }
});

function highlightFeature(e) {
    var layer = e.target;

    layer.setStyle({
        weight: 5,
        color: '#666',
        dashArray: '',
        fillOpacity: 0.7
    });

    if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
        layer.bringToFront();
    }
}

function resetHighlight(e) {
    geojson.resetStyle(e.target);
}

function zoomToFeature(e) {
    mymap.fitBounds(e.target.getBounds());
}

function style(feature) {
    return {
        weight: 2,
        opacity: 1,
        color: 'transparent',
        dashArray: '3',
        fillOpacity: 0.7
    };
}

function onEachFeature(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
        click: zoomToFeature
    });
}

var africaCountriesData = (function() {
    var json = null;
    $.ajax({
        'async': false,
        'global': false,
        'url': STATIC_URL+'maps/js/past/africa-hig.geo.json',
        'dataType': "json",
        'success': function(data) {
            json = data;
        }
    });
    return json;
})();
var geojson;
var mymap;

$(function(){
    $($('.review-recording').find('audio')[0]).on("canplay", function () {
        $('.duration').html(secondsTimeSpanToMS(this.duration));
    }).on('ended', function(){
        $(this).siblings('.audio-controls').find('.play-button').removeClass('fas fa-stop').addClass('fas fa-play-circle');
    });

    $('body').on('click', function (e) {
        //did not click a popover toggle, or icon in popover toggle, or popover
        if ($(e.target).parents('.popover').length === 0) {
            $('[data-toggle="popover"]').popover('hide');
        }
        var toggle = $(e.target).data('toggle');
        if (toggle == "popover") {
            $(e.target).popover('show');
        }
    });

    $('[data-toggle="popover"]').popover({
        container: 'body',
        placement: 'bottom',
        html: true,
        content: $('#popper-content'),
    }).on('show.bs.popover', function() {
        $('#popper-content').addClass('d-block');
    }).on('hide.bs.popover', function() {
        $('#popper-content').addClass('d-none');
    });
    $('[data-toggle="popover"]').on('shown.bs.popover', function () {
        var enslavedId = $(this).data('enslaved-id');

        var audioButtons = $(".audios-" + enslavedId).find('button');

        $.each(audioButtons, function(){
            var elementId = $(this).data('audio-id');
            var recordItem = elementId.replace(/_/g, '.');

            var audioItem = $('#'+elementId);
            if (audioItem.length === 0) {
                audioItem = $('<audio id="'+elementId+'" src="'+STATIC_URL+'recordings/'+recordItem+'">'+
                    gettext("Your browser doesn't support <code>audio</code> tags.")+
                    '</audio>');
                audioItem.on('ended', function(){
                    var audioId = $(this)[0].id;
                    $('[data-audio-id="'+audioId+'"]').removeClass('fa fa-spinner fa-spin').addClass('far fa-play-circle').removeAttr('disabled');
                });
                $('body').append(audioItem);
            }
        });

        $(".audio-player").click(function () {
            $(this).removeClass('far fa-play-circle').addClass('fa fa-spinner fa-spin').attr('disabled', 'disabled');

            document.getElementById($(this).data('audio-id')).play();
        });
    });

    $(".recording-button").click(function(){
        start();
        $(".recording-button").addClass('d-none');
        $(".stop-recording-button").removeClass('d-none');
    });

    $(".stop-recording-button").click(function(){
        stop();
        $(".stop-recording-button").addClass('d-none');
    });

    $(".play-button").click(function(){
        var audio = $(this).parent().siblings('audio')[0]

        if ($(this).hasClass('fa-play-circle')) {
            $(this).removeClass('fa-play-circle');
            $(this).addClass('fa-stop');
            audio.play();
        } else {
            $(this).removeClass('fa-stop');
            $(this).addClass('fa-play-circle');
            audio.pause();
            audio.currentTime = 0;
        }

        // Prevent Default Action
        return false;
    });

    mymap = L.map('mapid').setView([0.57128, 15.829786], 3);

    $(".btn-next-section").click(function(){
        $('#pills-profile-tab').tab('show');
        return false;
    });

    $(".btn-previous-section").click(function(){
        $('#pills-home-tab').tab('show');
        return false;
    });

    $("#pills-profile-tab").on('shown.bs.tab', function(e) {
      mymap.invalidateSize();
    });

    L.tileLayer('https://{s}.tile.jawg.io/jawg-sunny/{z}/{x}/{y}{r}.png?access-token={accessToken}', {
        attribution: '<a href="http://jawg.io" title="Tiles Courtesy of Jawg Maps" target="_blank">&copy; <b>Jawg</b>Maps</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        minZoom: 0,
        maxZoom: 22,
        subdomains: 'abcd',
        accessToken: 'NHr9dsp5NeloMikhmQAeJiSNxW2QDRz9cHNKGawiDlTdnFR2RvJBqEFbaxSjwRtY'
    }).addTo(mymap);

    geojson = L.geoJson(africaCountriesData, {
        style: style,
        onEachFeature: onEachFeature
    }).addTo(mymap);

});

const req = { audio: true, video: false };
let stopAction = null;
let chunks = [];
let blobs = [];

const soundClips = document.querySelector('.sound-clips');

// THIS IS SAMPLE CODE TO TEST AUDIO RECORDINGS!
function start() {
    navigator.mediaDevices.getUserMedia(req)
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();
            mediaRecorder.ondataavailable = function(e) {
                chunks.push(e.data);
            };
            mediaRecorder.onstop = function(e) {
                var reviewRecording = $('.review-recording');
                var audio = document.getElementById('audio-recording-1');

                const blob = new Blob(chunks, { 'type' : chunks[0].type });
                chunks = [];
                const audioURL = window.URL.createObjectURL(blob);
                audio.src = audioURL;
                audio.addEventListener("loadedmetadata", function () {
                    if(this.duration === Infinity) {
                        this.currentTime = 1e101;
                        this.ontimeupdate = function() {
                            this.ontimeupdate = () => {
                                return;
                            }
                            $(this).siblings('.audio-controls').find('.duration').html(secondsTimeSpanToMS(this.duration));
                            audio.currentTime = 0.1;
                            audio.currentTime = 0;
                        }
                    } else {
                        $(this).siblings('.audio-controls').find('.duration').html(secondsTimeSpanToMS(this.duration));
                    }
                });

                audio.addEventListener('ended', function(){
                    $(this).siblings('.audio-controls').find('.play-button').removeClass('fas fa-stop').addClass('fas fa-play-circle');
                });

                reviewRecording.find('.delete-button').on('click', function(){
                    $(this).closest('.review-recording').addClass('d-none');
                    $(this).closest('.review-recording').siblings('.recording-button').removeClass('d-none');
                    return false;
                });

                reviewRecording.removeClass('d-none');
            };

            stopAction = function() {
                var track = stream.getTracks()[0];
                track.stop();
                mediaRecorder.stop();
            };
        })
        .catch(err => alert('Cannot start mic'));
}

function stop() {
    if (stopAction) {
        stopAction();
    }
}

function secondsTimeSpanToMS(s) {
    s = parseInt(s, 10);
    var m = Math.floor(s/60); //Get remaining minutes
    s -= m*60;
    return (m < 10 ? '0'+m : m)+":"+(s < 10 ? '0'+s : s); //zero padding on minutes and seconds
}
