// reserved keyword for saved search query identifier
const SAVED_SEARCH_LABEL = "#searchId=";
const ENSLAVED_PATH = "enslaved/";
const SEARCH_URL = "/past/api/search_enslaved";

var voyageColumns = [
  {
    group : 'ship_nation_owner',
    groupName : gettext('Ship, Nation, Owners'),
    fields : [
      { data: "var_voyage_id", label: gettext("Voyage ID"), isImputed: false },
      { data: "var_ship_name", label: gettext("Vessel name"), isImputed: false },
      { data: "var_owner", label: gettext("Vessel owner"), isImputed: false },
      { data: "var_nationality", label: pgettext("past popup label", "NATIONAL"), isImputed: false },
      { data: "var_imputed_nationality", label: pgettext("past popup label", "NATINIMP"), isImputed: true },
      { data: "var_vessel_construction_place_lang", label: gettext("Place constructed"), isImputed: false },
      { data: "var_year_of_construction", label: gettext("Year constructed"), isImputed: false },
      { data: "var_registered_place_lang", label: gettext("Place registered"), isImputed: false },
      { data: "var_registered_year", label: gettext("Year registered"), isImputed: false },
      { data: "var_rig_of_vessel", label: pgettext("past popup label", "RIG"), isImputed: false },
      { data: "var_tonnage", label: gettext("Tonnage"), isImputed: false },
      { data: "var_tonnage_mod", label: gettext("Standardized tonnage"), isImputed: true },
      { data: "var_guns_mounted", label: gettext("Guns mounted"), isImputed: false },
      { data: "var_cargo", label: pgettext("past popup label", "CARGO"), isImputed: false },
    ]
  },
  {
    group : 'outcome',
    groupName : gettext('Outcome'),
    fields : [
      { data: "var_outcome_voyage_lang", label: gettext("Particular outcome of voyage"), isImputed: false },
      { data: "var_outcome_slaves_lang", label: pgettext("past popup label", "FATE2"), isImputed: false },
      { data: "var_outcome_ship_captured_lang", label: gettext("Outcome of voyage if ship captured"), isImputed: false },
      { data: "var_outcome_owner_lang", label: gettext("Outcome of voyage for owner"), isImputed: false },
      { data: "var_resistance_lang", label: pgettext("past popup label", "RESISTANCE"), isImputed: false }
    ]
  },
  {
    group : 'itinerary',
    groupName : gettext('Itinerary'),
    fields : [
      { data: "var_imp_port_voyage_begin_lang", label: pgettext("past popup label", "PTDEPIMP"), isImputed: true },
      { data: "var_imp_principal_place_of_slave_purchase_lang", label: pgettext("past popup label", "MJBYPTIMP"), isImputed: true },
      { data: "var_first_place_slave_purchase_lang", label: pgettext("past popup label", "PLAC1TRA"), isImputed: false },
      { data: "var_second_place_slave_purchase_lang", label: pgettext("past popup label", "PLAC2TRA"), isImputed: false },
      { data: "var_third_place_slave_purchase_lang", label: pgettext("past popup label", "PLAC3TRA"), isImputed: false },
      { data: "var_port_of_call_before_atl_crossing_lang", label: gettext("Places of call before Atlantic crossing"), isImputed: false },
      { data: "var_imp_principal_port_slave_dis_lang", label: pgettext("past popup label", "MJSLPTIMP"), isImputed: true },
      { data: "var_first_landing_place_lang", label: pgettext("past popup label", "SLA1PORT"), isImputed: false },
      { data: "var_second_landing_place_lang", label: pgettext("past popup label", "ADPSALE1"), isImputed: false },
      { data: "var_third_landing_place_lang", label: pgettext("past popup label", "ADPSALE2"), isImputed: false },
      { data: "var_place_voyage_ended_lang", label: pgettext("past popup label", "PORTRET"), isImputed: false }
    ]
  },
  {
    group : 'dates',
    groupName : gettext('Dates'),
    fields : [
      { data: "var_imp_length_home_to_disembark", label: pgettext("past popup label", "VOY1IMP"), isImputed: false },
      { data: "var_length_middle_passage_days", label: pgettext("past popup label", "VOYAGE"), isImputed: false },
      { data: "var_imp_arrival_at_port_of_dis", label: gettext("Year of arrival at port of disembarkation "), isImputed: true },
      { data: "var_voyage_began_partial", label: pgettext("past popup label", "DATEDEPA"), isImputed: false },
      { data: "var_slave_purchase_began_partial", label: pgettext("past popup label", "D1SLATRA"), isImputed: false },
      { data: "var_date_departed_africa_partial", label: pgettext("past popup label", "DLSLATRA"), isImputed: false },
      { data: "var_first_dis_of_slaves_partial", label: pgettext("past popup label", "DATARR32"), isImputed: false },
      { data: "var_departure_last_place_of_landing_partial", label: gettext("Date vessel departed for homeport"), isImputed: false },
      { data: "var_voyage_completed_partial", label: pgettext("past popup label", "DATARR43"), isImputed: false }
    ]
  },
  {
    group : 'captain_and_crew',
    groupName : gettext('Captain and Crew'),
    fields : [
      { data: "var_captain", label: gettext("Captain's name"), isImputed: false },
      { data: "var_crew_voyage_outset", label: gettext("Crew at voyage outset"), isImputed: false },
      { data: "var_crew_first_landing", label: pgettext("past popup label", "CREW3"), isImputed: false },
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
      { data: "var_num_slaves_intended_first_port", label: pgettext("past popup label", "SLINTEND"), isImputed: false },
      { data: "var_num_slaves_carried_first_port", label: pgettext("past popup label", "NCAR13"), isImputed: false },
      { data: "var_num_slaves_carried_second_port", label: pgettext("past popup label", "NCAR15"), isImputed: false },
      { data: "var_num_slaves_carried_third_port", label: pgettext("past popup label", "NCAR17"), isImputed: false },
      { data: "var_total_num_slaves_arr_first_port_embark", label: pgettext("past popup label", "SLAARRIV"), isImputed: false },
      { data: "var_num_slaves_disembark_first_place", label: pgettext("past popup label", "SLAS32"), isImputed: false },
      { data: "var_num_slaves_disembark_second_place", label: pgettext("past popup label", "SLAS36"), isImputed: false },
      { data: "var_num_slaves_disembark_third_place", label: pgettext("past popup label", "SLAS39"), isImputed: false },
      { data: "var_imputed_percentage_men", label: gettext("Percent men"), isImputed: false },
      { data: "var_imputed_percentage_women", label: gettext("Percent women"), isImputed: false },
      { data: "var_imputed_percentage_boys", label: gettext("Percent boys"), isImputed: false },
      { data: "var_imputed_percentage_girls", label: gettext("Percent girls"), isImputed: false },
      { data: "var_imputed_percentage_male", label: gettext("Percent males"), isImputed: false },
      { data: "var_imputed_percentage_child", label: gettext("Percent children"), isImputed: false },
      { data: "var_imputed_sterling_cash", label: gettext("Sterling cash price in Jamaica"), isImputed: false },
      { data: "var_imputed_death_middle_passage", label: pgettext("past popup label", "VYMRTIMP"), isImputed: false },
      { data: "var_imputed_mortality", label: pgettext("past popup label", "VYMRTRAT"), isImputed: false },
      { data: "var_afrinfo", label: pgettext("past popup label", "AFRINFO"), isImputed: false },
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
        enslaversList[value.enslaver_name].push(gettext(value.enslaver_role));
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
                    if (Array.isArray(filter[key1][key2][key3].value["searchTerm"])) {
                      var sortedSelections = filter[key1][key2][key3].value["searchTerm"].sort(sortNumber);
                      var searchTerm = [];

//                       console.log(sortedSelections);
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
    if (Array.isArray(searchTerms)) {
      searchTerms.forEach(function(searchTerm) {
        treeselectOptions.forEach(function(treeselectOption) {
          if (treeselectOption.value == searchTerm) {
            labels.push(treeselectOption.label);
          }
        });
      });
    } else {
      treeselectOptions.forEach(function(treeselectOption) {
        if (treeselectOption.value == searchTerms || treeselectOption.id == searchTerms) {
          labels.push(treeselectOption.label);
        }
      });
    }
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
  var payload = {};

  // load only once remotely and then local copy
  if (!vm.filterData.treeselectOptions[varName]) {
    if (loadType == "place") {
      var apiUrl = '/past/api/enslaved-filtered-places';
      var modelVarName = {
        embarkation_ports: "imp_principal_place_of_slave_purchase_id",
        disembarkation_ports: "imp_principal_port_slave_dis_id",
        // intended_disembarkation_port: "imp_principal_port_slave_dis_id",
        post_disembark_location: "post_disembark_location_id",
      };
      
      if (modelVarName[varName] === undefined) {
        callback("Error: varName " + varName + " is not acceptable");
        return false;
      }

      var params = {var_name: modelVarName[varName], dataset: localStorage.enslavedDataset};

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
        case 'vessel_fate':
          var apiUrl = '/voyage/var-options';
          payload.var_name = 'var_outcome_ship_captured';
          break;
        default:
          callback("Error: varName " + varName + " is not acceptable");
          return false;
      }

      axios
        .post(apiUrl, payload)
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
            case 'vessel_fate':
              var options = parseVesselFate(response);
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

var parseVesselFate = function(response) {
  response.data.data.map(function(data) {
    data["id"] = data["value"];
  });
  return response.data.data;
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
  var unique_countries = new Object;
  var multi_country_language_groups = new Object;
  $.each(response.data, function(id, languageGroup) {
  	var thislanguagegroup={'id':languageGroup.id,'name':languageGroup.name,'count':0}
    $.each(languageGroup.countries, (id, country) => {
      unique_countries[country.modern_country_id]=country.country_name
      thislanguagegroup['count']+=1
    });
    
    if (thislanguagegroup['count']>1) {
    	multi_country_language_groups[languageGroup.id]=thislanguagegroup
    }
    
  });
  
  $.each(unique_countries, function(key, country) {
    options[0].children.push({
      id: key,
      label: country,
      children: [],
      languageGroupIds: []
    });
  });

  //fill multi-country languageGroups
  
  
  
  options[0].children.sort(function (a,b){
  	      if ( a.label < b.label ){
        return -1;
      }
      if ( a.label > b.label ){
        return 1;
      }
      return 0;
    });
  
  if (Object.keys(multi_country_language_groups).length>0) {
  	var multicountry={
      id: 1234567,
      label: 'Multi-Country',
      children: [],
      languageGroupIds: []
    };
    
	  Object.keys(multi_country_language_groups).forEach(k=>{
	  	
	  	var lg=multi_country_language_groups[k]
	  	
		multicountry.children.push({
			'id':lg.id,
			'label':lg.name,
			'isDisabled':false,
			'languageGroupIds':[lg.id]
		});
		multicountry.languageGroupIds.push(lg.id)
	  })
	  options[0].children.splice(0,0,multicountry)
  }
	
  // fill single-country languageGroups
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
        if (languageGroupCountry.country_name == country.label && !multi_country_language_groups[languageGroupId]) {
//           if (options[0].children[key].languageGroupIds.indexOf(languageGroupId) === -1) {
            options[0].children[key].languageGroupIds.push(languageGroupId);
//           }
          options[0].children[key].children.push({'id': languageGroupId, 'label' : label, 'isDisabled': false, languageGroupIds: [languageGroupId]});
        } 
      });
       
    });
  });
  
  //clear out empty entries
  var childrenplaceholder=new Array;
  $.each(options[0].children, function(key, country) {
  	if (options[0].children[key].children.length>0) {
  		childrenplaceholder.push(options[0].children[key])
  	}
  })
  options[0].children=[]
  childrenplaceholder.forEach(c=>{options[0].children.push(c)})
  
  
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
                $('#results_main_table').DataTable().order([ 2, "asc" ]);
                d.order[0]['column'] = rankingIndex;
                d.order[0]['dir'] = "asc";
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
        [gettext("15 rows"), gettext("50 rows"), gettext("100 rows"), gettext("200 rows")]
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
  } else if (currentTab == "maps") {


// I. MAP AND DOM GLOBALS

	//A. Search & DOM
	var currentSearchObj = searchAll(filter, filterData);
	$("#map_container").html('<div id="AO_map" style="width:100%; height:100%; min-height:400px"></div>');

	var AO_map = L.map('AO_map', {
		fullscreenControl: false,
		center:[0,0],
		zoom:3.2,
		minZoom:2,
		maxZoom:18
	}).on('zoomend', function() {
		var currentzoom=AO_map.getZoom()
		if (currentzoom>4){
			regionorplace="place";
			update_oceanic_edges();
			ports_origins_layer_group.addTo(AO_map);
			ports_dest_layer_group.addTo(AO_map);
			ports_embdisemb_layer_group.addTo(AO_map);
			ports_distributed_languages_layer_group.addTo(AO_map)
			regions_origins_layer_group.removeFrom(AO_map);
			regions_dest_layer_group.removeFrom(AO_map);
			regions_embdisemb_layer_group.removeFrom(AO_map);
			regions_distributed_languages_layer_group.removeFrom(AO_map);
		} else {
			regionorplace="region";
			update_oceanic_edges();
			regions_origins_layer_group.addTo(AO_map);
			regions_dest_layer_group.addTo(AO_map);
			regions_embdisemb_layer_group.addTo(AO_map);
			regions_distributed_languages_layer_group.addTo(AO_map);
			ports_origins_layer_group.removeFrom(AO_map);
			ports_dest_layer_group.removeFrom(AO_map);
			ports_embdisemb_layer_group.removeFrom(AO_map);
			ports_distributed_languages_layer_group.removeFrom(AO_map);
		}
		
		var maxanimationzoom=7
		
		if (currentzoom > maxanimationzoom && animation_active) {
			toggle_animation()
// 			animationtoggledbyzoom=true
		}
		
		if (currentzoom <= maxanimationzoom && !animation_active) {
			toggle_animation()
// 			animationtoggledbyzoom=false
		}
		
	}).on('zoomstart', function(a) {
		oceanic_main_edges_layer_group.clearLayers();
		oceanic_animation_edges_layer_group.clearLayers();
		endpoint_main_edges_layer_group.clearLayers();
		endpoint_animation_edges_layer_group.clearLayers();
		activepopups.forEach(p=>p.remove());
		activepopups=new Array;
	});
	
	window.onresize = (event) => {maximizeMapHeight()};
	
	function maximizeMapHeight() {
		var maxMapHeight=window.innerHeight-221; //ffs
		if (maxMapHeight>400){
			$('#AO_map')[0].style['min-height']=maxMapHeight.toString()+'px';
		}
	}
	
	//B. Tile Layers
	
	var mappingSpecialists=L.tileLayer(
		'https://api.mapbox.com/styles/v1/jcm10/clbmdqh2q000114o328k5yjpf/tiles/{z}/{x}/{y}?access_token='+mbaccesstoken,
		{attribution: '<a href="https://www.mappingspecialists.com/" target="blank">Mapping Specialists, Ltd.</a>'});
	var origin_nodelogvaluescale=new Object;
	var embark_disembark_nodelogvaluescale=new Object;
	var hiddenedgesvaluescale=new Object;
	var oceanicedgesvaluescale=new Object;
	
	var oceanic_edges_holding_layer_group= L.layerGroup();
	oceanic_edges_holding_layer_group.addTo(AO_map);
	
	var mappingSpecialistsRivers=L.tileLayer(
	  'https://api.mapbox.com/styles/v1/jcm10/cl98xvv9r001z14mm17w970no/tiles/{z}/{x}/{y}?access_token='+mbaccesstoken)
	var mappingSpecialistsCountries=L.tileLayer(
	  'https://api.mapbox.com/styles/v1/jcm10/cl98yryw3003t14o66r6fx4m9/tiles/{z}/{x}/{y}?access_token='+mbaccesstoken)
	var featurelayers = {
		"Rivers":mappingSpecialistsRivers,
		"Modern Countries":mappingSpecialistsCountries,
		"Voyages":oceanic_edges_holding_layer_group
	}

	
	//C. FEATURE LAYERS
	
	//C1. Cluster groups
	
	//C1a. Origins need to be managed at Port and Region levels (at least for now -- it's making the cluster / individual markers touchy and I'd like to consolidate this into a single layer as I have with final destinations)
	
	var ports_origins_layer_group = make_cluster_layer_groups('origin');
	
	var regions_origins_layer_group = make_cluster_layer_groups('origin');
	
	//C1b. Final destinations -- single layer group
	
	var ports_dest_layer_group = make_cluster_layer_groups('final_destination');
	
	var regions_dest_layer_group = make_cluster_layer_groups('final_destination');


	//D. Non-clustered points groups
	
	var ports_embdisemb_layer_group = L.layerGroup();
	
	var regions_embdisemb_layer_group = L.layerGroup();

	var regions_distributed_languages_layer_group = L.layerGroup();
	
	var ports_distributed_languages_layer_group = L.layerGroup();
	
	var distributedlanguagegroups_hidden_nodes_layer_group = L.layerGroup();
	distributedlanguagegroups_hidden_nodes_layer_group.addTo(AO_map);
	
	var oceanic_waypoints_layer_group = L.layerGroup();
	
	
	var oceanic_main_edges_layer_group= L.layerGroup();
	oceanic_main_edges_layer_group.addTo(oceanic_edges_holding_layer_group);
	
	var oceanic_animation_edges_layer_group= L.layerGroup();
	oceanic_animation_edges_layer_group.addTo(oceanic_edges_holding_layer_group);
	
	var endpoint_main_edges_layer_group = L.layerGroup();
	endpoint_main_edges_layer_group.addTo(AO_map);
		
	var endpoint_animation_edges_layer_group = L.layerGroup();
	endpoint_animation_edges_layer_group.addTo(AO_map);

// II.  STATE GLOBALS

	var animationmode = true;
	var nodesdict = {'region':{},'place':{}};
	var regionorplace = "region";
	var activepopups=new Array;
	var edgesdict = {'region':{},'place':{}};
	var st_e=new Object;

// III. USEFUL FORMATTING FUNCTIONS


// IV. LAYER GROUP FACTORIES

	// A. FACTORIES

	  function makeRouteToolTip(r,networkname) {
 	  	
 	  	var source_id=r.source_target[0]
		if (nodesdict[networkname][source_id]){
			var routesource=nodesdict[networkname][source_id]._layers
			var routesourcename=routesource[Object.keys(routesource)[0]].feature.properties.name
		}
		var target_id=r.source_target[1]
		if (nodesdict[networkname][target_id]){
			var routetarget=nodesdict[networkname][target_id]._layers
			var routetargetname=routetarget[Object.keys(routetarget)[0]].feature.properties.name
		}
		
		
 	  	if (r.leg_type=='origin') { 	  		
 	  		
 	  		var toandorfrom=''
 	  		
 	  		if (!routesourcename|!routetargetname){
				if (!routesourcename) {
					var toandorfrom='taken to '+routetargetname
				}
				if (!routetargetname) {
					var toandorfrom='with '+routesourcename+' origins'
				}
 	  		} else {
 	  			
 	  			var toandorfrom='with '+routesourcename+' origins taken to '+routetargetname
 	  			
 	  		}
 	  		
			var popuptext = [
					r.weight,
					pluralorsingular('Liberated African',r.weight),
					toandorfrom
					].join(" ")
		
		
		} else if (r.leg_type=='final_destination') {
		
			var toandorfrom=''
 	  		
 	  		if (!routesourcename|!routetargetname){
				if (!routesourcename) {
					var toandorfrom='ended up in '+routetargetname
				}
				if (!routetargetname) {
					var toandorfrom='who disembarked in '+routesourcename
				}
 	  		} else {
 	  			
 	  			var toandorfrom='who disembarked in '+routesourcename+' ended up in '+routetargetname
 	  			
 	  		}
 	  		
			var popuptext = [
					r.weight,
					pluralorsingular('Liberated African',r.weight),
					toandorfrom
					].join(" ")
		
 	  	} else if (r.leg_type=='offramp') {
			var popuptext = [
				r.weight,
				pluralorsingular('Liberated African',r.weight),
				"transported to",
				routetargetname
				].join(" ")
 	  	} else if (r.leg_type=='onramp') { 	
			var popuptext = [
				r.weight,
				pluralorsingular('Liberated African',r.weight),
				"taken from",
				routesourcename
				].join(" ")
 	  	} else if (r.leg_type=='oceanic_leg'){
			var popuptext = [r.weight,pluralorsingular('Liberated African',r.weight),"transported."].join(" ");
		}
	  	return popuptext;
	  };
	
	//WE USE THIS TO MAKE OUR MARKER CLUSTER LAYER GROUPS
	function make_cluster_layer_groups(cluster_class) {
		
		var layergroup = L.markerClusterGroup(	
			{
				zoomToBoundsOnClick: false,
				showCoverageOnHover: false,
				spiderfyOnMaxZoom: false,
				iconCreateFunction: function (cluster) {
				var markers = cluster.getAllChildMarkers();
				var n = 1;
				markers.forEach(marker=>{
					n+=marker.feature.properties.size
				});
				
				if (cluster_class=='origin') {
					var html='<div class="origin_cluster_circle"></div>';
					var nodesize=origin_nodelogvaluescale(n)*2
				} else if (cluster_class=='final_destination') {
					var html='<div class="dest_cluster_circle"></div>';
					var nodesize=dest_nodelogvaluescale(n)*2
				}
				
				return L.divIcon({ html: html, iconSize: L.point(nodesize, nodesize), className:"transparentmarkerclusterdiv"});
			}
		}).on('clustermouseover', function (a) {
			activepopups.forEach(p=>p.remove());
			activepopups=new Array;
			var clusterchildmarkers=a.layer.getAllChildMarkers();
			
			if (cluster_class=='origin') {
				var tablenameheader='Language Group'
			} else if (cluster_class=='final_destination') {
				var tablenameheader='Last Known Location'
			}
			
			popuphtml=make_origin_nodes_languagegroupstable(clusterchildmarkers,tablenameheader);
			//http://jsfiddle.net/3tnjL/59/
			var pop = new L.popup({
					'className':'leafletAOPopup',
					'closeOnClick':false,
					'showCoverageOnHover': false,
				}).
				setLatLng(a.latlng).
				setContent(popuphtml);
			pop.addTo(AO_map);
			activepopups.push(pop);
			var child_hidden_edges=new Array;
			Object.keys(clusterchildmarkers).forEach(marker=>{
				if (clusterchildmarkers[marker])	{	
					if (clusterchildmarkers[marker].feature){
						clusterchildmarkers[marker].feature.properties.hidden_edges.forEach(e_id=>{child_hidden_edges.push(e_id)})
					}
				}
			});
			refresh_hidden_edges(child_hidden_edges,regionorplace,AO_map,endpoint_main_edges_layer_group,endpoint_animation_edges_layer_group);							
		})
		return layergroup
	}
	
	// B. ADDTO FUNCTIONS	
	
	
	





	
	// GEOJSON POINTS
	
	
	
	function add_distributednodes(distributednodes,nodesize) {
		distributednodes.forEach(n=> {
			var targetlayer=geojson.getLayer(n.name)
			targetlayer.addTo(distributedlanguagegroups_hidden_nodes_layer_group)
		})
	}
	
	
// 	
// 	var geojsonurl='http://127.0.0.1:8100/static/maps/js/past/africa-hig.geo.json'
// 	console.log(geojsonurl)
// 	
// 	var africaCountriesData = (function() {
// 		var json = null;
// 		$.ajax({
// 			'async': false,
// 			'global': false,
// 			'url': geojsonurl,
// 			'dataType': "json",
// 			'success': function(data) {
// 				json = data;
// 			}
// 		});
// 		return json;
// 	})();

	
	var acnames=new Array;
	
	
// 	console.log(africaCountriesData)
	
	
	
	
    geojson = L.geoJson(africaCountriesData, {
        onEachFeature: function (feature, layer) {
			layer._leaflet_id = feature.properties.name;
			layer.options.weight=0;
			layer.options.fillOpacity=.5;
			layer.options.color="#60c0ab"
			layer.options.weight=1;
			layer.options.opacity=.2;

			
			
// 			layer.options={
// 				"color": "#ffffff",
// 				"weight": 5,
// 				"opacity": 1
// 			};
			layer.addTo(distributedlanguagegroups_hidden_nodes_layer_group);
			
// 			console.log(layer)
		}
		
    })
	distributedlanguagegroups_hidden_nodes_layer_group.clearLayers()
	
	function add_point_to_layergroup(feature,layer_group,nodesize,networkname,edges_main_layer_group,edges_animation_layer_group) {
		var point_id=feature.properties.point_id;
		var node_classes=feature.properties.node_classes;
		var node_title=feature.properties.name;
		var hidden_edges=feature.properties.hidden_edges;
		var newlayer=L.geoJSON(feature, 
			{
				pointToLayer: function (feature, latlng)
					{
						var marker= L.circleMarker(latlng, {
							radius: nodesize,
							fillColor: nodeColorPicker(feature.properties.node_classes),
							color: "#000",
							weight: 1,
							opacity: 1,
							fillOpacity: 0.6
						})		
						
						marker.on('mouseover', function (a) {
							activepopups.forEach(p=>p.remove());
							activepopups=new Array;
							
							if (Object.keys(distributedlanguagegroups[networkname]).includes(point_id.toString())) {
								
								var popuptext=[
									feature.properties.size,
									pluralorsingular('Liberated African',feature.properties.size),
									"with",
									feature.properties.name,
									"origins.*<br/><i>*Note: this marker stands in for a language<br/>with wide geographic distribution, now visible.</i>"
								].join(" ")
								
								marker.bindTooltip(popuptext,{'sticky':false}).openTooltip();
								
								var hidethis={"region":regions_origins_layer_group,"place":ports_origins_layer_group}[regionorplace]	
								hidethis.remove()
								
								Object.keys(distributedlanguagegroups[networkname]).forEach(
									languagegroupid=>{
										
										if (languagegroupid!=point_id.toString() && nodesdict[networkname][languagegroupid]){
											nodesdict[networkname][languagegroupid].remove()
										}
									}
								)
								
								add_distributednodes(distributedlanguagegroups[networkname][point_id.toString()],nodesize)
								
								
								
							} else {
								var pop = new L.popup({
									'className':'leafletAOPopup',
									'closeOnClick':false,
									'showCoverageOnHover': false,
								}).
								setLatLng(a.latlng).
								setContent(makeNodePopUp(feature,nodesdict[networkname],edgesdict[networkname]));
								pop.addTo(AO_map);
								activepopups.push(pop);
								marker.openPopup();
								
							}
							
							
							refresh_hidden_edges(hidden_edges,regionorplace,AO_map,edges_main_layer_group,edges_animation_layer_group);							
							marker.bringToFront();
						});
						
						if (Object.keys(distributedlanguagegroups[networkname]).includes(point_id.toString())) {
							
							marker.on('mouseout', function (a) {
								distributedlanguagegroups_hidden_nodes_layer_group.clearLayers()
								var hidethis={"region":regions_origins_layer_group,"place":ports_origins_layer_group}[regionorplace]	
								hidethis.addTo(AO_map)
								Object.keys(distributedlanguagegroups[networkname]).forEach(
									languagegroupid=>{
										if (languagegroupid!=point_id.toString() && nodesdict[networkname][languagegroupid]){
											nodesdict[networkname][languagegroupid].addTo(layer_group)
										}
									}
								)
							})
						}
						
						
						return marker
				}
			},
		);
		layer_group.addLayer(newlayer);
		return newlayer
	};	


	function straightlinebezier(a,b){
		var midx=(a['lat']+b['lat'])/2
		var midy=(a['lng']+b['lng'])/2
		var control=[midx,midy]
		var straightline=[[[a['lat'],a['lng']],[b['lat'],b['lng']]],[control,control]]
		return straightline
	}

	function refresh_hidden_edges(edge_id_list,networkname,map,main_layer_group,animation_layer_group){
		main_layer_group.clearLayers();
		animation_layer_group.clearLayers();
		//first, radically clean up the edge list
		var live_edge_list = new Array();
		edge_id_list.forEach(e=>{
			if (edgesdict[networkname][e]) {live_edge_list.push(edgesdict[networkname][e])}	
		})
		//console.log(live_edge_list)
		var tmp_edge_dict=new Object();
		//now roll them up into a dictionary
		
		
		
		live_edge_list.forEach(edge=>{
// 			console.log(edge.main._coords)
			var ctrl=edge.main._coords[3]
			var st=edge.source_target
			if (edge.leg_type=='origin'){
				var source_id=st[0]
				var target_id=st[1]
				var source=nodesdict[networkname][source_id]
				var target=nodesdict[networkname][target_id]
				var target_leaflet_id=target._leaflet_id
				var target_latlng=target._layers[Object.keys(target._layers)[0]].feature.geometry.coordinates
				var target_coords={'lat':target_latlng[1],'lng':target_latlng[0]}
				if (regionorplace=='region') {
					var lg=regions_origins_layer_group
				} else {
					var lg=ports_origins_layer_group
				}
				var vp=lg.getVisibleParent(source._layers[Object.keys(source._layers)[0]])
				if (vp) {
					var source_coords=vp._latlng
					var source_leaflet_id=vp._leaflet_id
				} else {
					var source_latlng=source._layers[Object.keys(source._layers)[0]].feature.geometry.coordinates
					var source_coords={'lat':source_latlng[1],'lng':source_latlng[0]}
					var source_leaflet_id=source._leaflet_id
				}
			} else if (edge.leg_type=='final_destination') {
				var source_id=st[0]
				var target_id=st[1]
				var source=nodesdict[networkname][source_id]
				var target=nodesdict[networkname][target_id]
				var source_leaflet_id=source._leaflet_id
				var source_latlng=source._layers[Object.keys(source._layers)[0]].feature.geometry.coordinates
				var source_coords={'lat':source_latlng[1],'lng':source_latlng[0]}
				if (regionorplace=='region') {
					var lg=regions_dest_layer_group
				} else {
					var lg=ports_dest_layer_group
				}
				var vp=lg.getVisibleParent(target._layers[Object.keys(target._layers)[0]])
				if (vp) {
					var target_coords=vp._latlng
					var target_leaflet_id=vp._leaflet_id
				} else {
					var target_latlng=target._layers[Object.keys(target._layers)[0]].feature.geometry.coordinates
					var target_coords={'lat':target_latlng[1],'lng':target_latlng[0]}
					var target_leaflet_id=target._leaflet_id
				}
			};
			//console.log(edge.leg_type)
// 			console.log("ST-->",source_coords,target_coords)
// 			console.log("CTRL-->",ctrl)
			
// 			var geometry=[[[source_coords['lat'],source_coords['lng']],[target_coords['lat'],target_coords['lng']]],[ctrl,ctrl]]
// 			console.log(geometry)
			
				if (tmp_edge_dict[source_leaflet_id]) {
					if (tmp_edge_dict[source_leaflet_id][target_leaflet_id]) {
						tmp_edge_dict[source_leaflet_id][target_leaflet_id].weight+=edge.weight
						tmp_edge_dict[source_leaflet_id][target_leaflet_id].ctrls.push(ctrl)
						existing_st=tmp_edge_dict[source_leaflet_id][target_leaflet_id]['source_target']
						
						if (source_id!=existing_st[0]) {
							tmp_edge_dict[source_leaflet_id][target_leaflet_id]['source_target']=[null,existing_st[1]]
						}
						
						if (target_id!=existing_st[1]) {
							tmp_edge_dict[source_leaflet_id][target_leaflet_id]['source_target']=[existing_st[0],null]
						}
						
					} else {
						tmp_edge_dict[source_leaflet_id][target_leaflet_id]={'weight':edge.weight,'source_latlng':source_coords,'target_latlng':target_coords,'ctrls':[ctrl],'leg_type':edge.leg_type,'source_target':st}
					}
				} else {
					tmp_edge_dict[source_leaflet_id]={}
					tmp_edge_dict[source_leaflet_id][target_leaflet_id]={'weight':edge.weight,'source_latlng':source_coords,'target_latlng':target_coords,'ctrls':[ctrl],'leg_type':edge.leg_type,'source_target':st}
				}
		})
		
		Object.keys(tmp_edge_dict).forEach(s=>{
			Object.keys(tmp_edge_dict[s]).forEach(t=>{
				var edge=tmp_edge_dict[s][t]
				
				var ctrl_lngs=0;
				var ctrl_lats=0;
// 				console.log(edge)
				edge.ctrls.forEach(ctrl=>{
// 					console.log(ctrl)
					ctrl_lngs+=ctrl[1];
					ctrl_lats+=ctrl[0];
				})
				
				var ctrl=[ctrl_lats/edge.ctrls.length,ctrl_lngs/edge.ctrls.length]
				
				var geometry=[[[edge.source_latlng['lat'],edge.source_latlng['lng']],[edge.target_latlng['lat'],edge.target_latlng['lng']]],[ctrl,ctrl]]
				
				var updatededge=edge
				updatededge['geometry']=geometry
				make_edge(map,updatededge,networkname,main_layer_group,animation_layer_group,recordtodict=false,hiddenedgesvaluescale)
			})
		})	
	}
	
	//only used by refresh_oceanic_edges, but it's easy to see this might be needed elsewhere.
	function bringpointlayerstofront() {
		[	
			ports_embdisemb_layer_group,
			regions_embdisemb_layer_group
		].forEach(lg=>{
			lg.eachLayer(function(layer){layer.bringToFront()})
		})
	}

	//the behavior of these different edge classes (clustered vs non-clustered) makes it reasonable to handle them differently
	function refresh_oceanic_edges(edge_id_list,networkname,map,main_layer_group,animation_layer_group){
		main_layer_group.clearLayers();
		animation_layer_group.clearLayers();
		edge_id_list.forEach(e=>{
		if (edgesdict[networkname][e]) {
				edge=edgesdict[networkname][e]
				st=edge.source_target;
				source_id=st[0];
				target_id=st[1];
// 				var lg= new Object;
// 				if (regionorplace=='region') {
// 					var lg=regions_origins_layer_group
// 				} else {
// 					var lg=ports_origins_layer_group
// 				}
				var source=nodesdict[networkname][source_id]
				var target=nodesdict[networkname][target_id]
				if (source&&target){
					edge.main.redraw()
					edge.main.addTo(main_layer_group)
					var updatedanimation=make_animationrouteoptions(edge.main,AO_map)
					edge.animation.options.animate.duration=updatedanimation.animate.duration
					edge.animation.options.dashArray=updatedanimation.dashArray
					edge.animation.redraw()
					edge.animation.addTo(animation_layer_group)
				}
			}
		})
		bringpointlayerstofront()
	}
	
	function make_animationrouteoptions(basepath,map){
		var off=20
		var on=1
		return {
			color: "#6c757dc9",
			weight: "1",
			dashArray:on.toString() + " " + (off-on).toString(),
			animate: {
				"duration":1000,
				"iterations":Infinity,
				"direction":'normal'
			}
		}
	}

	function get_featurecollection_edges_by_types(all_network_edges,tags) {
	
		filtered_edges=new Object;
		Object.keys(all_network_edges).forEach(e_id=>{
			var edge=all_network_edges[e_id];
			if(tags.includes(edge.leg_type)){
				filtered_edges[e_id]=edge;
			}
		})
		return filtered_edges;
	}
	
	function get_edgedict_edges_by_types(all_network_edges,tags) {
		filtered_edges=new Object;
		Object.keys(all_network_edges).forEach(e_id=>{
			var edge=all_network_edges[e_id];
			if(tags.includes(edge.leg_type)){
				filtered_edges[e_id]=edge;
			}
		})
		return filtered_edges;
	}
	
	function update_oceanic_edges() {
		endpoint_main_edges_layer_group.clearLayers();
		endpoint_animation_edges_layer_group.clearLayers();
		oceanic_main_edges_layer_group.clearLayers();
		oceanic_animation_edges_layer_group.clearLayers();
		
		var all_network_edges=edgesdict[regionorplace];
		var oceanic_edges=get_edgedict_edges_by_types(all_network_edges,['onramp','offramp','oceanic_leg']);
		
		refresh_oceanic_edges(Object.keys(oceanic_edges),regionorplace,AO_map,oceanic_main_edges_layer_group,oceanic_animation_edges_layer_group)
		
		oceanic_edges=get_edgedict_edges_by_types(all_network_edges,['onramp','offramp','oceanic_leg']);
		
		Object.keys(oceanic_edges).forEach(e_id=>{
			var edge=oceanic_edges[e_id];
			edge.main.addTo(oceanic_main_edges_layer_group);
			edge.animation.addTo(oceanic_animation_edges_layer_group);
		})
		
	}

	function make_edge(map,edge,networkname,main_layer_group,animation_layer_group,recordtodict=true,edgeweightvaluescale){
// 		console.log(edge)
		var commands = [];
		var edge_type=edge.leg_type;
		var weight=edgeweightvaluescale(edge.weight);
		var color=legColorPicker(edge_type);
		commands.push("M", edge.geometry[0][0]);
		commands.push("C", edge.geometry[1][0], edge.geometry[1][1], edge.geometry[0][1]);
		
		var newroute=L.curve(commands, {
			color: color,
			weight: weight,
			stroke: true,
		})
		.bindTooltip(makeRouteToolTip(edge,networkname),{'sticky':true})
		.on('mouseover', function () {
			activepopups.forEach(p=>p.remove());
			activepopups=new Array;
		})
		
		newroute.addTo(main_layer_group);
	
		//then layer on the animation curves
		//in oder to do which (using basic css) we need to know how long these curves are
		//because the css animation works on the basis of animation duration (how long it should take to complete a run)
		//and if what we're animating is the traversal of a small dot along a bezier curve
		//then we have to make the time apportioned inversely proportional to the length of the curve
		//tldr: in order that the dots on longer routes and shorter routes move the same speed, the longer routes need animations of longer duration, and vice versa
		//increase timingscalar to slow this down, decrease it to speed it up
		var animationrouteoptions=make_animationrouteoptions(newroute,map)
		var newanimationroute=L.curve(commands, animationrouteoptions);
		newanimationroute.addTo(animation_layer_group);
		
		if (recordtodict) {
			edgesdict[networkname][edge.id]={
				'main':newroute,
				'animation':newanimationroute,
				'source_target':edge.source_target,
				'leg_type':edge.leg_type,
				'weight':edge.weight
			};
		}
		
	};

	var region_vs_place_vars = {
		'place':{
			'origins_layer_group':ports_origins_layer_group,
			'distributed_languages_layer_group':ports_distributed_languages_layer_group,
			'embark_disembark_layers_group':ports_embdisemb_layer_group,
			'dest_layer_group':ports_dest_layer_group,
		},
		'region':{
			'origins_layer_group':regions_origins_layer_group,
			'distributed_languages_layer_group':regions_distributed_languages_layer_group,
			'embark_disembark_layers_group':regions_embdisemb_layer_group,
			'dest_layer_group':regions_dest_layer_group,
			
		}
	};

	function initial_map_builder(resp) {
		//we only need to make the origins layer group once, despite it existing in both place & region zoom levels
		var test_region_hidden_edges=new Array
		Object.keys(region_vs_place_vars).forEach(networkname=>{
			var network=resp[networkname];
			var origins_layer_group = region_vs_place_vars[networkname]['origins_layer_group'];
			var embark_disembark_layer_group = region_vs_place_vars[networkname]['embark_disembark_layers_group'];
			var dest_layer_group = region_vs_place_vars[networkname]['dest_layer_group'];
			var featurecollection=network.points;
			var distributed_languages_layer_group = region_vs_place_vars[networkname]['distributed_languages_layer_group'];
			origin_nodelogvaluescale=nodelogvaluescale_fn(featurecollection,4,28);
			embark_disembark_nodelogvaluescale=nodelogvaluescale_fn(featurecollection,3,10);
			dest_nodelogvaluescale=nodelogvaluescale_fn(featurecollection,4,15);
			featurecollection.features.forEach(function (feature) {
			
				var point_id=feature.properties.point_id
				var node_classes=Object.keys(feature.properties.node_classes);
				if (node_classes.includes('origin')) {
					if (Object.keys(distributedlanguagegroups[networkname]).includes(point_id.toString())) {
						var thislayergroup=distributed_languages_layer_group
					} else {
						var thislayergroup=origins_layer_group
					} 
					
					var nodesize=origin_nodelogvaluescale(feature.properties.size);
					var newlayer = add_point_to_layergroup(feature,thislayergroup,nodesize,networkname,endpoint_main_edges_layer_group,endpoint_animation_edges_layer_group);
					
					nodesdict[networkname][point_id]=newlayer
						
				} else if (node_classes.includes('embarkation') || node_classes.includes('disembarkation')) {
					if (networkname=='region') {
						var nodesize=embark_disembark_nodelogvaluescale(feature.properties.size);
					} else {
						var nodesize=5
					}
					var newlayer = add_point_to_layergroup(feature,embark_disembark_layer_group,nodesize,networkname,endpoint_main_edges_layer_group,endpoint_animation_edges_layer_group)
					nodesdict[networkname][point_id]=newlayer
				} else if (node_classes.includes('post-disembarkation')) {
					var nodesize=dest_nodelogvaluescale(feature.properties.size);
					var newlayer = add_point_to_layergroup(feature,dest_layer_group,nodesize,networkname,endpoint_main_edges_layer_group,endpoint_animation_edges_layer_group);
					nodesdict[networkname][point_id]=newlayer
				} else {
					oceanic_waypoints_layer_group.addTo(AO_map)
					var newlayer=add_point_to_layergroup(feature,oceanic_waypoints_layer_group,1,networkname,oceanic_main_edges_layer_group,oceanic_animation_edges_layer_group);
					nodesdict[networkname][point_id]=newlayer
					oceanic_waypoints_layer_group.remove()
				}
			})
			
			var edges=network.routes;
			hiddenedgesvaluescale=routeslogvaluescale_fn(edges,1,11);
			oceanicedgesvaluescale=routeslogvaluescale_fn(edges,1,3);
			var hiddenedges=get_featurecollection_edges_by_types(edges,['origin','final_destination']);
			var oceanicedges=get_featurecollection_edges_by_types(edges,['onramp','offramp','oceanic_leg']);
			Object.keys(hiddenedges).forEach(e_id=>{make_edge(AO_map,hiddenedges[e_id],networkname,endpoint_main_edges_layer_group,endpoint_animation_edges_layer_group,recordtodict=true,hiddenedgesvaluescale)});
			Object.keys(oceanicedges).forEach(e_id=>{make_edge(AO_map,oceanicedges[e_id],networkname,oceanic_main_edges_layer_group,oceanic_animation_edges_layer_group,recordtodict=true,oceanicedgesvaluescale)});
			update_oceanic_edges();
		});
		

	}
	maximizeMapHeight();
	AO_map.invalidateSize();
	var animationtoggledbyzoom=false;
	
	function toggle_animation() {
	
		if (animation_active) {
			animation_active=false
			endpoint_animation_edges_layer_group.remove()
			oceanic_animation_edges_layer_group.remove()
		} else {
			animation_active=true
			endpoint_animation_edges_layer_group.addTo(AO_map)
			oceanic_animation_edges_layer_group.addTo(AO_map)
			update_oceanic_edges()
		}
		
		animationtoggle_div.remove();
		animationtoggle_div.addTo(AO_map);
		$('#animationtogglebutton').click(function(e) {toggle_animation()});
	}
	
	
	var animation_active=true;
	var animationtoggle_div = L.control({ position: "topleft" });
	animationtoggle_div.onAdd = function(map) {
			if (animation_active) {
				var isactivetext="Running"
				var divclass="animationtoggle_active"
			} else {
				var isactivetext="Stopped"
				var divclass="animationtoggle_inactive"
			}
			var div = L.DomUtil.create("div", divclass);
// 			div.innerHTML += '<a href="javascript:void(0)" id="animationtogglebutton">Animation '+isactivetext+'</a>';
			div.innerHTML += 'Animation '+isactivetext;
			return div
		};
	
	
	//------------>MAKE THE CALL FOR THE DATA
	$.ajax({
		type: "POST",
		url: SEARCH_URL,
		data: JSON.stringify({
				search_query: currentSearchObj,
				output: "maps"
			}),
		success: function(d){
			maximizeMapHeight();
			AO_map.invalidateSize();
			add_control_layers_to_map(featurelayers,AO_map);
			regions_origins_layer_group.addTo(AO_map);
			ports_embdisemb_layer_group.addTo(AO_map);
			regions_embdisemb_layer_group.addTo(AO_map);
			ports_dest_layer_group.addTo(AO_map);
			ports_origins_layer_group.addTo(AO_map);
			ports_distributed_languages_layer_group.addTo(AO_map);
			regions_distributed_languages_layer_group.addTo(AO_map);
// 			mappingSpecialistsCountries.addTo(AO_map);
			mappingSpecialists.addTo(AO_map);
			
			var total_results_count=d.region.total_results_count;			
			drawUpdateCount(AO_map,total_results_count);
			drawLegend(AO_map);
			animationtoggle_div.addTo(AO_map);
// 			$('#animationtogglebutton').click(function(e) {toggle_animation()});
			initial_map_builder(d);
			AO_map.invalidateSize();
			maximizeMapHeight();
			AO_map.invalidateSize();
			var default_minmax_group = new L.featureGroup([
				L.marker([12,-20]),
				L.marker([-8,20])
			]);
			AO_map.fitBounds(default_minmax_group.getBounds());
			AO_map.invalidateSize();
			maximizeMapHeight();
			AO_map.invalidateSize();
			document.getElementById("past-maps-loader").hidden=true;
			AO_map.invalidateSize();
			maximizeMapHeight();
			AO_map.invalidateSize();
		}
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
