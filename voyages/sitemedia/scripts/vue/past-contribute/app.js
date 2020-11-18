// main app
var pastContribute = new Vue({
    el: "#past-contribute",
    delimiters: ["[[", "]]"],
    data: {
        enslaved: {},
        total_names: 0,
        recordings_content: '',
        audioList: {},
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

$(function(){
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
});
