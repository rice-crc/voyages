// main app
var pastContribute = new Vue({
    el: "#past-contribute",
    delimiters: ["[[", "]]"],
    data: function(){
        return {
            enslaved: {},
            recordings_content: '',
            names_suggestions: [{
                name: '',
                notes: '',
                recording: null,
            }],
            audioList: [],
            language_groups: new TreeselectVariable({
                    varName: "language_groups",
                    label: gettext("Language Group"),
                    description: "",
                },{
                    op: "is one of",
                    searchTerm: [],
                },{
                    isImputed: false,
                    isadvanced: false,
                    disableBranchNodes: true,
                    maxLength: 2,
                }),
            notes: '',
            filterData: {
              treeselectOptions: {
              }
            },
            row: {
              // store current row's data; used for displaying entry full details
              data: null,
              collapseVisible: true
            },
            rowModalShow: false
        };
    },
    computed: {
        filledNamesSuggestions() {
            return this.names_suggestions.filter(function(name_suggestion){
                return name_suggestion.name != '';
            });
        },
        hasMoreThanOneSuggestion() {
            return this.names_suggestions.length > 1;
        }
    },
    watch: {
        // row in a datatable
        row: {
          handler: function() {
            var results = [];
            var rowData = this.row.data;
            voyageColumns.forEach(function(group, key){
              if (group.group !== "year") {
                var datum = {
                  group: group.group,
                  groupName: group.groupName,
                  variables: {}
                };
                group.fields.forEach(function(field, key){
                  var varName = field.data;
                  var label = field.label !== undefined ? field.label : field.data;
                  var value = rowData[varName];
                  var isImputed = field.isImputed !== undefined ? field.isImputed : false;

                  if (varName.indexOf('percentage') != -1 || varName.indexOf('mortality') != -1) {
                    value = roundDecimal(value * 100, 1) + "%";
                  }
                  else if (varName == 'var_sources') {
                    value = getVoyageFormattedSource(value);
                  }

                  datum.variables[varName] = {
                    varName: varName,
                    label: label,
                    value: value,
                    isImputed: isImputed
                  };
                });
                results.push(datum);
              }
            });
            this.row.results = results;

            // collect ids for the group collapse. there might be a better way
            var ids = "";
            for (group in this.row.results) {
              ids = ids + this.row.results[group]["group"] + ".";
            }
            this.row.ids = ids.slice(0, -1);
          },
          deep: true
        },
    },
    methods: {
        // toggle whether language group is multilingual
        toggleIsMultilingual() {
          this.language_groups.options.isMultiple = !this.language_groups.options.isMultiple;
          if (!this.language_groups.options.isMultiple) {
              this.language_groups.label = gettext("Primary language group (Optional)");
          } else {
              this.language_groups.label = gettext("Language Group");
          }
        },

        sendContribution() {
            var contrib_languages = [];
            if (Array.isArray(this.language_groups.value.searchTerm)) {
                $.each(this.language_groups.value.searchTerm, function(key, value){
                    contrib_languages.push({
                        ethnicity_id: "1",
                        lang_group_id: value.slice(value.indexOf('-') + 1),
                    });
                });
            } else {
                var value = this.language_groups.value.searchTerm;
                value = value.slice(value.indexOf('-') + 1);
                contrib_languages.push({
                    ethnicity_id: "1",
                    lang_group_id: value,
                });
            }

            var params = {
                enslaved_id: this.enslaved.enslaved_id,
                contrib_names: this.filledNamesSuggestions.map(({name, notes}) => ({name, notes})),
                contrib_languages: contrib_languages,
                notes: this.notes,
                is_multilingual: !this.language_groups.options.isMultiple
            }

            axios
            .post('/past/enslaved_contribution', params)
            .then((response) => {
                var promises = response.data.name_ids.map((value, key) => {
                    var recording = this.filledNamesSuggestions[key].recording;
                    if (recording instanceof Blob) {
                        return axios
                        .post('/past/store-audio/'+response.data.contrib_id+'/'+value+'/'+response.data.audio_token, recording);
                    }
                });
                var filteredPromises = promises.filter((value) => value);

                return Promise.all(filteredPromises);
            })
            .then((response) => {
                alert("Contribution saved with success");
                document.location = '/past/database';
            })
            .catch(function(error) {
                return error;
            });
        },

        changed(variable, changed) {
            this.language_groups.changed = changed;
            this.language_groups.value["searchTerm"] = variable["searchTerm"];
            this.language_groups.value["op"] = variable["op"];
        },
        openVoyageModal() {
          var columns = [];
          voyageColumns.forEach(function(group, key){
            group.fields.forEach(function(field, key){
              columns.push(field);
            });
          });
          var params = {
            "searchData": {
              "items": [
                {
                  "op": "equals",
                  "varName": "voyage_id",
                  "searchTerm": this.enslaved.voyage__id,
                },
                {
                  "op": "equals",
                  "varName": "dataset",
                  "searchTerm": "-1",
                }
              ]
            },
            "tableParams": {
              "columns": columns
            },
            "output" : "resultsTable"
          };

          axios
            .post('/voyage/api/search', params)
            .then(function(response) {
              if (response.data.data[0]) {
                pastContribute.row.data = response.data.data[0];
                pastContribute.rowModalShow = true;
              }
              return;
            })
            .catch(function(error) {
              return error;
            });
        },
        addSuggestion(){
            this.names_suggestions.push( { name: '', notes: '', recording: null} );
        },
        removeSuggestion(index){
            this.names_suggestions.splice(index, 1);
        }
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
        .then(function() {
            geoJsonAddMarker();
        })
        .catch(function(error) {
            return error;
        });
    }
});

function highlightFeature(e) {
    highlightLayer(e.target);
}

function highlightLayer(layer) {
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
    resetLayer(e.target);
}

function resetLayer(layer) {
    geojson.resetStyle(layer);
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
    layer._leaflet_id = feature.properties.name;
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

var geoJsonAddMarker = function() {
    var marker = L.marker({
        lat: pastContribute.enslaved.voyage__voyage_itinerary__imp_principal_place_of_slave_purchase__latitude,
        lng: pastContribute.enslaved.voyage__voyage_itinerary__imp_principal_place_of_slave_purchase__longitude
    });
    marker.addTo(mymap);
};
var geojson;
var mymap;

$(function(){
    $(".vue-treeselect").on("mouseover", ".vue-treeselect__indent-level-1 > .vue-treeselect__option", function(){
        var name = $($(this)[0]).text();
        var layer = geojson.getLayer(name);
        highlightLayer(layer);
    });

    $(".vue-treeselect").on("mouseleave", ".vue-treeselect__indent-level-1 > .vue-treeselect__option", function(){
        var name = $($(this)[0]).text();
        var layer = geojson.getLayer(name);
        resetLayer(layer);
    });

    $(".vue-treeselect").on("mouseover", ".vue-treeselect__indent-level-2 > .vue-treeselect__option", function(){
        var layer = geojson.getLayer($(this).closest('.vue-treeselect__indent-level-1').find('.vue-treeselect__option').data('id'));
        highlightLayer(layer);
    });

    $(".vue-treeselect").on("mouseleave", ".vue-treeselect__indent-level-2 > .vue-treeselect__option", function(){
        var layer = geojson.getLayer($(this).closest('.vue-treeselect__indent-level-1').find('.vue-treeselect__option').data('id'));
        resetLayer(layer);
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

    mymap = L.map('mapid', {
        maxBounds: [
            [37.901314, -31.447038],
            [-37.665391, 60.728849]
        ],
        maxBoundsViscosity: 1.0,
        center: [0.57128, 15.829786],
        zoom: 3,
        minZoom: 3,
    });
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

    L.tileLayer('https://{s}.tile.jawg.io/jawg-sunny/{z}/{x}/{y}{r}.png?lang=en&access-token={accessToken}', {
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
