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
  } else if (currentTab == "maps") {


// MAP AND DOM GLOBALS

//A. Search & DOM
	var currentSearchObj = searchAll(filter, filterData);
	$("#map_container").html('<div id="AO_map" style="width:100%; height:100%; min-height:400px"></div>');

//B. Base Tile Layers
	var mappingSpecialists=L.tileLayer(
	  'https://api.mapbox.com/styles/v1/jcm10/cl5v6xvhf001b14o4tdjxm8vh/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiamNtMTAiLCJhIjoiY2wyOTcyNjJsMGY5dTNwbjdscnljcGd0byJ9.kZvEfo7ywl2yLbztc_SSjw',
	  {attribution: '<a href="https://www.mappingspecialists.com/" target="blank">Mapping Specialists, Ltd.</a>'});

	var basemap = {"Mapping Specialists":mappingSpecialists}
	
	var AO_map = L.map('AO_map', {
		fullscreenControl: false,
		center:[0,0],
		zoom:3.2,
		minZoom:3.2,
		layers:	[mappingSpecialists],
	});	
	
	maximizeMapHeight();
	AO_map.invalidateSize();
	var default_minmax_group = new L.featureGroup([
			L.marker([15,-23]),
			L.marker([-10,24])
		]);
	AO_map.fitBounds(default_minmax_group.getBounds());
	maximizeMapHeight()
	
	var nodelogvaluescale=new Object;
	
	var mappingSpecialistsRivers=L.tileLayer(
	  'https://api.mapbox.com/styles/v1/jcm10/cl98xvv9r001z14mm17w970no/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiamNtMTAiLCJhIjoiY2wyOTcyNjJsMGY5dTNwbjdscnljcGd0byJ9.kZvEfo7ywl2yLbztc_SSjw').addTo(AO_map);
	var mappingSpecialistsCountries=L.tileLayer(
	  'https://api.mapbox.com/styles/v1/jcm10/cl98yryw3003t14o66r6fx4m9/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiamNtMTAiLCJhIjoiY2wyOTcyNjJsMGY5dTNwbjdscnljcGd0byJ9.kZvEfo7ywl2yLbztc_SSjw').addTo(AO_map);
	var featurelayers = {
		"Rivers":mappingSpecialistsRivers,
		"Modern Countries":mappingSpecialistsCountries,
// 		"Animation": mainanimationrouteslayergroup,
	}

//C. Layer Controls
	var layerControl = L.control.layers(null,featurelayers).addTo(AO_map);
	L.control.scale({ position: "bottomright" }).addTo(AO_map);
	AO_map.invalidateSize();
	maximizeMapHeight();
	window.onresize = (event) => {maximizeMapHeight()};




	function personorpeople(count){
		if (count===1) {
			var result="person"
		} else {
			var result="people"
		}
		return result
	};

	// MORE OR LESS STABLE MAP ELEMENTS
	// UPPER-LEFT LEGEND/LINK SHOWING THE TOTAL NUMBER OF PEOPLE IN THE SEARCH RESULT
	// borrowed from https://codepen.io/haakseth/pen/KQbjdO
	function drawUpdateCount(map,results_count) {
		var results_count_div = L.control({ position: "topleft" });
		results_count_div.onAdd = function(map) {
			var div = L.DomUtil.create("div", "legend");
			div.innerHTML += '<p class="legendp"><a href="#results">'+results_count.toString()+' '+personorpeople(results_count)+'.<br/>← Read their names</a></p>';
			return div
		};
		results_count_div.addTo(map);
	};
	// LOWER LEFT LEGEND SHOWING THE COLOR CODES FOR THE NODES
	function drawLegend(map) {
		var legend_div = L.control({ position: "bottomleft" });
		legend_div.onAdd = function(map) {
			var div = L.DomUtil.create("div", "legend");
			div.innerHTML= '<table class=legendtable>\
				<tr>\
					<td><div class="circle" style="background-color:rgb(167,224,169);"></div><td>\
					<td>' + gettext('Origins') + '\
					<span id="origins_map_key_pill" data-toggle="tooltip" class="badge badge-pill badge-secondary tooltip-pointer" title="Peoples\' origins are imputed based on their recorded names."> IMP </span>\
					</td>\
				</tr>\
				<tr>\
					<td><div class="circle" style="background-color:rgb(255,0,0);"></div><td>\
					<td>'+gettext('Embarkations')+'</td>\
				</tr>\
				<tr>\
					<td><div class="circle" style="background-color:rgb(163,0,255);"></div><td>\
					<td>Embark & Disembark</td>\
				</tr>\
				<tr>\
					<td><div class="circle" style="background-color:rgb(0,0,255);"></div><td>\
					<td>' + gettext('Disembarkations') + '</td>\
				</tr>\
				<tr>\
					<td><div class="circle" style="background-color:rgb(246,193,60);"></div><td>\
					<td>'+gettext('Post-Disembark Locations')+'</td>\
				</tr>\
				</table>\
				'
			return div
		};
		legend_div.addTo(map);
		$(function () {
			$('[data-toggle="tooltip"]').tooltip()
		})
	};






//D. Primary Layer Groups

	
	function formatNodePopUpListItem(k,v) {
		var nodeclass_labels={
			'embarkation':'embarked',
			'disembarkation':'disembarked',
			'post-disembarkation':'ended up',
			'origin':'originated'
		};
		
		var label = nodeclass_labels[k];
		var count = v.count;
		var key = v.key;
		var formattedstring=[count.toString(),personorpeople(count),label].join(' ')
		if (k!='origin') {
			var text='<a href="#" onclick="linkfilter(' + key.toString() + ',\'' + k + '\'); return false;">' + formattedstring + '</a>'
		} else {
			var text = false
		};
		return text;
	};
	
	
		//Node color rules:
	//Priority given to embarkations & disembarkations, and their combination
	//So my only color "scale" is red<-->blue
	//Only nodes that have no embark or disembark get colored as yellow (final destination) or green (origin)
	function nodeColorPicker(nodeclasses) {
		if ('embarkation' in nodeclasses || 'disembarkation' in nodeclasses) {
			if ('embarkation' in nodeclasses && 'disembarkation' in nodeclasses) {
				var embark=nodeclasses.embarkation.count;
				var disembark=nodeclasses.disembarkation.count;
				var embarkratio=embark/(embark+disembark)
				var disembarkratio=disembark/(embark+disembark)
				var thiscolor=d3.rgb(embarkratio*255,0,disembarkratio*255);
				return thiscolor
			} else {
				if ('embarkation' in nodeclasses) {
					var thiscolor=d3.rgb(255,0,0);
				} else if ('disembarkation' in nodeclasses) {
					var thiscolor=d3.rgb(0,0,255);
				}
			}
		} else if ('post-disembarkation' in nodeclasses) {
			var thiscolor=d3.rgb(246,193,60);
		} else if ('origin' in nodeclasses) {
			var thiscolor=d3.rgb(96,192,171);
		};
		return thiscolor
	}
	
	
	function makeNodePopUp(node_classes,node_title) {
		var popupsubheads=[];
		//a node can have multiple classes (mostly this is for sierra leone)
		Object.entries(node_classes).forEach(([k,v]) => popupsubheads.push(formatNodePopUpListItem (k,v)));
		if (!popupsubheads.includes(false)){
			var popupcontent=popupsubheads.join(' and ') + " in " + node_title;
		} else {
			var count=node_classes['origin']['count'];
			var popupcontent=[count,personorpeople(count),"with",node_title,"origins."].join(" ")
		}
		return(popupcontent);
	};
	
	function add_point_to_layergroup(feature,layer_group,nodesize,networkname) {
		var point_id=feature.properties.point_id;
		var node_classes=feature.properties.node_classes;
		var node_title=feature.properties.name;
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
						marker.bindPopup(makeNodePopUp(node_classes,node_title),{'className':'leafletAOPopup'});
						marker.on('mouseover', function () {
							displayhiddenroutes(AO_map,[feature]);
							marker.openPopup();
							marker.bringToFront();
						});
						marker.on('mouseout',function () {
							marker.closePopup();
							hiddenrouteslayergroup.clearLayers();
							hiddenanimationrouteslayergroup.clearLayers();
						})
						return marker
				}
			},
		);
		var l_id=L.stamp(newlayer);
		var point_id=feature.properties.point_id
		nodesdict[point_id]['leaflet_id']=l_id;
		layer_group.addLayer(newlayer);
	};	



			




	
	
		
	function make_languagegroupstable(markers) {
		
		var tablehtml="<table class='lgmaptable'><tr><td>Language Group</td><td>Number of people</td></tr>";
		
		//markerclusters contain lots of different kinds of "markers" -- to get at our geojson ones, we have to filter
		//there's likely a smarter way to do this
		
		var tablerowdata=new Array;
		Object.keys(markers).forEach(marker=>{
			if (markers[marker])	{	
				if (markers[marker].feature){
					tablerowdata.push({"lg":markers[marker].feature.properties.name,"value":markers[marker].feature.properties.size})
				}
			}
		})
		tablerowdata.sort((a,b)=>a.value-b.value);
		tablerowdata.reverse()
		
		displaylimit=5;
		
		tablerowdata.slice(0,displaylimit).forEach(r=>{tablehtml+="<tr><td>"+r.lg+"</td><td>"+r.value.toString()+"</td></tr>"});
		if (displaylimit<tablerowdata.length) {
			var excluded_lg_count=tablerowdata.length-displaylimit;
			var excluded_people_count=0
			tablerowdata.slice(displaylimit,tablerowdata.length-1).forEach(r=>{excluded_people_count+=r.value})
			tablehtml += "<tr><td>"+excluded_lg_count.toString()+" more language groups</td><td>"+excluded_people_count.toString()+"</td></tr>"	
		}
		
		tablehtml+="</table>"
		
		return tablehtml
		
	}

	
	





	function legColorPicker(leg_type,alpha=1) {
		if (leg_type == 'final_destination') {
			var thiscolor=d3.color("rgba(246,193,60,"+alpha+")");
		} else if (leg_type == 'origin') {
			var thiscolor=d3.color("rgba(96,192,171,"+alpha+")");
		} else {
			var thiscolor=d3.color("rgba(215,153,250,"+alpha+")");		
		};
		return thiscolor;
	};
		
	//Node color rules:
	//Priority given to embarkations & disembarkations, and their combination
	//So my only color "scale" is red<-->blue
	//Only nodes that have no embark or disembark get colored as yellow (final destination) or green (origin)
	function nodeColorPicker(nodeclasses) {
		if ('embarkation' in nodeclasses || 'disembarkation' in nodeclasses) {
			if ('embarkation' in nodeclasses && 'disembarkation' in nodeclasses) {
				var embark=nodeclasses.embarkation.count;
				var disembark=nodeclasses.disembarkation.count;
				var embarkratio=embark/(embark+disembark)
				var disembarkratio=disembark/(embark+disembark)
				var thiscolor=d3.rgb(embarkratio*255,0,disembarkratio*255);
				return thiscolor
			} else {
				if ('embarkation' in nodeclasses) {
					var thiscolor=d3.rgb(255,0,0);
				} else if ('disembarkation' in nodeclasses) {
					var thiscolor=d3.rgb(0,0,255);
				}
			}
		} else if ('post-disembarkation' in nodeclasses) {
			var thiscolor=d3.rgb(246,193,60);
		} else if ('origin' in nodeclasses) {
			var thiscolor=d3.rgb(96,192,171);
		};
		return thiscolor
	}
	
	//Routes get tooltips. And here is where we make them!
	  function makeRouteToolTip(r) {
 	  	if (r.leg_type=='final_destination') {
			var routesource=nodesdict[r.source_target[0]]
			var routetarget=nodesdict[r.source_target[1]]
 	  		try {
				var popuptext = [
					r.weight,
					personorpeople(r.weight),
					"ended up in",
					routetarget.name,
					"after landing in",
					routesource.name
					].join(" ")
 	  		} catch(error) {
				console.log("BAD SOURCE OR TARGET NODE-->",r);
				var st=r.source_target;
				var popuptext=["bad source or target node. source: ",st[0],". target: ",st[1]].join('')
			}
 	  	} else if (r.leg_type=='origin') {
			var routesource=nodesdict[r.source_target[0]]
			var routetarget=nodesdict[r.source_target[1]]
 	  		try {
				var popuptext = [
					r.weight,
					routesource.name,
					personorpeople(r.weight),
					"taken to",
					routetarget.name
					].join(" ")
 	  		} catch(error) {
				console.log("BAD SOURCE OR TARGET NODE-->",r);
				var st=r.source_target;
				var popuptext=["bad source or target node. source: ",st[0],". target: ",st[1]].join('')
			}
 	  	} else if (r.leg_type=='offramp') {
			var routetarget=nodesdict[r.source_target[1]]
			try {
				var popuptext = [
					r.weight,
					personorpeople(r.weight),
					"transported to",
					routetarget.name
					].join(" ")
			} catch (error) {
				console.log("BAD TARGET NODE-->",r);
				var st=r.source_target;
				var popuptext=["bad target node: ",st[1]].join('')
			}
 	  	} else if (r.leg_type=='onramp') { 	
			var routesource=nodesdict[r.source_target[0]]
 	  		try {
				var popuptext = [
					r.weight,
					personorpeople(r.weight),
					"taken from",
					routesource.name
					].join(" ")
 	  		} catch(error) {
				console.log("BAD SOURCE NODE-->",r);
				var st=r.source_target;
				var popuptext=["bad source node: ",st[0]].join('')
 	  		}
 	  	} else {
			var popuptext = [r.weight,personorpeople(r.weight),"transported."].join(" ");
		}
	  	return popuptext;
	  };
	
	//This function creates a bezier curve
	//& is used for all curve creation, including animations and interactivity bindings.
	//note that w 
	function addRoute(map,route,mainlayergroup,point_id=null,animationlayergroup=null){
		//parse the geometry, classes, features, and draw a route curve 
		var commands = [];
		commands.push("M", route.geometry[0][0]);
		commands.push("C", route.geometry[1][0], route.geometry[1][1], route.geometry[0][1]);
// 		var weight=valueScale(route.weight);
		var distance=0;
		
		var timingscalar = 50
		

				
		var newroute=L.curve(commands, {
			color: "#fff0",
			weight: 1,
			stroke: true,
		})
		.bindTooltip(makeRouteToolTip(route),{'sticky':true})
		.addTo(mainlayergroup);
		
		
		//then layer on the animation curves
		//in oder to do which (using basic css) we need to know how long these curves are
		//because the css animation works on the basis of animation duration (how long it should take to complete a run)
		//and if what we're animating is the traversal of a small dot along a bezier curve
		//then we have to make the time apportioned inversely proportional to the length of the curve
		//tldr: in order that the dots on longer routes and shorter routes move the same speed, the longer routes need animations of longer duration, and vice versa
		//increase timingscalar to slow this down, decrease it to speed it up
		var distance=0
		
		
		var interpolation_steps=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
		var pairs=d3.pairs(newroute.trace(interpolation_steps));
		function euclideandistance(p1,p2) {
			xyone=AO_map.latLngToContainerPoint(p1);
			xytwo=AO_map.latLngToContainerPoint(p2);
			var ed=Math.sqrt((xyone.x-xytwo.x)**2+(xyone.y-xytwo.y)**2)
			return ed
		}
		if (pairs.length>1){
			pairs.forEach(sp=>distance+=(euclideandistance(sp[0],sp[1])))
		}
		
// 		newroute.removeFrom(mainlayergroup);
		
		var duration=distance*timingscalar;
		
		if (animationlayergroup && animationmode){
			
			var standard_interval=10
			
			var newanimationroute=L.curve(commands, {
				color: "#6c757dc9",
				weight: "1",
				dashArray:"1 " + (standard_interval-1).toString(),
				animate: {
					"duration":duration,
					"iterations":Infinity,
					"direction":'normal'
				}
			});
		newanimationroute.addTo(animationlayergroup);
		// the distance traversed has to be measured in *PIXELS* or else the speed increases with zoom level
			
	// 		console.log(distance)


	// 			newanimationroute.animate.duration=distance*timingscalar;
			
	// 			var distance=newanimationroute._path.getTotalLength();
			
		};
		
		//this is some interactivity micro-tuning/crafting
		//when you roll over a node with hidden routes (i.e., inland to origination point or final destination)
		//you want the node you're rolling over to be on top of the routes that are drawn emanating from it -- otherwise, those routes' interactivities make it very likely you'll get rid of your node popup immediately by having these appear directly under your mouse and on top of the node
		//however, we want *only* that node to come to the front, because you do want to be able to roll your mouse off that node and immediately onto one of the emanating routes, potentially to follow it out to the other, connected nodes -- which, when you hit them, you want to be able to roll off the route onto the node to bring that node to the front and draw the routes emanating from *it* etc. etc.
		if (['origin','final_destination'].includes(route.leg_type)) {
			var hovernode_leaflet_id=nodesdict[point_id].leaflet_id;
			var hovernode_layer = map._layers[hovernode_leaflet_id];
			if (hovernode_layer) {hovernode_layer.bringToFront()};
// 			newroute.on('mouseover', function () {	
// 				if (currently_open_popup_layer.closePopup) {
// 					currently_open_popup_layer.closePopup();
// 				}
// 			});
		//and this bad boy makes sure that those node popups go away once you hit one of the other non-hidden routes
		} else if (['onramp','offramp','oceanic_leg'].includes(route.leg_type)) {
			newroute.on('mouseover', function () {	
				hiddenrouteslayergroup.clearLayers();
				hiddenanimationrouteslayergroup.clearLayers();
				if (nodesarehidden) {
					refreshhiddennodes();
					nodesarehidden=false;
				}
// 				if (currently_open_popup_layer.closePopup) {
// 					currently_open_popup_layer.closePopup();
// 				}
			});
		};
	  };
	  
	//Main routes are drawn when the map is refreshed. These are the embarkation-->disembarkation routes
	//Which include connections from the embarkation point into the oceanic network, and from that back out to the disembarkation port
	//We are for now calling those final-mile connections "onramps" and "offramps"
	function drawMainRoutes(map, routes) {
		var mapRouteValueMin = d3.min(routes, function (r) {
			return r.weight;
		});
		var mapRouteValueMax = d3.max(routes, function (r) {
			return r.weight;
		});
	  valueScale.domain([mapRouteValueMin, mapRouteValueMax]).range([3, 13]);
	  
	  routes.map((route) => {
// 	  	if (route.visible){
// // 			newroute=addRoute(map,route,mainrouteslayergroup,null,mainanimationrouteslayergroup);
// 		} else {
// // 			console.log(route);
			hiddenroutes[route.id]=route;
// 		}
	})
	};












	function displayhiddenroutes(map,nodes) {
		hiddenrouteslayergroup.clearLayers();
		hiddenanimationrouteslayergroup.clearLayers();

// 		
		nodes.forEach(node=>{
	// 		console.log(node.properties)
			var hidden_edge_ids=node.properties.hidden_edges;
		
			var attached_node_ids = new Array;
			hidden_edge_ids.forEach(edge_id => {
				var route=hiddenroutes[edge_id];
				if (route) {
					addRoute(map,route,hiddenrouteslayergroup,node.properties.point_id,hiddenanimationrouteslayergroup);
					route.source_target.forEach(p_id=> {if (!attached_node_ids.includes(p_id)) {attached_node_ids.push(p_id)}})
				}
			})
		})
// 		remove_unattached_nodes_and_restore_attached_hidden_nodes_pfffffffff(attached_node_ids,node);
		
	};







































	
	
	
	
	
	
	
	
	function make_clustermarker(markers,size){
		size_scaled=nodelogvaluescale(size)-2
		var html = '<div class="cluster_circle"></div>';
		return html
	}

	var origins_layer_group = L.markerClusterGroup(	
		{
			maxClusterRadius: 120,
			zoomToBoundsOnClick: false,
			iconCreateFunction: function (cluster) {
			var markers = cluster.getAllChildMarkers();
			var n = 0;
			markers.forEach(marker=>n+=marker.feature.properties.size);
			var html = make_clustermarker(markers,n);
			return L.divIcon({ html: html, iconSize: L.point(nodelogvaluescale(n)*2, nodelogvaluescale(n)*2), className:"transparentmarkerclusterdiv"});
		}
	}).on('clustermouseover', function (a) {
		var clusterchildmarkers=a.layer.getAllChildMarkers();
		popuphtml=make_languagegroupstable(clusterchildmarkers);
		//http://jsfiddle.net/3tnjL/59/
		var pop = new L.popup({
				'className':'leafletAOPopup',
				'closeOnClick':false,
				showCoverageOnHover: false,
			}).
			setLatLng(a.latlng).
			setContent(popuphtml);
		pop.addTo(AO_map);
		activepopups.push(pop);

		var child_nodes=new Array;
		Object.keys(clusterchildmarkers).forEach(marker=>{
			if (clusterchildmarkers[marker])	{	
				if (clusterchildmarkers[marker].feature){
					child_nodes.push(clusterchildmarkers[marker].feature)
				}
			}
		});
		
		
		displayhiddenroutes(AO_map,child_nodes)


	})
	.on('clustermouseout', function (a) {
		activepopups.forEach(p=>p.remove());
		activepopups=new Array;
		hiddenrouteslayergroup.clearLayers();
		hiddenanimationrouteslayergroup.clearLayers();
	});
	
	AO_map.on('zoomstart', function(a) {
		activepopups.forEach(p=>p.remove());
		activepopups=new Array;
		hiddenrouteslayergroup.clearLayers();
		hiddenanimationrouteslayergroup.clearLayers();
	});
	
	var ports_layer_group = L.layerGroup();
	ports_layer_group.addTo(AO_map);
	
	origins_layer_group.addTo(AO_map);
	
	var activepopups=new Array;
	
	var hiddenrouteslayergroup = L.layerGroup();
	hiddenrouteslayergroup.addTo(AO_map);

	var hiddenroutes = new Object();
	var valueScale = d3.scaleLog();

	var hiddenanimationrouteslayergroup = L.layerGroup();
	hiddenanimationrouteslayergroup.addTo(AO_map);


	function makeRoutesDict(network) {
		var features=network.points.features;
		features.forEach(feature => nodesdict[feature.properties.point_id]=feature.properties);
	}
	
	
		var animationmode = true;
	//B3. The nodesdict object allows us to look up nodes by id
	var nodesdict = new Object;











	function initial_map_builder(resp) {
		['place'].forEach(networkname=>{
			var network=resp[networkname];
			var featurecollection=network.points;
			makeRoutesDict(network);
			drawMainRoutes(AO_map,network.routes);
			nodelogvaluescale_fn(featurecollection);
			featurecollection.features.forEach(function (feature) {
				var node_classes=feature.properties.node_classes;			
				if (Object.keys(node_classes)[0]=='origin') {
					var nodesize=nodelogvaluescale(feature.properties.size);
					add_point_to_layergroup(feature,origins_layer_group,nodesize,networkname);
				} else if ('embarkation' in node_classes || 'disembarkation' in node_classes) {
				
					var nodesize=5;
					add_point_to_layergroup(feature,ports_layer_group,nodesize,networkname)
				
				}
				
			})
		});		
	}
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	//------------>MAKE THE CALL FOR THE DATA
	$.ajax({
		type: "POST",
		url: SEARCH_URL,
		data: JSON.stringify({
				search_query: currentSearchObj,
				output: "maps"
			}),
		success: function(d){
			AO_map.invalidateSize();
			var total_results_count=d.region.total_results_count;
			drawUpdateCount(AO_map,total_results_count);
			drawLegend(AO_map);
			initial_map_builder(d);
			AO_map.invalidateSize();
			if (total_results_count>80000) {
				var default_minmax_group = new L.featureGroup([
					L.marker([15,-23]),
					L.marker([-10,24])
				]);
				AO_map.fitBounds(default_minmax_group.getBounds());
			}
		}
	});
	
	

	
	
//E. Styling globals
//E1. scale the nodes sizes logarithmically 
		function nodelogvaluescale_fn(points) {

		var valueMin = d3.min(points.features, function (p) {
			return p.properties.size;
		  });
		  var valueMax = d3.max(points.features, function (p) {
			return p.properties.size;
		  });
		nodelogvaluescale = d3.scaleLog().domain([valueMin, valueMax]).range([4, 25]);
	}

	function maximizeMapHeight() {
		var maxMapHeight=window.innerHeight-221; //ffs
		$('#AO_map')[0].style['min-height']=maxMapHeight.toString()+'px';
	}


	
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
