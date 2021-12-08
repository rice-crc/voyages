// reserved keyword for saved search query identifier
const SAVED_SEARCH_LABEL = "#searchId=";
const TRANS_PATH = "past-db/";
const SEARCH_URL = "api/search";

var voyageColumns = [
  {
    group : 'ship_nation_owner',
    groupName : gettext('Ship, Nation, Owners'),
    fields : [
      { data: "var_voyage_id", label: gettext("Voyage ID"), isImputed: false },
      { data: "var_ship_name", label: gettext("Vessel name"), isImputed: false },
      { data: "var_owner", label: gettext("Vessel owner"), isImputed: false },
      { data: "var_nationality", label: gettext("Flag"), isImputed: false },
      { data: "var_imputed_nationality", label: gettext("Flag (imputed)"), isImputed: true },
      { data: "var_vessel_construction_place_lang", label: gettext("Place constructed"), isImputed: false },
      { data: "var_year_of_construction", label: gettext("Year constructed"), isImputed: false },
      { data: "var_registered_place_lang", label: gettext("Place registered"), isImputed: false },
      { data: "var_registered_year", label: gettext("Year registered"), isImputed: false },
      { data: "var_rig_of_vessel", label: gettext("Rig of vessel"), isImputed: false },
      { data: "var_tonnage", label: gettext("Tonnage"), isImputed: false },
      { data: "var_tonnage_mod", label: gettext("Standardized tonnage"), isImputed: true },
      { data: "var_guns_mounted", label: gettext("Guns mounted"), isImputed: false }
    ]
  },
  {
    group : 'outcome',
    groupName : gettext('Outcome'),
    fields : [
      { data: "var_outcome_voyage_lang", label: gettext("Particular outcome of voyage"), isImputed: false },
      { data: "var_outcome_slaves_lang", label: gettext("Outcome of voyage for slaves"), isImputed: false },
      { data: "var_outcome_ship_captured_lang", label: gettext("Outcome of voyage if ship captured"), isImputed: false },
      { data: "var_outcome_owner_lang", label: gettext("Outcome of voyage for owner"), isImputed: false },
      { data: "var_resistance_lang", label: gettext("African resistance"), isImputed: false }
    ]
  },
  {
    group : 'itinerary',
    groupName : gettext('Itinerary'),
    fields : [
      { data: "var_imp_port_voyage_begin_lang", label: gettext("Place where voyage began"), isImputed: true },
      { data: "var_imp_principal_place_of_slave_purchase_lang", label: gettext("Principal place of slave purchase"), isImputed: true },
      { data: "var_first_place_slave_purchase_lang", label: gettext("1st place of slave purchase"), isImputed: false },
      { data: "var_second_place_slave_purchase_lang", label: gettext("2nd place of slave purchase"), isImputed: false },
      { data: "var_third_place_slave_purchase_lang", label: gettext("3rd place of slave purchase"), isImputed: false },
      { data: "var_port_of_call_before_atl_crossing_lang", label: gettext("Places of call before Atlantic crossing"), isImputed: false },
      { data: "var_imp_principal_port_slave_dis_lang", label: gettext("Principal place of slave landing"), isImputed: true },
      { data: "var_first_landing_place_lang", label: gettext("1st place of slave landing"), isImputed: false },
      { data: "var_second_landing_place_lang", label: gettext("2nd place of slave landing"), isImputed: false },
      { data: "var_third_landing_place_lang", label: gettext("3rd place of slave landing"), isImputed: false },
      { data: "var_place_voyage_ended_lang", label: gettext("Place where voyage ended"), isImputed: false }
    ]
  },
  {
    group : 'dates',
    groupName : gettext('Dates'),
    fields : [
      { data: "var_imp_length_home_to_disembark", label: gettext("Voyage length, homeport to disembarkation"), isImputed: false },
      { data: "var_length_middle_passage_days", label: gettext("Middle passage (days)"), isImputed: false },
      { data: "var_imp_arrival_at_port_of_dis", label: gettext("Year of arrival at port of disembarkation "), isImputed: true },
      { data: "var_voyage_began_partial", label: gettext("Date that voyage began"), isImputed: false },
      { data: "var_slave_purchase_began_partial", label: gettext("Date trade began in Africa"), isImputed: false },
      { data: "var_date_departed_africa_partial", label: gettext("Date vessel departed Africa"), isImputed: false },
      { data: "var_first_dis_of_slaves_partial", label: gettext("Date vessel arrived with slaves"), isImputed: false },
      { data: "var_departure_last_place_of_landing_partial", label: gettext("Date vessel departed for homeport"), isImputed: false },
      { data: "var_voyage_completed_partial", label: gettext("Date voyage completed"), isImputed: false }
    ]
  },
  {
    group : 'captain_and_crew',
    groupName : gettext('Captain and Crew'),
    fields : [
      { data: "var_captain", label: gettext("Captain's name"), isImputed: false },
      { data: "var_crew_voyage_outset", label: gettext("Crew at voyage outset"), isImputed: false },
      { data: "var_crew_first_landing", label: gettext("Crew at first landing of slaves"), isImputed: false },
      { data: "var_crew_died_complete_voyage", label: gettext("Crew deaths during voyage"), isImputed: false }
    ]
  },
  {
    group : 'slaves',
    groupName : gettext('Slaves'),
    fields : [
      { data: "var_imp_total_num_slaves_purchased", label: gettext("Total embarked"), isImputed: true },
      { data: "var_total_num_slaves_purchased", label: gettext("Total embarked"), isImputed: false },
      { data: "var_imp_total_slaves_disembarked", label: gettext("Total disembarked"), isImputed: true },
      { data: "var_num_slaves_intended_first_port", label: gettext("Slaves intended at 1st place"), isImputed: false },
      { data: "var_num_slaves_carried_first_port", label: gettext("Slaves carried from 1st port"), isImputed: false },
      { data: "var_num_slaves_carried_second_port", label: gettext("Slaves carried from 2nd port"), isImputed: false },
      { data: "var_num_slaves_carried_third_port", label: gettext("Slaves carried from 3rd port"), isImputed: false },
      { data: "var_total_num_slaves_arr_first_port_embark", label: gettext("Slaves arrived at 1st port"), isImputed: false },
      { data: "var_num_slaves_disembark_first_place", label: gettext("Slaves landed at 1st port"), isImputed: false },
      { data: "var_num_slaves_disembark_second_place", label: gettext("Slaves landed at 2nd port"), isImputed: false },
      { data: "var_num_slaves_disembark_third_place", label: gettext("Slaves landed at 3rd port"), isImputed: false },
      { data: "var_imputed_percentage_men", label: gettext("Percent men"), isImputed: false },
      { data: "var_imputed_percentage_women", label: gettext("Percent women"), isImputed: false },
      { data: "var_imputed_percentage_boys", label: gettext("Percent boys"), isImputed: false },
      { data: "var_imputed_percentage_girls", label: gettext("Percent girls"), isImputed: false },
      { data: "var_imputed_percentage_male", label: gettext("Percent males"), isImputed: false },
      { data: "var_imputed_percentage_child", label: gettext("Percent children"), isImputed: false },
      { data: "var_imputed_sterling_cash", label: gettext("Sterling cash price in Jamaica"), isImputed: false },
      { data: "var_imputed_death_middle_passage", label: gettext("Slaves died during middle passage"), isImputed: false },
      { data: "var_imputed_mortality", label: gettext("Mortality rate"), isImputed: false }
    ]
  },
  {
    group : 'sources',
    groupName : gettext('Source'),
    fields : [
      { data: "var_sources", label: gettext("Source of data"), isImputed: false }
    ]
  }
];

function getColumnIndex(column) {
  var index = null;
  allColumns[enslavedDataset].forEach(function(columnItem, columnIndex) {
    if (columnItem.data == column) {
      index = columnIndex;
      return true;
    }
  });
  return index;
}

// process search data returned from the API
function processResponse(json, mainDatatable, fuzzySearch) {
  var data = [];
  var rankingIndex = getColumnIndex('ranking');

  json.data.forEach(function(row) {
    row.names = $.map(row.names, function(s) { return s.replace(' ', '&nbsp;'); }).join('<br>');

    var arrivalDateArray = row.voyage__voyage_dates__first_dis_of_slaves ? row.voyage__voyage_dates__first_dis_of_slaves.split([',']) : '';
    var arrivalDate = '';

    if (arrivalDateArray.length == 3) {
      arrivalDate = arrivalDateArray[2];
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

    if (!row.ranking) {
      row.ranking = '1';
    } else {
      row.ranking++;
    }

    if (row.enslavers_list) {
      var enslaversList = {};
      row.enslavers_list.forEach((value, index) => {
        if (enslaversList[value.enslaver_name] === undefined) {
          enslaversList[value.enslaver_name] = [];
        }

        enslaversList[value.enslaver_name].push(gettext(searchBar.enslaverRoles[value.enslaver_role]));
      });
      row.enslavers_list = enslaversList;
    }

    // source formatting
    row.sources_raw = row.sources_list;
    row.sources_list = getFormattedSourceInTable(
      row.sources_list
    );

    data.push(row);
  });

  if (rankingIndex !== null) {
    if (fuzzySearch) {
      if (!mainDatatable.column(rankingIndex).visible()) {
        mainDatatable.column(rankingIndex).visible(true);
      }
    } else {
      mainDatatable.column(rankingIndex).visible(false);
    }
  }

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

/**
 * round with decimal (keep the decimal even if it is an integer)
 */
function roundDecimal(value, precision) {
  var multiplier = Math.pow(10, precision);
  return (Math.round(value * multiplier) / multiplier).toFixed(precision);
}

// get formated source by parsing through the backend response
function getVoyageFormattedSource(sources) {
  var value = ""; // empty value string
  sources.forEach(function(source) {
    var first = source.split("<>")[0];
    var second = source.split("<>")[1];
    value += "<div><span class='source-title'>" + first + ": </span>";
    value += "<span class='source-content'>" + second + "</span></div>";
  });
  return value;
}

function getFormattedSourceInTable(sources) {
  var value = ""; // empty value string
  try {
    sources.forEach(function(source) {
      value +=
        "<div><span data-toggle='tooltip' data-placement='top' data-html='true' data-original-title='" +
        source.full_ref +
        "'>" +
        source.text_ref +
        "</span></div>";
    });
  }
  catch(err) {
    console.log(`Error in getFormattedSourceInTable: ${err.message}`);
  }
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
  var items = {enslaved_dataset: enslavedDataset};
  for (key1 in filter) {
    if (key1 !== "count") {
      for (key2 in filter[key1]) {
        if (key2 !== "count") {
          for (key3 in filter[key1][key2]) {
            if (key3 !== "count") {
              if (filter[key1][key2][key3].activated) {
                var item = {};
                var searchTerm = [];
                if (filter[key1][key2][key3].value["searchTerm0"] === undefined) {
                  // if it's a multi-tiered place variable
                  if (filter[key1][key2][key3].constructor.name === "PlaceVariable") {
                    var sortedSelections = filter[key1][key2][key3].value["searchTerm"].sort(sortNumber);
                    var searchTerm = [];

                    sortedSelections.forEach(function(selection) {
                      var varName = filter[key1][key2][key3]["varName"];
                      if (selection == filterData.treeselectOptions[varName][0].id) {
                        // select all
                        filterData.treeselectOptions[varName][0].children.forEach(function(broadRegion) {
                          broadRegion.children.forEach(function(region) {
                            region.children.forEach(function(subRegion) {
                              searchTerm.push(subRegion.id);
                            });
                          });
                        });
                      } else {
                        // broadRegion
                        filterData.treeselectOptions[varName][0].children.forEach(function(broadRegion) {
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

                    // if it's a LanguageGroupVariable
                  } else if (filter[key1][key2][key3].constructor.name === "LanguageGroupVariable") {
                    var sortedSelections = filter[key1][key2][key3].value["searchTerm"].sort(sortNumber);
                    var searchTerm = [];

                    sortedSelections.forEach(function(selection) {
                      var varName = filter[key1][key2][key3]["varName"];
                      if (selection == filterData.treeselectOptions[varName][0].id) {
                        // select all
                        searchTerm = filterData.treeselectOptions[varName][0].languageGroupIds;
                      } else {
                        // country
                        filterData.treeselectOptions[varName][0].children.forEach(function(country) {
                          if (selection == country.id) {
                            searchTerm = [...new Set([...searchTerm ,...country.languageGroupIds])];
                          } else {
                            country.children.forEach(function(languageGroup) {
                              if (selection == languageGroup.id) {
                                searchTerm = [...new Set([...searchTerm ,...languageGroup.languageGroupIds])];
                              }
                            });
                          }
                        });
                      }
                    });

                    item["searchTerm"] = searchTerm;
                    
                    // if it's a TreeselectVariable
                  } else if (filter[key1][key2][key3].constructor.name === "TreeselectVariable") {
                    var sortedSelections = filter[key1][key2][key3].value["searchTerm"].sort(sortNumber);
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
                  } else if (filter[key1][key2][key3].constructor.name === "PercentageVariable") {
                    item["searchTerm"] = parseInt(filter[key1][key2][key3].value["searchTerm"]) / 100;
                  } else {
                    item["searchTerm"] = filter[key1][key2][key3].value["searchTerm"];
                  }
                } else {
                  item["searchTerm"] = [
                    filter[key1][key2][key3].value["searchTerm0"],
                    filter[key1][key2][key3].value["searchTerm1"]
                  ];

                  // patch for date variables
                  if (filter[key1][key2][key3].constructor.name === "DateVariable") {
                    // if user chose to search against a particular day, make sure it is searching against a range
                    // i.e. add 23:59:59 to searchTerm0
                    if (filter[key1][key2][key3].value["op"] == "is equal to") {
                      filter[key1][key2][key3].value["searchTerm1"] = filter[key1][key2][key3].value["searchTerm0"].substring(0, 10);
                      filter[key1][key2][key3].value["searchTerm0"] = filter[key1][key2][key3].value["searchTerm1"].replace("/", "-") + "T00:00:00Z";
                      filter[key1][key2][key3].value["searchTerm1"] = filter[key1][key2][key3].value["searchTerm1"] + "T23:59:59Z";
                    }
                    // make the to date always inclusive (add 23:59:59)
                    if (filter[key1][key2][key3].value["searchTerm1"] !== null) {
                      if (filter[key1][key2][key3].value["searchTerm0"].substring(0, 10) != filter[key1][key2][key3].value["searchTerm1"].substring(0, 10)) {
                        // filter[key1][key2][key3].value["searchTerm1"] = moment(filter[key1][key2][key3].value["searchTerm1"], SOLR_DATE_FORMAT).add(1, "days").subtract(1, "seconds");
                        filter[key1][key2][key3].value["searchTerm1"] = filter[key1][key2][key3].value["searchTerm1"].replace("/", "-") + "T23:59:59Z";
                      }
                    }
                    item["searchTerm"] = [
                      filter[key1][key2][key3].value["searchTerm0"],
                      filter[key1][key2][key3].value["searchTerm1"]
                    ];
                  }

                  // patch for percentage variables
                  if (filter[key1][key2][key3].constructor.name === "PercentageVariable") {
                    var searchTerm0 = parseInt(filter[key1][key2][key3].value["searchTerm0"]) / 100;
                    var searchTerm1 = parseInt(filter[key1][key2][key3].value["searchTerm1"]) / 100;
                    item["searchTerm"] = [searchTerm0, searchTerm1];
                  }

                  if (filter[key1][key2][key3].constructor.name === "NumberVariable") {
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
                      case "is between":
                        searchTerm0 = filter[key1][key2][key3].value["searchTerm0"] ?? searchTerm0;
                        searchTerm1 = filter[key1][key2][key3].value["searchTerm1"] ?? searchTerm1;
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
  } else if (currentVariable.constructor.name == "LanguageGroupVariable") {
    treeselectOptions = treeselectOptions[currentVariable.varName][0];
    searchTerms.forEach(function(searchTerm) {
      if (searchTerm == treeselectOptions.id) {
        // ALL SELECTED
        labels.push(treeselectOptions.label);
      } else {
        if (treeselectOptions.children !== undefined) {
          // COUNTRIES
          countries = treeselectOptions.children;
          countries.forEach(function(country) {
            if (searchTerm == country.id) {
              labels.push(country.label);
            } else {
              if (country.children !== undefined) {
                // LANGUAGE GROUPS
                languageGroups = country.children;
                languageGroups.forEach(function(languageGroup) {
                  if (searchTerm == languageGroup.id) {
                    labels.push(languageGroup.label);
                  }
                });
              }
            }
          });
        }
      }
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
          vm.options.errorMessage = error;
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
          vm.options.errorMessage = error;
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
      id: 'br'+data.broadRegions[key].order,
      label: data.broadRegions[key].broad_region,
      children: []
    });
  }

  // build regions
  for (regionId in data.regions) {
    var broadRegion = data.regions[regionId].broad_region;
    for (broadRegionId in options[0].children) {
      if (options[0].children[broadRegionId].id == 'br'+broadRegion.order) {
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
    var broadRegionId = 'br'+data.ports[portId].region.broad_region.order;

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
    options.push({'id': id, 'label' : country.name});
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
      children: [],
      languageGroupIds: [],
    }
  ];

  // fill countries
  var countries = [];
  $.each(response.data, function(id, languageGroup) {
    $.each(languageGroup.countries, (id, country) => {
      countries.push(country);
    });
  });
  countries = [...new Set(countries)].sort()

  $.each(countries, function(key, country) {
    options[0].children.push({
      id: country,
      label: country,
      children: [],
      languageGroupIds: []
    });
  });

  // fill languageGroups
  $.each(response.data, function(id, languageGroup) {
    var label = languageGroup.name;
    var languageGroupId = languageGroup.id;
    if (options[0].languageGroupIds.indexOf(languageGroupId) === -1) {
      options[0].languageGroupIds.push(languageGroupId);
    }
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
      $.each(languageGroup.countries, (index, languageGroupCountry) => {
        if (languageGroupCountry == country.label) {
          if (options[0].children[key].languageGroupIds.indexOf(languageGroupId) === -1) {
            options[0].children[key].languageGroupIds.push(languageGroupId);
          }
          options[0].children[key].children.push({'id': key+'-'+languageGroupId, 'label' : label, 'isDisabled': false, languageGroupIds: [languageGroupId]});
        }
      });
    });
  });
  $.each(options[0].children, function(key, country) {
    country.children.sort(function (a, b) {
      if ( a.label < b.label ){
        return -1;
      }
      if ( a.label > b.label ){
        return 1;
      }
      return 0;
    })
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

function displayColumnOrder(order) {
  if ($('#display-column-order').length > 0) {
    $('#display-column-order').remove();
  }

  if (order.length > 1) {
    var styleElem = document.head.appendChild(document.createElement("style"));
    $(styleElem).attr("id", "display-column-order");

    var innerHTML = '';
    $.each(order, function(index, value){
      innerHTML += '[data-column-index="'+value.column+'"] span.column-header:after {content: " ('+(index+1)+')";}';
    });

    styleElem.innerHTML = innerHTML;
  }
}

function refreshUi(filter, filterData, currentTab, tabData, options) {
  if (currentTab == "results") {
    var currentSearchObj = searchAll(filter, filterData);
    var fuzzySearch = false;
    if (!currentSearchObj.exact_name_search && currentSearchObj.searched_name) {
      fuzzySearch = true;
    }

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
          if (d.order) {
            var rankingIndex = getColumnIndex('ranking');
            if (rankingIndex !== null) {
              var rankingVisible = $('#results_main_table').DataTable().column(rankingIndex).visible();

              if (fuzzySearch && !rankingVisible) {
                  d.order[0]['column'] = rankingIndex;
              }
            }

            currentSearchObj.order_by = $.map(d.order, function(item) {
              var columnIndex = mainDatatable
                ? mainDatatable.colReorder.order()[item.column]
                : item.column;
              return {
                columnName: allColumns[enslavedDataset][columnIndex].data,
                direction: item.dir
              };
            });
          }

          displayColumnOrder(d.order);

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
          return processResponse(json, mainDatatable, fuzzySearch);
        },

        fail: function(xhr, status, error) {
          vm.options.errorMessage = error;
          $("#sv-loader").addClass("display-none");
          $("#sv-loader-error").removeClass("display-none");
        }
      },

      scrollX: true,

      colReorder: true,

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
      ],
      //pagingType: "input",
      bFilter: false,
      processing: true,
      serverSide: true,
      columns: allColumns[enslavedDataset],
      stateSave: true,
      stateDuration: -1,
      initComplete: function() {
        $('[data-toggle="tooltip"]').tooltip();
        initAudioActions();
      },
    });

    mainDatatable.on("column-reorder", function(e, settings, details) {
      var order = $.map(settings.aaSorting, function(item) {
        return {column: item[0]};
      });
      displayColumnOrder(order);
    });

    mainDatatable.on("column-visibility", function(e, settings, column, state, recalc) {
      $('[data-toggle="tooltip"]').tooltip();
      // initAudioActions();
    });

    mainDatatable.on('draw', function(){
      $('[data-toggle="tooltip"]').tooltip();
      initAudioActions();
    });
  }
}

function initAudioActions() {
  $('[data-toggle="popover"]').popover({
        container: 'body',
        placement: 'left',
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

function openVoyageModal(voyageId, dataset) {
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
          "searchTerm": voyageId,
        },
        {
          "op": "equals",
          "varName": "dataset",
          "searchTerm": dataset == undefined || dataset == null ? "-1" : dataset,
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
        searchBar.row.data = response.data.data[0];
        searchBar.rowModalShow = true;
      }
      return;
    })
    .catch(function(error) {
      return error;
    });
}
