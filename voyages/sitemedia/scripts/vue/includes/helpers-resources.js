// reserved keyword for saved search query identifier
const SAVED_SEARCH_LABEL = "#searchId=";
const SEARCH_URL = "api/search";

// process search data returned from the API
function processResponse(json) {
  var data = [];
  json.data.forEach(function(row) {
    var arrivalDateArray = row.voyage__voyage_dates__first_dis_of_slaves ? row.voyage__voyage_dates__first_dis_of_slaves.split([',']) : '';
    var arrivalDate = '';
    var arrivalYear = '';
    var arrivalMonth = '';
    var arrivalDay = '';

    if (arrivalDateArray.length == 3) {
      arrivalMonth = arrivalDateArray[0];
      arrivalDay = arrivalDateArray[1];
      arrivalYear = arrivalDateArray[2];
      if (arrivalMonth && arrivalDay) {
        arrivalDate = arrivalMonth + '/' + arrivalDay + '/' + arrivalYear;
      } else {
        arrivalDate = arrivalYear;
      }
    } else if (arrivalDateArray.length == 1) {
      arrivalDate = arrivalDateArray[0];
    }
    row.voyage__voyage_dates__first_dis_of_slaves = arrivalDate;

    var gender = '';
    if (row.gender == 1) {
      gender = gettext("Male");
    } else if (row.gender == 2) {
      gender = gettext("Female");
    }
    row.gender = gender;

    // row.source = getFormattedSourceInTable(row.source);

    data.push(row);
  });

  return data;
}

/**
 * Add space between camelCase text.
 */
function unCamelCase(str) {
  str = str.replace(/([a-z\xE0-\xFF])([A-Z\xC0\xDF])/g, "$1 $2");
  str = str.toLowerCase(); //add space between camelCase text
  return str;
}

/**
 * UPPERCASE first char of each sentence and lowercase other chars.
 */
function sentenceCase(str) {
  // Replace first char of each sentence (new line or after '.\s+') to
  // UPPERCASE
  return unCamelCase(str).replace(/(^\w)|\.\s+(\w)/gm, upperCase);
}

// get formated source by parsing through the backend response
// returns the format for table display
// ABCD - [Tooltip: details]
function getFormattedSourceInTable(sources) {
  var value = ""; // empty value string
  sources.forEach(function(source) {
    var first = source.split("<>")[0];
    var second = source.split("<>")[1];
    value +=
      "<div><span data-toggle='tooltip' data-placement='top' data-html='true' data-original-title='" +
      second +
      "'>" +
      first +
      "</span>";
  });
  return value;
}

// solr date format
const SOLR_DATE_FORMAT = "YYYY-MM-DDThh:mm:ss[Z]";

// get language for datatables
var dtLanguage = {};
if (LANGUAGE_CODE == "es") {
  dtLanguage = {
    url: "//cdn.datatables.net/plug-ins/1.10.19/i18n/Spanish.json"
  };
} else if (LANGUAGE_CODE == "pt") {
  dtLanguage = {
    url: "//cdn.datatables.net/plug-ins/1.10.19/i18n/Portuguese.json"
  };
}

// variableMapping
// used for loading a variable (variables extracted from a saved query ==> variables in the vm filter object)
var variableMapping = {

};

// mark a variable as changed and activated state
function activateFilter(filter, group, subGroup, filterValues) {
  for (key1 in filter[group][subGroup]) {
    if (key1 !== "count") {
      if (filter[group][subGroup][key1].changed) {
        filter[group][subGroup][key1].changed = true;
        filter[group][subGroup][key1].activated = true;
      } else {
        filter[group][subGroup][key1].changed = false;
        filter[group][subGroup][key1].activated = false;
      }
    }
  }
}

// reset filter
function resetFilter(filter, group, subGroup) {
  for (key in filter[group][subGroup]) {
    if (key !== "count") {
      if (filter[group][subGroup][key].value["searchTerm0"] === undefined) {
        // has only one search term
        filter[group][subGroup][key].value["searchTerm"] =
          filter[group][subGroup][key].default["searchTerm"];
      } else {
        // has two search terms
        filter[group][subGroup][key].value["searchTerm0"] =
          filter[group][subGroup][key].default["searchTerm0"];
        filter[group][subGroup][key].value["searchTerm1"] =
          filter[group][subGroup][key].default["searchTerm1"];
      }
      filter[group][subGroup][key].value["op"] =
        filter[group][subGroup][key].default["op"];
      filter[group][subGroup][key].changed = false;
      filter[group][subGroup][key].activated = false;
    }
  }
}

// serialize a filter
function serializeFilter(filter) {
  return JSON.stringify(filter);
}

function searchAll(filter, filterData) {
  var items = {};
  for (key1 in filter) {
    if (key1 !== "count") {
      for (key2 in filter[key1]) {
        if (key2 !== "count") {
          for (key3 in filter[key1][key2]) {
            if (key3 !== "count") {
              if (filter[key1][key2][key3].activated) {
                var item = {};
                var searchTerm = [];
                if (
                  filter[key1][key2][key3].value["searchTerm0"] === undefined
                ) {
                  // if it's a multi-tiered place variable
                  if (
                    filter[key1][key2][key3].constructor.name ===
                    "PlaceVariable"
                  ) {
                    var sortedSelections = filter[key1][key2][key3].value[
                      "searchTerm"
                    ].sort(sortNumber);
                    var searchTerm = [];

                    sortedSelections.forEach(function(selection) {
                      var varName = filter[key1][key2][key3]["varName"];
                      if (
                        selection == filterData.treeselectOptions[varName][0].id
                      ) {
                        // select all
                        filterData.treeselectOptions[
                          varName
                        ][0].children.forEach(function(broadRegion) {
                          broadRegion.children.forEach(function(region) {
                            region.children.forEach(function(subRegion) {
                              searchTerm.push(subRegion.id);
                            });
                          });
                        });
                      } else {
                        // broadRegion
                        filterData.treeselectOptions[
                          varName
                        ][0].children.forEach(function(broadRegion) {
                          if (selection == broadRegion.id) {
                            broadRegion.children.forEach(function(region) {
                              region.children.forEach(function(subRegion) {
                                searchTerm.push(subRegion.id);
                              });
                            });
                          } else {
                            broadRegion.children.forEach(function(region) {
                              // region
                              if (selection == region.id) {
                                region.children.forEach(function(subRegion) {
                                  searchTerm.push(subRegion.id);
                                });
                              } else {
                                // subRegion
                                region.children.forEach(function(subRegion) {
                                  if (selection == subRegion.id) {
                                    searchTerm.push(subRegion.id);
                                  }
                                });
                              }
                            });
                          }
                        });
                      }
                    });

                    item["searchTerm"] = searchTerm;

                    // if it's a TreeselectVariable
                  } else if (
                    filter[key1][key2][key3].constructor.name ===
                    "TreeselectVariable"
                  ) {
                    var sortedSelections = filter[key1][key2][key3].value[
                      "searchTerm"
                    ].sort(sortNumber);
                    var searchTerm = [];

                    if (sortedSelections.includes("0")) {
                      // select all
                      filterData.treeselectOptions[varName][0].children.forEach(
                        function(options) {
                          searchTerm.push(options.id);
                        }
                      );
                    } else {
                      searchTerm = filter[key1][key2][key3].value["searchTerm"];
                    }

                    item["searchTerm"] = searchTerm;
                  } else if (
                    filter[key1][key2][key3].constructor.name ===
                    "PercentageVariable"
                  ) {
                    item["searchTerm"] =
                      parseInt(filter[key1][key2][key3].value["searchTerm"]) /
                      100;
                  } else {
                    item["searchTerm"] =
                      filter[key1][key2][key3].value["searchTerm"];
                  }
                } else {
                  item["searchTerm"] = [
                    filter[key1][key2][key3].value["searchTerm0"],
                    filter[key1][key2][key3].value["searchTerm1"]
                  ];

                  // patch for date variables
                  if (
                    filter[key1][key2][key3].constructor.name === "DateVariable"
                  ) {
                    // if user chose to search against a particular day, make sure it is searching against a range
                    // i.e. add 23:59:59 to searchTerm0
                    if (filter[key1][key2][key3].value["op"] == "is equal to") {
                      filter[key1][key2][key3].value["searchTerm1"] = filter[
                        key1
                      ][key2][key3].value["searchTerm0"].substring(0, 10);
                      filter[key1][key2][key3].value["searchTerm0"] =
                        filter[key1][key2][key3].value["searchTerm1"].replace(
                          "/",
                          "-"
                        ) + "T00:00:00Z";
                      filter[key1][key2][key3].value["searchTerm1"] =
                        filter[key1][key2][key3].value["searchTerm1"] +
                        "T23:59:59Z";
                    }
                    // make the to date always inclusive (add 23:59:59)
                    if (
                      filter[key1][key2][key3].value["searchTerm1"] !== null
                    ) {
                      if (
                        filter[key1][key2][key3].value["searchTerm0"].substring(
                          0,
                          10
                        ) !=
                        filter[key1][key2][key3].value["searchTerm1"].substring(
                          0,
                          10
                        )
                      ) {
                        // filter[key1][key2][key3].value["searchTerm1"] = moment(filter[key1][key2][key3].value["searchTerm1"], SOLR_DATE_FORMAT).add(1, "days").subtract(1, "seconds");
                        filter[key1][key2][key3].value["searchTerm1"] =
                          filter[key1][key2][key3].value["searchTerm1"].replace(
                            "/",
                            "-"
                          ) + "T23:59:59Z";
                      }
                    }
                    item["searchTerm"] = [
                      filter[key1][key2][key3].value["searchTerm0"],
                      filter[key1][key2][key3].value["searchTerm1"]
                    ];
                  }

                  // patch for percentage variables
                  if (
                    filter[key1][key2][key3].constructor.name ===
                    "PercentageVariable"
                  ) {
                    var searchTerm0 =
                      parseInt(filter[key1][key2][key3].value["searchTerm0"]) /
                      100;
                    var searchTerm1 =
                      parseInt(filter[key1][key2][key3].value["searchTerm1"]) /
                      100;
                    item["searchTerm"] = [searchTerm0, searchTerm1];
                  }

                  if (
                    filter[key1][key2][key3].constructor.name ===
                    "NumberVariable"
                  ) {
                    var searchTerm0 = 0;
                    var searchTerm1 = 999999;
                    switch (filter[key1][key2][key3].value["op"]){
                      case "is equal to":
                        searchTerm0 = searchTerm1 = filter[key1][key2][key3].value["searchTerm0"];
                      break;
                      case "is at most":
                        searchTerm1 = filter[key1][key2][key3].value["searchTerm0"];
                      break;
                      case "is at least":
                        searchTerm0 = filter[key1][key2][key3].value["searchTerm0"];
                      break;
                    }

                    item["searchTerm"] = [
                      searchTerm0,
                      searchTerm1
                    ];
                  }
                }

                items[filter[key1][key2][key3].varName] = item["searchTerm"];
              }
            }
          }
        }
      }
    }
  }

  return items;
}

function processPlacesAjax(data) {
  var self = {};
  // Process data.
  // Here we assume that the data is properly
  // order so that each port appears after the
  // region that it belongs to and the region
  // appears after the broad region it belongs to.
  var broadRegions = {};
  var regions = {};
  var ports = {};
  var allDict = {};
  for (var i = 0; i < data.length; ++i) {
    var item = data[i];
    if (item.type == "port") {
      item.region = regions[item.parent];
      item.pk = item.value;
      item.label = item.port;
      ports[item.value] = item;
    } else if (item.type == "region") {
      item.broad_region = broadRegions[item.parent];
      item.label = item.region;
      item.ports = [];
      regions[item.pk] = item;
    } else if (item.type == "broad_region") {
      item.label = item.broad_region;
      item.ports = [];
      broadRegions[item.pk] = item;
    }
    allDict[item.value] = item;
  }
  for (var key in ports) {
    var p = ports[key];
    var r = p.region;
    var b = r.broad_region;
    r.ports.push(p.code);
    b.ports.push(p.code);
  }
  self.isLoaded = true;
  self.all = data;
  self.allDict = allDict;
  self.broadRegions = broadRegions;
  self.regions = regions;
  self.ports = ports;
  return self;
}

// get treeselect variable labels of currently selected items
function getTreeselectLabel(currentVariable, searchTerms, treeselectOptions) {
  labels = [];

  if (currentVariable.constructor.name == "TreeselectVariable") {
    treeselectOptions = treeselectOptions[currentVariable.varName];
    searchTerms.forEach(function(searchTerm) {
      treeselectOptions.forEach(function(treeselectOption) {
        if (treeselectOption.value == searchTerm) {
          labels.push(treeselectOption.label);
        }
      });
    });
  } else if (currentVariable.constructor.name == "PlaceVariable") {
    treeselectOptions = treeselectOptions[currentVariable.varName][0];
    searchTerms.forEach(function(searchTerm) {
      if (searchTerm == treeselectOptions.id) {
        // ALL SELECTED
        labels.push(treeselectOptions.label);
      } else {
        if (treeselectOptions.children !== undefined) {
          // BROARD REGION
          broadRegions = treeselectOptions.children;
          broadRegions.forEach(function(broadRegion) {
            if (searchTerm == broadRegion.id) {
              labels.push(broadRegion.label);
            } else {
              if (broadRegion.children !== undefined) {
                // REGION
                regions = broadRegion.children;
                regions.forEach(function(region) {
                  if (searchTerm == region.id) {
                    labels.push(region.label);
                  } else {
                    // SUB REGION
                    if (region.children !== undefined) {
                      // SUB REGION
                      subRegions = region.children;
                      subRegions.forEach(function(subRegion) {
                        if (searchTerm == subRegion.id) {
                          labels.push(subRegion.label);
                        }
                      });
                    }
                  }
                });
              }
            }
          });
        }
      }
    });
  }

  return labels;
}

// load treeselect options
function loadTreeselectOptions(vm, vTreeselect, filter, callback) {
  var varName = filter.varName;
  var loadType = filter.type;

  // load only once remotely and then local copy
  if (!vm.filterData.treeselectOptions[varName]) {
    if (loadType == "place") {
      var apiUrl = '/voyage/filtered-places';
      switch (varName) {
        case 'embarkation_ports':
          var params = {var_name: 'imp_principal_place_of_slave_purchase_id'};
          break;

        case 'disembarkation_ports':
        case 'intended_disembarkation_port':
        case 'post_disembarkation_location':
          var params = {var_name: 'imp_principal_port_slave_dis_id'};
          break;

        default:
          callback("Error: varName " + varName + " is not acceptable");
          return false;
      }

      axios
        .post(apiUrl, params)
        .then(function(response) {
          var options = parsePlaces(response);
          vm.filterData.treeselectOptions[varName] = options;
          vTreeselect.treeselectOptions = vm.filterData.treeselectOptions[varName];
          callback(); // notify vue-treeselect about data population completion
          return;
        })
        .catch(function(error) {
          options.errorMessage = error;
          $("#sv-loader").addClass("display-none");
          $("#sv-loader-error").removeClass("display-none");
          return error;
        });
    }

    // load TreeselectVariable
    else if (loadType == "treeselect") {
      switch (varName) {
        case 'register_country':
        case 'modern_country':
          var apiUrl = '/past/api/modern-countries';
          break;
        case 'ethnicity':
          var apiUrl = '/past/api/ethnicities';
          break;
        case 'language_groups':
          var apiUrl = '/past/api/language-groups';
          break;
        default:
          callback("Error: varName " + varName + " is not acceptable");
          return false;
      }

      axios
        .post(apiUrl)
        .then(function(response) {
          var options = [];
          switch (varName) {
            case 'register_country':
            case 'modern_country':
              var options = parseCountries(response);
              break;
            case 'ethnicity':
              var options = parseEthnicities(response);
              break;
            case 'language_groups':
              var options = parseLanguageGroups(response);
              break;
          }

          vm.filterData.treeselectOptions[varName] = options;
          vTreeselect.treeselectOptions = vm.filterData.treeselectOptions[varName];

          callback(); // notify vue-treeselect about data population completion
          return;
        })
        .catch(function(error) {
          options.errorMessage = error;
          $("#sv-loader").addClass("display-none");
          $("#sv-loader-error").removeClass("display-none");
          return error;
        });
    }

    // load weird place variables
    else {
      callback("Error loading options");
    }
  }

  vTreeselect.treeselectOptions = vm.filterData.treeselectOptions[varName];
  callback(); // notify vue-treeselect about data population completion
}

// parsePlaces function
var parsePlaces = function(response) {
  var data = processPlacesAjax(response.data.data);
  // fill select all
  var options = [
    {
      id: 0,
      code: 0,
      label: gettext("Select All"),
      children: []
    }
  ];

  // sort regions by order
  data.regions = Object.keys(data.regions)
    .sort(function(a, b) {
      return data.regions[a].order - data.regions[b].order;
    })
    .map(key => data.regions[key]); // sort data.regions by "order" attribute

  // fill broad regions
  for (key in data.broadRegions) {
    options[0].children.push({
      id: data.broadRegions[key].order,
      label: data.broadRegions[key].broad_region,
      children: []
    });
  }

  // build regions
  for (regionId in data.regions) {
    var broadRegion = data.regions[regionId].broad_region;
    for (broadRegionId in options[0].children) {
      if (options[0].children[broadRegionId].id == broadRegion.order) {
        options[0].children[broadRegionId].children.push({
          id: data.regions[regionId].code,
          label: data.regions[regionId].region,
          children: []
        });
      }
    }
  }

  // fill ports
  data.ports = Object.keys(data.ports)
    .sort(function(a, b) {
      return data.ports[a].order - data.ports[b].order;
    })
    .map(key => data.ports[key]); // sort data.ports by "order" attribute

  for (portId in data.ports) {
    // get basic information about a port
    var value = data.ports[portId].value;
    var label = data.ports[portId].port;
    var regionId = data.ports[portId].region.code;
    var broadRegionId = data.ports[portId].region.broad_region.order;

    // locate corresponding location in the options tree
    options[0].children.map(function(broadRegion) {
      if (broadRegion.id == broadRegionId) {
        broadRegion.children.map(function(region) {
          if (region.id == regionId) {
            // in the correct region
            region.children.push({
              // fill port
              id: value,
              label: label
            });
          }
        });
      }
    });
  }
  return options;
};

// parseCountries function
var parseCountries = function(response) {
  var options = [];
  $.each(response.data, function(id, country) {
    options.push({'id': id, 'label' : country});
  });
  return options;
}

// parseLanguageGroups function
var parseLanguageGroups = function(response) {
  // fill select all
  var options = [
    {
      id: 0,
      code: 0,
      label: gettext("Select All"),
      children: []
    }
  ];

  // fill countries
  var countries = {};
  $.each(response.data, function(id, languageGroup) {
    countries[languageGroup.country] = languageGroup.country;
  });
  $.each(countries, function(key, country) {
    options[0].children.push({
      id: country,
      label: country,
      children: []
    });
  });

  // fill languageGroups
  $.each(response.data, function(id, languageGroup) {
    var label = languageGroup.name;
    if (languageGroup.alts.length > 0) {
      var altNames = [];
      $.each(languageGroup.alts, function(id, altName) {
        altName = altName.trim();
        if (altName != languageGroup.name) {
          altNames.push(altName);
        }
      });
      if (altNames.length > 0) {
        label += ' (' + altNames.join(', ') + ')';
      }
    }
    $.each(options[0].children, function(key, country) {
      if (languageGroup.country == country.label) {
        options[0].children[key].children.push({'id': id, 'label' : label});
      }
    });
  });

  return options;
}

// parseEthnicities function
var parseEthnicities = function(response) {
  var options = [];
  $.each(response.data, function(id, ethnicity) {
    var label = ethnicity.name;

    /*
      ethnicity.language_group_id is not been used yet
    */

    if (ethnicity.alts.length > 0) {
      var altNames = [];
      $.each(ethnicity.alts, function(id, altName) {
        altName = altName.trim();
        if (altName != ethnicity.name) {
          altNames.push(altName);
        }
      });
      if (altNames.length > 0) {
        label += ' (' + altNames.join(', ') + ')';
      }
    }
    options.push({'id': id, 'label' : label});
  });
  return options;
}

function sortNumber(a, b) {
  return a - b;
}

function refreshUi(filter, filterData, currentTab, tabData, options) {
  var currentSearchObj = searchAll(filter, filterData);

  if (currentTab == "results") {
    // Results DataTable
    var pageLength = {
      extend: "pageLength",
      className: "btn btn-info buttons-collection dropdown-toggle"
    };
    var mainDatatable = $("#results_main_table").DataTable({
      ajax: {
        url: SEARCH_URL,
        type: "POST",
        data: function(d) {
          if (d.order[0] != undefined) {
            var order = d.order[0];
            currentSearchObj['order_by'] = {
              'column' : d.columns[order['column']].data,
              'dir' : order['dir']
            };
          }

          return JSON.stringify({
            search_query: currentSearchObj,
            tableParams: d,
            output: "resultsTable"
          });
        },

        // preprocess the returned data
        // a - to use % instead of decimals (e.g. 30% vs. 0.30)
        // b - to format source into HTML decorated string
        dataSrc: function(json) {
          return processResponse(json);
        },

        fail: function(xhr, status, error) {
          options.errorMessage = error;
          $("#sv-loader").addClass("display-none");
          $("#sv-loader-error").removeClass("display-none");
        }
      },

      scrollX: true,

      // colReorder: true,

      // columnDefs: [
      //   {
      //     width: "25%",
      //     targets: 0
      //   },
      //   {
      //     width: "25%",
      //     targets: 1
      //   },
      //   {
      //     width: "25%",
      //     targets: 2
      //   },
      //   {
      //     width: "25%",
      //     targets: 3
      //   }
      // ],

      order: [[0, "asc"]],
      destroy: true,

      // page length Default
      pageLength: 15,

      // dom: 'ifrtBp',
      dom:
        "<'flex-container'iB>" +
        "<'row'<'col-sm-12'tr>>" +
        "<'row'<'col-sm-5'><'col-sm-7'p>>",
      lengthMenu: [
        [15, 50, 100, 200],
        ["15 rows", "50 rows", "100 rows", "200 rows"]
      ],

      language: dtLanguage,

      buttons: [
        columnToggleMenu,
        pageLength,
        // {
        //   extend: "collection",
        //   text:
        //     '<span class="fa fa-columns" style="vertical-align: middle;"></span>',
        //   className: "btn btn-info buttons-collection dropdown-toggle",
        //   text: gettext("Download"),
        //   titleAttr: gettext("Download results"),
        //   // Top level: CSV vs. Excel
        //   buttons: [
        //     {
        //       extend: "collection",
        //       text: "CSV",
        //       buttons: [
        //         {
        //           text: gettext("All results with all columns"),
        //           action: makeDownloadFunction(false, false, false)
        //         },
        //         {
        //           text: gettext("All results with visible columns"),
        //           action: makeDownloadFunction(false, false, true)
        //         },
        //         {
        //           text: gettext("Filtered results with all columns"),
        //           action: makeDownloadFunction(false, true, false)
        //         },
        //         {
        //           text: gettext("Filtered results with visible columns"),
        //           action: makeDownloadFunction(false, true, true)
        //         }
        //       ]
        //     },

        //     {
        //       extend: "collection",
        //       text: "Excel",
        //       buttons: [
        //         {
        //           text: gettext("All results with all columns"),
        //           action: makeDownloadFunction(true, false, false)
        //         },
        //         {
        //           text: gettext("All results with visible columns"),
        //           action: makeDownloadFunction(true, false, true)
        //         },
        //         {
        //           text: gettext("Filtered results with all columns"),
        //           action: makeDownloadFunction(true, true, false)
        //         },
        //         {
        //           text: gettext("Filtered results with visible columns"),
        //           action: makeDownloadFunction(true, true, true)
        //         }
        //       ]
        //     }
        //   ]
        // }
      ],
      //pagingType: "input",
      bFilter: false,
      processing: true,
      serverSide: true,
      columns: allColumns,
      stateSave: true,
      stateDuration: -1,
      initComplete: function() {
        $('[data-toggle="tooltip"]').tooltip();
      }
    });

    // built for the datatable download dropdown menu
    function makeDownloadFunction(isExcel, isFiltered, isVisibleColumns) {
      return function() {
        // TODO (20190710): Remove the next few lines when proper column
        // headers and a canonical order are defined for the download.
        if (!isVisibleColumns) {
          alert("The download option with all columns is not available yet.");
          return;
        }
        // decides if it's returning visible columns or all columns
        var visibleColumns = isVisibleColumns
          ? mainDatatable.columns().visible().context[0].aoColumns.map(function(variable){if (variable.bVisible) return variable.data }).filter(Boolean)
          : [];

        var form = $(
          "<form action='api/download' method='post'>{% csrf_token %}</form>"
        );
        form.append(
          $("<input name='data' type='hidden'></input>").attr(
            "value",
            JSON.stringify({
              searchData: isFiltered ? currentSearchObj : { items: [] }, // decides if it's returning filtered data or all data

              cols: visibleColumns,
              excel_mode: !!isExcel // make sure it's a true boolean variable
            })
          )
        );
        form
          .appendTo("body")
          .submit()
          .remove();
      };
    }
  }

}

// helpers

var loader = new LazyLoader();

// Helper to load CSS files and scripts on demand.
function LazyLoader() {
  var self = this;
  self.loadedFiles = {};
  self.loadCss = function(url) {
    $("head").append(
      '<link rel="stylesheet" href="' + url + '" type="text/css" />'
    );
  };
  self.loadScript = function(url) {
    var dfd = new $.Deferred();
    var callback = function() {
      dfd.resolve("script loaded");
      self.loadedFiles[url] = true;
    };
    if (self.loadedFiles.hasOwnProperty(url)) {
      callback();
    } else {
      var script = document.createElement("script");
      script.type = "text/javascript";
      script.async = false;
      script.onreadystatechange = callback;
      script.onload = callback;
      script.src = url;
      document.getElementsByTagName("head")[0].appendChild(script);
    }
    return dfd;
  };
  return self;
}
