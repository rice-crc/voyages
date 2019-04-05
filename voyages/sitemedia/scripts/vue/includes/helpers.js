// reserved keyword for saved search query identifier
const SAVED_SEARCH_LABEL = "#searchId=";
const TRANS_PATH = "voyages/";

/**
 * Add space between camelCase text.
 */
function unCamelCase(str) {
  str = str.replace(/([a-z\xE0-\xFF])([A-Z\xC0\xDF])/g, '$1 $2');
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
* round without decimal (if it's an integer stay at the integer level)
*/
function round(value, precision) {
  var multiplier = Math.pow(10, precision || 0);
  return Math.round(value * multiplier) / multiplier;
}
/**
* round with decimal (keep the decimal even if it is an integer)
*/
function roundDecimal(value, precision) {
  var multiplier = Math.pow(10, precision);
  return (Math.round(value * multiplier) / multiplier).toFixed(precision);
}

// converts camel case into title case
function camel2title(camelCase) {
  // no side-effects
  return camelCase
    // inject space before the upper case letters
    .replace(/([A-Z])/g, function(match) {
      return " " + match;
    })
    // replace first char with upper case
    .replace(/^./, function(match) {
      return match.toUpperCase();
    });
}

// format a number to become 1,000 (with commas)
const numberWithCommas = (x) => {
  return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

const isPercentageAxis = (axes) => {
  if (Array.isArray(axes)) {
    return axes.length > 0 && axes.reduce((agg, axis) => agg && isPercentageAxis(axis), true);
  }
  let axis = axes;
  return axis.includes('percentage') || 
    axis.includes('mortality') ||
    axis.includes('resistance_idnum') ||
    axis == 'var_resistance_freq' ||
    axis == 'var_imputed_mortality_avg';
}

// a function that generates a random key for saved queries
var generateRandomKey = function() {
  var ALPHABET = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
  var ID_LENGTH = 8;
  var rtn = '';
  for (var i = 0; i < ID_LENGTH; i++) {
    rtn += ALPHABET.charAt(Math.floor(Math.random() * ALPHABET.length));
  }
  return rtn;
}

// a function that generates a unique key for saved queries
// it depends on function generateRandomKey
var generateUniqueRandomKey = function(previous) {
  var UNIQUE_RETRIES = 9999;
  previous = previous || [];
  var retries = 0;
  var id;
  // Try to generate a unique ID,
  // i.e. one that isn't in the previous.
  while (!id && retries < UNIQUE_RETRIES) {
    id = generateRandomKey();
    if (previous.indexOf(id) !== -1) {
      id = null;
      retries++;
    }
  }
  return id;
};

// get formated source by parsing through the backend response
function getFormattedSource(sources) {
    var value = ""; // empty value string
    sources.forEach(function (source) {
      var first = source.split("<>")[0];
      var second = source.split("<>")[1];
      value += "<div><span class='source-title'>" + first + ": </span>";
      value += "<span class='source-content'>" + second + "</span></div>";
    })
  return value;
}

// get formated source by parsing through the backend response
// returns the format for table display
// ABCD - [Tooltip: details]
function getFormattedSourceInTable(sources) {
    var value = ""; // empty value string
    sources.forEach(function (source) {
      var first = source.split("<>")[0];
      var second = source.split("<>")[1];
      value += "<div><span data-toggle='tooltip' data-placement='top' data-html='true' data-original-title='" + second + "'>" + first + "</span>";
    })
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

// IMP tooltip
var impTooltipString = '<span class="badge badge-pill badge-secondary tooltip-pointer" data-toggle="tooltip" data-placement="top" data-original-title="' + gettext("Imputed results are calculated by an algorithm.") + '"> ' + gettext("IMP") + ' </span>';

// variableMapping
// used for loading a variable (variables extracted from a saved query ==> variables in the vm filter object)
var variableMapping = {
  imp_arrival_at_port_of_dis: "var_imp_arrival_at_port_of_dis",
  voyage_id: "var_voyage_id",
  ship_name: "var_ship_name",
  owner: "var_owner",
  nationality_idnum: "var_nationality",
  imputed_nationality_idnum: "var_imputed_nationality",
  vessel_construction_place_idnum: "var_vessel_construction_place_idnum",
  year_of_construction: "var_year_of_construction",
  registered_place_idnum: "var_registered_place_idnum",
  registered_year: "var_registered_year",
  rig_of_vessel_idnum: "var_rig_of_vessel",
  tonnage: "var_tonnage",
  tonnage_mod: "var_tonnage_mod",
  guns_mounted: "var_guns_mounted",

  imp_port_voyage_begin_idnum: "var_imp_port_voyage_begin_id",
  imp_principal_place_of_slave_purchase_idnum: "var_imp_principal_place_of_slave_purchase_id",
  first_place_slave_purchase_idnum: "var_first_place_slave_purchase_id",
  second_place_slave_purchase_idnum: "var_second_place_slave_purchase_id",
  third_place_slave_purchase_idnum: "var_third_place_slave_purchase_id",
  port_of_call_before_atl_crossing_idnum: "var_port_of_call_before_atl_crossing_id",
  imp_principal_port_slave_dis_idnum: "var_imp_principal_port_slave_dis_id",
  first_landing_place_idnum: "var_first_landing_place_id",
  second_landing_place_idnum: "var_second_landing_place_id",
  third_landing_place_idnum: "var_third_landing_place_id",
  place_voyage_ended_idnum: "var_place_voyage_ended_id",

  imp_total_num_slaves_purchased: "var_imp_total_num_slaves_purchased",
  total_num_slaves_purchased: "var_total_num_slaves_purchased",
  imp_total_slaves_disembarked: "var_imp_total_slaves_disembarked",
  num_slaves_intended_first_port: "var_num_slaves_intended_first_port",
  num_slaves_carried_first_port: "var_num_slaves_carried_first_port",
  num_slaves_carried_second_port: "var_num_slaves_carried_second_port",
  num_slaves_carried_third_port: "var_num_slaves_carried_third_port",
  total_num_slaves_arr_first_port_embark: "var_total_num_slaves_arr_first_port_embark",
  num_slaves_disembark_first_place: "var_num_slaves_disembark_first_place",
  num_slaves_disembark_second_place: "var_num_slaves_disembark_second_place",
  num_slaves_disembark_third_place: "var_num_slaves_disembark_third_place",
  imputed_percentage_men: "var_imputed_percentage_men",
  imputed_percentage_women: "var_imputed_percentage_women",
  imputed_percentage_boys: "var_imputed_percentage_boys",
  imputed_percentage_girls: "var_imputed_percentage_girls",
  imputed_percentage_male: "var_imputed_percentage_male",
  imputed_percentage_child: "var_imputed_percentage_child",
  imputed_sterling_cash: "var_imputed_sterling_cash",
  imputed_death_middle_passage: "var_imputed_death_middle_passage",
  imputed_mortality: "var_imputed_mortality",

  imp_length_home_to_disembark: "var_imp_length_home_to_disembark",
  length_middle_passage_days: "var_length_middle_passage_days",
  voyage_began: "var_voyage_began",
  slave_purchase_began: "var_slave_purchase_began",
  date_departed_africa: "var_date_departed_africa",
  first_dis_of_slaves: "var_first_dis_of_slaves",
  departure_last_place_of_landing: "var_departure_last_place_of_landing",
  voyage_completed: "var_voyage_completed",

  outcome_voyage_idnum: "var_outcome_voyage",
  outcome_slaves_idnum: "var_outcome_slaves",
  outcome_ship_captured_idnum: "var_outcome_ship_captured",
  outcome_owner_idnum: "var_outcome_owner",
  resistance_idnum: "var_resistance",
  captain: "var_captain",
  crew_voyage_outset: "var_crew_voyage_outset",
  crew_first_landing: "var_crew_first_landing",
  crew_died_complete_voyage: "var_crew_died_complete_voyage",
  sources_plaintext: "var_sources_plaintext"
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
      if (filter[group][subGroup][key].value["searchTerm0"] === undefined) { // has only one search term
        filter[group][subGroup][key].value["searchTerm"] = filter[group][subGroup][key].default["searchTerm"];
      } else { // has two search terms
        filter[group][subGroup][key].value["searchTerm0"] = filter[group][subGroup][key].default["searchTerm0"];
        filter[group][subGroup][key].value["searchTerm1"] = filter[group][subGroup][key].default["searchTerm1"];
      }
      filter[group][subGroup][key].value["op"] = filter[group][subGroup][key].default["op"];
      filter[group][subGroup][key].changed = false;
      filter[group][subGroup][key].activated = false;
    }
  }
}

// serialize a filter
function serializeFilter(filter){
  return JSON.stringify(filter);
}

function replaceKey(key) {
  if (key == "is less than") {
    return "is at most"
  } else if (key == "is more than") {
    return "is at least";
  } else if (key == "is equal to") {
    return "equals";
  } else {
    return key;
  }
}

function searchAll(filter, filterData) {
  var items = [];
  for (key1 in filter) {
    if (key1 !== "count") {
      for (key2 in filter[key1]) {
        if (key2 !== "count") {
          for (key3 in filter[key1][key2]) {
            if (key3 !== "count") {
              if (filter[key1][key2][key3].activated) {
                var item = {};
                var searchTerm = [];
                item["op"] = replaceKey(filter[key1][key2][key3].value["op"]);
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
                            })
                          })
                        });
                      } else {
                        // broadRegion
                        filterData.treeselectOptions[varName][0].children.forEach(function(broadRegion) {
                          if (selection == broadRegion.id) {
                            broadRegion.children.forEach(function(region) {
                              region.children.forEach(function(subRegion) {
                                searchTerm.push(subRegion.id);
                              });
                            })
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
                  } else if (filter[key1][key2][key3].constructor.name === "TreeselectVariable") {
                    var sortedSelections = filter[key1][key2][key3].value["searchTerm"].sort(sortNumber);
                    var searchTerm = [];
                    

                    if (sortedSelections.includes("0")) {
                      // select all
                      filterData.treeselectOptions[varName][0].children.forEach(function(options) {
                        searchTerm.push(options.id);
                      });
                    } else {
                      searchTerm = filter[key1][key2][key3].value["searchTerm"];
                    }

                    item["searchTerm"] = searchTerm;
                  } else if (filter[key1][key2][key3].constructor.name === "PercentageVariable"){
                    item["searchTerm"] = parseInt(filter[key1][key2][key3].value["searchTerm"])/100;
                  } else {
                    item["searchTerm"] = filter[key1][key2][key3].value["searchTerm"];
                  }
                } else {
                  item["searchTerm"] = [filter[key1][key2][key3].value["searchTerm0"], filter[key1][key2][key3].value["searchTerm1"]];

                  // patch for date variables
                  if (filter[key1][key2][key3].constructor.name === "DateVariable") {
                    // if user chose to search against a particular day, make sure it is searching against a range
                    // i.e. add 23:59:59 to searchTerm0
                    if (filter[key1][key2][key3].value["op"] == "is equal to") {
                      filter[key1][key2][key3].value["op"] = "is between";
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
                    item["searchTerm"] = [filter[key1][key2][key3].value["searchTerm0"], filter[key1][key2][key3].value["searchTerm1"]];
                    item["op"] = filter[key1][key2][key3].value["op"];
                  }

                  // patch for percentage variables
                  if (filter[key1][key2][key3].constructor.name === "PercentageVariable") {
                    var searchTerm0 = parseInt(filter[key1][key2][key3].value["searchTerm0"])/100;
                    var searchTerm1 = parseInt(filter[key1][key2][key3].value["searchTerm1"])/100;
                    item["searchTerm"] = [searchTerm0, searchTerm1];
                  }
                }

                // TODO: fix a bug with the backend: it should use _idnum and not _id except for voyage_id
                if (filter[key1][key2][key3].varName.slice(-3) == "_id" && filter[key1][key2][key3].varName !== "voyage_id") {
                  item["varName"] = filter[key1][key2][key3].varName + "num";
                } else {
                  item["varName"] = filter[key1][key2][key3].varName;
                }

                // TODO: backend patch
                if (filter[key1][key2][key3].varName == "nationality" ||
                  filter[key1][key2][key3].varName == "imputed_nationality" ||
                  filter[key1][key2][key3].varName == "rig_of_vessel" ||
                  filter[key1][key2][key3].varName == "outcome_voyage" ||
                  filter[key1][key2][key3].varName == "outcome_slaves" ||
                  filter[key1][key2][key3].varName == "outcome_ship_captured" ||
                  filter[key1][key2][key3].varName == "outcome_owner" ||
                  filter[key1][key2][key3].varName == "resistance"
                ) {
                  item["varName"] = filter[key1][key2][key3].varName + "_idnum";
                }

                items.push(item);
              }
            }
          }
        }
      }
    }
  }

  // placeholder
  hasYear = false;
  items.map(function(item) {
    if (item.varName == "imp_arrival_at_port_of_dis") {
      if (item.op == "between") {
        item.op = "is between"; // patch a backend bug
      }
      hasYear = true;
    }
  })

  if (!hasYear) {
    var item = {};
    item["op"] = "is between";
    item["searchTerm"] = [1514, 1866];
    item["varName"] = "imp_arrival_at_port_of_dis";
    items.push(item);
  }

  if (SV_MODE == "intra") {
    const intraFlagObject = { "op": "equals", "searchTerm": ["true"], "varName": "intra_american_voyage" };
    items.push(intraFlagObject);
  }
  // alert(JSON.stringify(items));
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
      item.ports = []
      regions[item.pk] = item;
    } else if (item.type == "broad_region") {
      item.label = item.broad_region;
      item.ports = []
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
    treeselectOptions = treeselectOptions["var_" + currentVariable.varName];
    searchTerms.forEach(function (searchTerm) {
      treeselectOptions.forEach(function(treeselectOption){
        if (treeselectOption.value == searchTerm) {
          labels.push(treeselectOption.label);
        }
      });
    });
  } else if (currentVariable.constructor.name == "PlaceVariable") {
    treeselectOptions = treeselectOptions[currentVariable.varName][0];
    searchTerms.forEach(function (searchTerm) {
      if (searchTerm == treeselectOptions.id) { // ALL SELECTED
        labels.push(treeselectOptions.label);
      } else {
        if (treeselectOptions.children !== undefined) { // BROARD REGION
          broadRegions = treeselectOptions.children;
          broadRegions.forEach(function (broadRegion) {
            if (searchTerm == broadRegion.id) {
              labels.push(broadRegion.label);
            } else {
              if (broadRegion.children !== undefined) { // REGION
                regions = broadRegion.children;
                regions.forEach(function (region) {
                  if (searchTerm == region.id) {
                    labels.push(region.label);
                  } else { // SUB REGION
                    if (region.children !== undefined) { // SUB REGION
                      subRegions = region.children;
                      subRegions.forEach(function (subRegion) {
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

    // load special weird variables
    if (["registered_place_idnum", "vessel_construction_place_idnum"].indexOf(varName) >= 0) {
      axios.post('/voyage/filtered-places', {})
      .then(function (response) {
        var options = parsePlaces(response);
        vm.filterData.treeselectOptions[varName] = options;
        vTreeselect.treeselectOptions = vm.filterData.treeselectOptions[varName];
        callback(); // notify vue-treeselect about data population completion
        return;
      })
      .catch(function (error) {
        options.errorMessage = error;
        $("#sv-loader").addClass("display-none");
        $("#sv-loader-error").removeClass("display-none");
        return error;
      });
    }

    // load PlaceVariable
    else if (loadType == "place"){
      axios.post('/voyage/filtered-places', {
        var_name: varName,
      })
      .then(function (response) {
        var options = parsePlaces(response);
        vm.filterData.treeselectOptions[varName] = options;
        vTreeselect.treeselectOptions = vm.filterData.treeselectOptions[varName];
        callback(); // notify vue-treeselect about data population completion
        return;
      })
      .catch(function (error) {
        options.errorMessage = error;
        $("#sv-loader").addClass("display-none");
        $("#sv-loader-error").removeClass("display-none");
        return error;
      });
    }
    
    // load TreeselectVariable
    else if (loadType == "treeselect"){
      varName = "var_" + varName;
      axios.post('/voyage/var-options', {
        var_name: varName,
      })
      .then(function (response) {
        response.data.data.map(function(data) {
          data["id"] = data["value"];
        });
        vm.filterData.treeselectOptions[varName] = response.data.data;
        vTreeselect.treeselectOptions = vm.filterData.treeselectOptions[varName];
        callback(); // notify vue-treeselect about data population completion
        return;
      })
      .catch(function (error) {
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
  var options = [{
    id: 0,
    label: gettext("Select All"),
    children: null
  }];

  // fill select all
  options = [{
    id: 0,
    code: 0,
    label: gettext("Select All"),
    children: [],
  }];

  // fill broad regions
  for (key in data.broadRegions) {
    options[0].children.push({
      id: data.broadRegions[key].order,
      label: data.broadRegions[key].broad_region,
      children: [],
    })
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
        })
      }
    }
  }

  // fill ports
  data.ports = Object.keys(data.ports).sort(function (a, b) { return data.ports[a].order - data.ports[b].order }).map(key => data.ports[key]);   // sort data.ports by "order" attribute

  for (portId in data.ports) {
    // get basic information about a port
    var code = data.ports[portId].code;
    var label = data.ports[portId].port;
    var regionId = data.ports[portId].region.code;
    var broadRegionId = data.ports[portId].region.broad_region.order;

    // locate corresponding location in the options tree
    options[0].children.map(function(broadRegion) {
      if (broadRegion.id == broadRegionId) {
        broadRegion.children.map(function(region) {
          if (region.id == regionId) { // in the correct region
            region.children.push({ // fill port
              id: code,
              label: label
            })
          }
        })
      }
    });

  }
  return options;
}

function sortNumber(a, b) {
  return a - b;
}

function initZeroArray(length) {
  var arr = [];
  while (length--) {
    arr.push(0);
  }
  return arr;
}

function destroyPreviousTable(id) {
  try {
    if ($.fn.DataTable.isDataTable(id)) {
      $(id).DataTable().destroy();
    }
  } catch (e) {
    console.log(e);
  }
}

function refreshUi(filter, filterData, currentTab, tabData, options) {
  // Update UI after search query was changed,
  // or a tab was selected.
  $('.animationElement, #map').hide();
  var currentSearchObj = {
    items: searchAll(filter, filterData),
    orderBy: []
  };

  var searchUrl = "api/beta_ajax_search";
  if (currentTab == 'results') {
    // Results DataTable
    var pageLength = {
      extend: 'pageLength',
      className: 'btn btn-info buttons-collection dropdown-toggle',
    };

    

    var mainDatatable = $('#results_main_table').DataTable({
      ajax: {
        url: searchUrl,
        type: 'POST',
        data: function(d) {
          if (d.order) {
            currentSearchObj.orderBy = $.map(d.order, function(item) {
              var columnIndex = mainDatatable ?
                mainDatatable.colReorder.order()[item.column] :
                item.column;
              return {
                name: allColumns[columnIndex].data.substring(4),
                direction: item.dir
              };
            });
          }

          // TEMP Yang: I don't think this is the right place for this code...
          // Besides, I think that this is attaching multiple handlers for
          // the click, which is inefficient.
          $('#results_main_table tbody').on('click', 'tr', function() {
            searchBar.row.data = mainDatatable.row(this).data();
          });

          return JSON.stringify({
            searchData: currentSearchObj,
            tableParams: d,
            output: 'resultsTable',
          });
        },

        // preprocess the returned data
        // a - to use % instead of decimals (e.g. 30% vs. 0.30)
        // b - to format source into HTML decorated string
        dataSrc: function (json) {
          var keys = null;
          var percentageKeys = [];
          for (var i = 0, ien = json.data.length; i < ien; i++) {
            // percentage vs. decimal
            if (percentageKeys.length <= 0) {
              keys = Object.keys(json.data[i]);
              keys.forEach(function(key){
                if (isPercentageAxis([key])) percentageKeys.push(key);
              });
            }
            percentageKeys.forEach(function(percentageKey){
              if (json.data[i][percentageKey]) {
                json.data[i][percentageKey] = roundDecimal(json.data[i][percentageKey] * 100, 1) + "%";
              }
            });

            // source formatting
            json.data[i]["var_sources_raw"] = json.data[i]["var_sources"];
            json.data[i]["var_sources"] = getFormattedSourceInTable(json.data[i]["var_sources"]);

          }
          return json.data;
        },
        
        fail: function (xhr, status, error) {
          options.errorMessage = error;
          $("#sv-loader").addClass("display-none");
          $("#sv-loader-error").removeClass("display-none");
        },
      
      },
      
      scrollX: true,
      colReorder: {
        order: [
          1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
          11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 
          21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 0,
          31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 
          41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
          51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 
          61, 62
        ]
      },

      columnDefs: [{
          width: "1%",
          targets: 0
        },
        {
          width: "5%",
          targets: 1
        },
        {
          width: "15%",
          targets: 62
        },
        {
          width: "5%",
          targets: 32
        },
        {
          width: "10%",
          targets: 50
        },
        {
          width: "5%",
          targets: 33
        },
        {
          width: "5%",
          targets: 34
        },
        {
          width: "5%",
          targets: 25
        },
      ],

      order: [[ 1, "asc" ]],
      destroy: true,

      // page length Default
      pageLength: 15,

      // dom: 'ifrtBp',
      dom: "<'flex-container'iB>" +
        "<'row'<'col-sm-12'tr>>" +
        "<'row'<'col-sm-5'><'col-sm-7'p>>",
      lengthMenu: [
        [15, 50, 100, 200],
        ['15 rows', '50 rows', '100 rows', '200 rows']
      ],

      language: dtLanguage,

      buttons: [
        columnToggleMenu,
        pageLength,
        {
          extend: 'collection',
          text: '<span class="fa fa-columns" style="vertical-align: middle;"></span>',
          className: 'btn btn-info buttons-collection dropdown-toggle',
          text: gettext('Download'),
          titleAttr: gettext('Download results'),
          // Top level: CSV vs. Excel
          buttons: [{
            extend: 'collection',
            text: 'CSV',
            buttons: [
              {
                text: gettext('All results with all columns'),
                action: makeDownloadFunction(false, false, false)
              }, {
                text: gettext('All results with visible columns'),
                action: makeDownloadFunction(false, false, true)
              }, {
                text: gettext('Filtered results with all columns'), 
                action: makeDownloadFunction(false, true, false) 
              }, {
                text: gettext('Filtered results with visible columns'),
                action: makeDownloadFunction(false, true, true)
              }],
            },

            {
              extend: 'collection',
              text: 'Excel',
              buttons: [
                {
                  text: gettext('All results with all columns'),
                  action: makeDownloadFunction(true, false, false)
                }, {
                  text: gettext('All results with visible columns'),
                  action: makeDownloadFunction(true, false, true)
                }, {
                  text: gettext('Filtered results with all columns'),
                  action: makeDownloadFunction(true, true, false)
                }, {
                  text: gettext('Filtered results with visible columns'),
                  action: makeDownloadFunction(true, true, true)
                }
              ],
            }
          ]
        }
      ],
      //pagingType: "input",
      bFilter: false,
      processing: true,
      serverSide: true,
      columns: allColumns,
      stateSave: true,
      stateDuration: -1,
      initComplete: function() {
        $('[data-toggle="tooltip"]').tooltip()
      }
    });
    
    mainDatatable.on('draw.dt', function () {
      $('[data-toggle="tooltip"]').tooltip();
    });

    // built for the datatable download dropdown menu
    function makeDownloadFunction(isExcel, isFiltered, isVisibleColumns) {
      return function () {
        // decides if it's returning visible columns or all columns
        var visibleColumns = isVisibleColumns ? $.map($.makeArray(mainDatatable.columns().visible()), function (visible, index) {
          return visible ? allColumns[index].data : undefined;
        }) : [];

        var form = $("<form action='api/beta_ajax_download' method='post'>{% csrf_token %}</form>");
        form.append($("<input name='data' type='hidden'></input>").attr('value', JSON.stringify({

          searchData: isFiltered ? currentSearchObj : { "items": [] }, // decides if it's returning filtered data or all data

          cols: visibleColumns,
          excel_mode: !!isExcel, // make sure it's a true boolean variable
        })));
        form.appendTo('body').submit().remove();
      }
    }

    mainDatatable.on( 'column-visibility.dt', function ( e, settings, column, state ) {
      $('[data-toggle="tooltip"]').tooltip()
    });

  } else if (currentTab == 'statistics') {
    // Summary statistics.
    var tableId = '#v-summary-statistics';
    destroyPreviousTable(tableId);
    var mainDatatable = $(tableId).DataTable({
      order: [[0, "desc"]],
      ajax: {
        url: searchUrl,
        type: 'POST',
        data: function(d) {
          return JSON.stringify({
            searchData: currentSearchObj,
            tableParams: d,
            output: 'summaryStats'
          });
        },

        // preprocess the returned data to replace * with IMP
        dataSrc: function (json) {
          for (var i = 0, ien = json.data.length; i < ien; i++) {
            json.data[i][0] = json.data[i][0].includes("*") ? gettext(json.data[i][0].slice(0, -1)).concat(impTooltipString) : gettext(json.data[i][0]);
          }
          return json.data;
        },

        fail: function (xhr, status, error) {
          options.errorMessage = error;
          $("#sv-loader").addClass("display-none");
          $("#sv-loader-error").removeClass("display-none");
        }
      },
      columnDefs: [{
        targets:[1,2], // do not eliminate the HTML parsing in the first column
        type: 'num-fmt',
        render: $.fn.dataTable.render.number(",")
      }],
      bFilter: false,
      paging: false,
      // dom: "<'flex-container'>" +
      //   "<'row'<'col-sm-12'tr>>",
      dom: "<'flex-container'iB>" +
        "<'row'<'col-sm-12'tr>>" +
        "<'row'<'col-sm-5'><'col-sm-7'p>>",
      language: dtLanguage,
      buttons: [
        {
          extend: 'collection',
          text: '<span class="fa fa-columns"></span>',
          className: 'btn btn-info buttons-collection dropdown-toggle',
          text: gettext('Download'),
          // Top level: CSV vs. Excel
          buttons: ['csvHtml5', 'excelHtml5']
        }
      ],
      processing: true,
      initComplete: function () {
        $('[data-toggle="tooltip"]').tooltip()
      }
    });
  } else if (currentTab == 'tables') {
    var getTableElement = function(source) {
      var id = tabData.tables[source].value;
      return tabs.tables[source].options.find(function(x) {
        return x.id == id;
      });
    };
    var getField = function(source) {
      var el = getTableElement(source);
      return el ? fieldMap[el.label] : null;
    };
    var cell = getTableElement("cell");
    var rowElement = getTableElement("row");
    var colElement = getTableElement("column");
    
    var postData = {
      searchData: currentSearchObj,
      output: "pivotTable",
      row_field: rowElement.varName,
      col_field: colElement.varName,
      pivot_functions: cell ? cell.functions : null,
      omit_empty: tabData.tables.options.omitEmpty.toString(),
    };
    var isRange = rowElement && rowElement.hasOwnProperty('range');
    if (isRange) {
      postData.range = rowElement.range;
    }
    // Validate post before issuing AJAX call.

    if (postData.row_field && postData.col_field && postData.pivot_functions) {
      $("#sv-loader").removeClass("display-none");

      $.post(searchUrl, JSON.stringify(postData), function(result) {
        // Produce a table with data content.
        var table = $('#v-tables');
        destroyPreviousTable('#v-tables');
        var columnHeaderRows = 1 + (result.col_extra_headers ? result.col_extra_headers.length : 0);
        var thead = table.find('thead');
        thead.empty();
        // Top-left row is blank.
        var subCells = $.map(Object.keys(cell.functions), function(key) {
          return key[0] == '_' ? undefined : key;
        });
        var totalsHeader = '<th colspan="' + subCells.length + '" rowspan="' + columnHeaderRows + '">' + gettext('Totals') + '</th>';
        var tr = '<tr><th rowspan="' + (columnHeaderRows + (subCells.length > 1 ? 1 : 0)) + '">' + gettext('Year Range') + '</th>';
        // Append extra column headers.
        if (columnHeaderRows > 1) {
          for (var i = 0; i < columnHeaderRows - 1; ++i) {
            var headerRow = result.col_extra_headers[i];
            for (var j = 0; j < headerRow.length; ++j) {
              var headerData = headerRow[j];
              tr += '<th colspan="' + headerData[1] * subCells.length + '">' + headerData[0] + '</th>';
            }
            if (i == 0) {
              tr += totalsHeader;
            }
            tr += '</tr>';
          }
          thead.append(tr);
          tr = '<tr>';
        }
        // Append normal column headers.
        var colTotals = initZeroArray((result.columns.length + 1) * subCells.length);
        for (var i = 0; i < result.columns.length; ++i) {
          tr += '<th colspan="' + subCells.length + '">' + result.columns[i] + '</th>';
        }
        if (columnHeaderRows == 1) {
          tr += totalsHeader;
        }
        tr += '</tr>';
        thead.append(tr);
        if (subCells.length > 1) {
          // Each cell is split into multiple values.
          tr = '<tr>'
          for (var i = 0; i < result.columns.length + 1; ++i) {
            for (var j = 0; j < subCells.length; ++j) {
              tr += '<th>' + subCells[j] + '</th>';
            }
          }
          tr += '</tr>';
          thead.append(tr);
        }
        // Append main data.
        var tbody = table.find('tbody');
        tbody.empty();
        // We first create a dense matrix with all the table numbers.
        // The data can then be processed (e.g. for row/col percentages).
        var mx = [];
        var allRowTotals = [];
        var rowCounts = initZeroArray(result.rows.length);
        var colCounts = initZeroArray((result.columns.length + 1) * subCells.length);
        var weightByCount = cell.hasOwnProperty('avg');
        for (var rowIdx = 0; rowIdx < result.rows.length; ++rowIdx) {
          var currentRowTotals = initZeroArray(subCells.length);
          var allCells = initZeroArray(result.columns.length * subCells.length);
          // The result representation is sparse, so we initially
          // set cell values for the row as Zero and then replace
          // the non-zero entries by reading result.rows[rowIdx].
          for (var rowCell = 0; rowCell < result.cells[rowIdx].length; ++rowCell) {
            var cellData = result.cells[rowIdx][rowCell];
            var colIdx = cellData[0];
            var cellCount = cellData[1].count;
            rowCounts[rowIdx] += cellCount;
            for (var j = 0; j < subCells.length; ++j) {
              var cellValue = cellData[1][subCells[j]];
              var computedIdx = colIdx * subCells.length + j;
              allCells[computedIdx] = cellValue;
              colCounts[computedIdx] += cellCount;
              var aggValue = weightByCount ? cellValue * cellCount : cellValue;
              currentRowTotals[j] += aggValue;
              colTotals[computedIdx] += aggValue;
            }
          }
          mx.push(allCells);
          for (var j = 0; j < subCells.length; ++j) {
            colCounts[allCells.length + j] += rowCounts[rowIdx];
            colTotals[allCells.length + j] += currentRowTotals[j];
          }
          if (weightByCount) {
            for (var j = 0; j < currentRowTotals.length; ++j) {
              currentRowTotals[j] /= rowCounts[rowIdx];
            }
          }
          allRowTotals.push(currentRowTotals);
        }
        if (weightByCount) {
          for (var j = 0; j < colTotals.length; ++j) {
            colTotals[j] /= colCounts[j];
          }
        }
        var format = cell.hasOwnProperty('format') ? cell.format : 'decimal';
        if (cell.hasOwnProperty('processing')) {
          // We require some processing of the table entries.
          if ('perc_row_total' == cell.processing) {
            format = 'percent';
            for (var rowIdx = 0; rowIdx < mx.length; ++rowIdx) {
              for (var colIdx = 0; colIdx < mx[rowIdx].length; ++colIdx) {
                mx[rowIdx][colIdx] /= allRowTotals[rowIdx][colIdx % subCells.length];
              }
              // Row percentages add up to 100%.
              for (var j = 0; j < subCells.length; ++j) {
                allRowTotals[rowIdx][j] = 1.0;
              }
            }
            for (var j = 0; j < colTotals.length; ++j) {
              colTotals[j] /= colTotals[colTotals.length - subCells.length + (j % subCells.length)];
            }
          } else if ('perc_col_total' == cell.processing) {
            format = 'percent';
            for (var rowIdx = 0; rowIdx < mx.length; ++rowIdx) {
              for (var colIdx = 0; colIdx < mx[rowIdx].length; ++colIdx) {
                mx[rowIdx][colIdx] /= colTotals[colIdx];
              }
              // Set row totals as a percentage of the global total.
              for (var j = 0; j < subCells.length; ++j) {
                allRowTotals[rowIdx][j] /= colTotals[mx[rowIdx].length + j];
              }
            }
            // Column totals now should be 100%.
            for (var j = 0; j < colTotals.length; ++j) {
              colTotals[j] = 1.0;
            }
          }
        }
        var fmtFunc = function(x) {
          return x.toLocaleString(undefined, {
            style: format,
            minimumFractionDigits: (format == 'percent' || weightByCount) ? 1 : 0,
            maximumFractionDigits: 1,
          });
        };
        for (var rowIdx = 0; rowIdx < mx.length; ++rowIdx) {
          var rowHeaderText = result.rows[rowIdx];
          if (isRange) {
            // The row header coming from the server contains just the
            // initial element of the range, so we must format it here.
            rowHeaderText = rowHeaderText + '-' + (parseInt(rowHeaderText) + postData.range.gap - 1);
          }
          tr = '<tr><th>' + rowHeaderText + '</th>';
          for (var colIdx = 0; colIdx < mx[rowIdx].length; ++colIdx) {
            tr += '<td class="right">' + fmtFunc(mx[rowIdx][colIdx]) + '</td>';
          }
          // Add row totals.
          for (var j = 0; j < subCells.length; ++j) {
            tr += '<th class="right">' + fmtFunc(allRowTotals[rowIdx][j], true) + '</th>'
          }
          tr += '</tr>';
          tbody.append(tr);
        }
        // Add column totals to the foot.
        var tfoot = table.find('tfoot');
        tfoot.empty();
        tr = '<tr><th>' + gettext('Totals') + '</th>';
        for (var colIdx = 0; colIdx < colTotals.length; ++colIdx) {
          tr += '<th class="right">' + fmtFunc(colTotals[colIdx], true) + '</th>';
        }
        tr += '</tr>';
        tfoot.append(tr);
        table.DataTable({
          scrollX: true,
          scrollCollapse: true,
          pageLength: 15,
          lengthMenu: [
            [15, 50, 100, 200],
            ['15', '50', '100', '200']
          ],
          processing: true,
          dom: "<'flex-container'iB>" +
            "<'row'<'col-sm-12'tr>>" +
            "<'row'<'col-sm-5'><'col-sm-7'p>>",
          language: dtLanguage,
          buttons: [
            {
              extend: 'collection',
              text: '<span class="fa fa-columns"></span>',
              className: 'btn btn-info buttons-collection dropdown-toggle',
              text: gettext('Download'),
              // Top level: CSV vs. Excel
              buttons: ['csvHtml5', 'excelHtml5']
            }
          ],
        });
      }).done(function() {
        $("#sv-loader").addClass("display-none");
      }).fail(function (xhr, status, error) {
        options.errorMessage = error;
        $("#sv-loader").addClass("display-none");
        $("#sv-loader-error").removeClass("display-none");
      });
    }
  } else if (currentTab == 'timeline') {

    var timelineVariableId = tabs.timeline.chart.value;
    var timelineVariable = tabs.timeline.chart.options[timelineVariableId]["varName"];
    var postData = {
      searchData: currentSearchObj,
      output: 'timeline',
      timelineVariable: timelineVariable,
    };
    if (postData.timelineVariable) {
      // if it is a percentage based variable; used to add % to the labels
      var isPercentage = isPercentageAxis([postData.timelineVariable]);
      $( "#sv-loader" ).removeClass( "display-none" );
      $.post(searchUrl, JSON.stringify(postData), function(result) {
        $("#sv-loader").removeClass("display-none");

        var data = [];

        var current_year = result.data[0].year;

        for (var i=0; i<result.data.length; i++) {
          var element = result.data[i];
          for (var j=current_year; j<element.year; j++) {
            var time = Date.parse(j.toString());
            data.push([time, 0]);
          }
          current_year = element.year + 1;
          var time = Date.parse(element.year.toString());
          data.push([time, element.value]);
        }

        // // Convert into HighCharts data format
        // result.data.forEach(function(element){
        //   var time = Date.parse(element.year.toString());
        //   data.push([time, element.value]);
        // });

        // Let Highcharts paint the chart
        Highcharts.chart('hc-timeline', {
          chart: {
            zoomType: 'x',
            style: {
                fontFamily: '-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol", serif'
            }
          },
          title: {
              text: ''
          },
          subtitle: {
            text: document.ontouchstart === undefined ?
              gettext('Click and drag in the plot area to zoom in') : gettext('Pinch the chart to zoom in'),
          },
          xAxis: {
            type: 'datetime',
          },
          yAxis: {
            title: {
              text: gettext('Value'),
            },
            min: 0,
            startOnTick: true,
            labels: {
              formatter: function() {
                var postfix = isPercentage ? "%" : ""; // for percentage based charts
                return this.value + postfix;
              }
            },
          },
          legend: {
            enabled: false
          },
          credits: {
            enabled: false,
          },
          tooltip: {
              formatter: function() {
                  var year = moment.unix(this.x / 1000).utc().format("YYYY");
                  var postfix = isPercentage ? "%" : ""; // for percentage based charts
              return gettext('Year ') + year + ': ' + '<b>' + this.y + postfix +'</b> ';
              }
          },
          lang: {
            noData: gettext('We are sorry but there is no data to display or an error has occurred.'),
          },
          plotOptions: {
            area: {
              marker: {
                radius: 2
              },
              lineWidth: 2,
              states: {
                hover: {
                  lineWidth: 2
                }
              },
              threshold: null
            }
          },
          exporting: {
            buttons: {
              contextButton: {
                menuItems: ["printChart",
                  "separator",
                  "downloadPNG",
                  "downloadJPEG",
                  "downloadPDF",
                  "downloadSVG",
                  "separator",
                  "downloadCSV",
                  "downloadXLS",
                  //"viewData",
                  "openInCloud"]
              }
            }
          },
          series: [{
            type: 'area',
            name: timelineVariable,
            data: data,
            color: HC_THEME_COLOR
          }]
        });

      }).done(function(){
        $( "#sv-loader" ).addClass( "display-none" );
      }).fail(function (xhr, status, error) {
        options.errorMessage = error;
        $("#sv-loader").addClass("display-none");
        $("#sv-loader-error").removeClass("display-none");
      });
    }


  } else if (currentTab == 'visualization') {
    loader.loadScript(STATIC_URL + 'scripts/library/d3.min.js')
      .then(function() {


        // Ready to plot graphs!
        var allChartTypes = {
          "xy-chart-tab": ["scatter", "x", "y"],
          "bar-chart-tab": ["bar", "x", "y"],
          "donut-chart-tab": ["donut", "sectors", "values"]
        };
        var chartType = allChartTypes[$('a.active.side-control-tab').attr('id')];

        // map the varName to the ids for Y
        var yIds = tabs.visualization[chartType[0]][chartType[2]].value;
        var yAxes = [];
        if (Array.isArray(yIds)) {
          yIds.forEach(function(element, index, yIds) {
            yAxes[index] = tabs.visualization[chartType[0]][chartType[2]].options[yIds[index]]["varName"];
          });
        } else {
          yAxes = tabs.visualization[chartType[0]][chartType[2]].options[yIds]["varName"];
        }

        // map the varName to the ids for X
        var xId = tabs.visualization[chartType[0]][chartType[1]].value;
        var xAxes = tabs.visualization[chartType[0]][chartType[1]].options[xId]["varName"];

        var postData = {
          searchData: currentSearchObj,
          output: 'graph',
          graphData: {
            xAxis: xAxes,
            yAxes: chartType[0] == 'donut' ? [yAxes] : yAxes
          }
        };

        if (postData.graphData.xAxis && postData.graphData.yAxes.length > 0) {
          $("#sv-loader").removeClass("display-none");
          $.post(searchUrl, JSON.stringify(postData), function(series) {
            $("#sv-loader").removeClass("display-none");
            if (chartType[0] == 'scatter') {
              $("#tabs-visualization-xy").empty();
              // Compute ordinal scales.
              var xValues = [];
              var seriesNames = [];
              var maxValue = 0;
              for (var yid in series) {
                seriesNames.push(yid);
                var items = series[yid];
                for (var i = 0; i < items.length; ++i) {
                  xValues.push(items[i].x);
                  if (items[i].value > maxValue) maxValue = items[i].value;
                }
              }
              xValues = d3.set(xValues).values().map(function(s) {
                return parseFloat(s);
              });

              var margin = {
                  top: 90 + 20 * (seriesNames.length - 2),
                  right: 15,
                  bottom: 110,
                  left: 80
                },
                width = 960 - margin.left - margin.right,
                height = 460 - margin.top - margin.bottom;
              var x = d3.scale.linear()
                .domain([d3.min(xValues), d3.max(xValues)])
                .nice()
                .range([0, width]);
              var y = d3.scale.linear()
                .domain([0, maxValue * 1.1])
                .range([height, 0]);
              var color = d3.scale.category10();
              var xAxis = d3.svg.axis()
                .scale(x)
                .orient("bottom")
                .tickSize(-height);
              if (postData.graphData.xAxis == 'var_imp_arrival_at_port_of_dis') {
                xAxis = xAxis.tickFormat(function(d, i) {
                  return d.toString();
                });
              }
              var yAxis = d3.svg.axis()
                .scale(y)
                .orient("left")
                .tickSize(-width);
              // If percentage, add to ticks.
              if (isPercentageAxis(postData.graphData.yAxes)) {
                yAxis.tickFormat(function(d) { return parseInt(d, 10) + "%"; });
              }
              var svg = d3.select("#tabs-visualization-xy")
                .append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
              svg.append("g")
                .attr("class", "x axis")
                .attr("transform", "translate(0," + (height + 4) + ")")
                .call(xAxis);
              svg.append("g")
                .attr("class", "y axis")
                .call(yAxis)
                .append("text")
                .attr("x", 0)
                .attr("y", 0)
                .attr("dy", "-1em")
                .style("text-anchor", "end")
                .text(gettext('Value'));

              var legend = svg.selectAll(".legend")
                .data(seriesNames)
                .enter()
                .append("g")
                .attr("class", "legend")
                .attr("transform", function(d, i) {
                  return "translate(0," + (i * 20 - margin.top + 30) + ")";
                });

              legend.append("rect")
                .attr("x", width - 18)
                .attr("width", 18)
                .attr("height", 18)
                .style("fill", color);

              legend.append("text")
                .attr("x", width - 24)
                .attr("y", 9)
                .attr("dy", ".35em")
                .style("text-anchor", "end")
                .text(function(d) {
                  return d;
                });

              for (var yid in series) {
                var line = d3.svg.line()
                  .x(function(d) {
                    return x(d.x);
                  })
                  .y(function(d) {
                    return y(d.value);
                  });
                svg.append('svg:path')
                  .attr('d', line(series[yid]))
                  .attr('stroke', color(yid))
                  .attr('stroke-width', 2)
                  .attr('fill', 'none');
              }
            } else if (chartType[0] == 'bar') {
              $("#tabs-visualization-bar").empty();
              // Compute ordinal scales.
              var labels = [];
              var seriesNames = [];
              var maxValue = 0;
              for (var yid in series) {
                seriesNames.push(yid);
                var items = series[yid];
                for (var i = 0; i < items.length; ++i) {
                  labels.push(items[i].x);
                  if (items[i].value > maxValue) maxValue = items[i].value;
                }
              }
              labels = d3.set(labels).values();

              var wrap = function(text) {
                var w = margin.bottom - 10;
                text.each(function() {
                  var text = d3.select(this),
                    words = text.text().split(/\s+/).reverse(),
                    word,
                    line = [],
                    lineNumber = 0,
                    lineHeight = 1.1, // ems
                    y = text.attr("y"),
                    dy = parseFloat(text.attr("dy")),
                    tspan = text.text(null).append("tspan").attr("x", 0).attr("y", y).attr("dy", dy + "em");
                  while (word = words.pop()) {
                    line.push(word);
                    tspan.text(line.join(" "));
                    if (tspan.node().getComputedTextLength() > w) {
                      line.pop();
                      tspan.text(line.join(" "));
                      line = [word];
                      tspan = text.append("tspan")
                        .attr("x", 0)
                        .attr("y", y)
                        .attr("dy", ++lineNumber * lineHeight + dy + "em").text(word);
                    }
                  }
                });
              }
              // Create D3js graph. This graph has two X-axes,
              // x0 represents the labels on the data items, while
              // x1 represents the name of the series. This is
              // used in a way that all the data items across different
              // series sharing the same label are grouped together.
              var margin = {
                  top: 90 + 20 * (seriesNames.length - 2),
                  right: 10,
                  bottom: 110,
                  left: 80
                },
                width = 960 - margin.left - margin.right,
                height = 460 - margin.top - margin.bottom;
              var x0 = d3.scale.ordinal()
                .domain(labels)
                .rangeRoundBands([0, width], .08);
              var x1 = d3.scale.ordinal()
                .domain(seriesNames)
                .rangeRoundBands([0, x0.rangeBand()]);
              var y = d3.scale.linear()
                .domain([0, maxValue * 1.1])
                .range([height, 0]);
              var color = d3.scale.category10();
              var xAxis = d3.svg.axis()
                .scale(x0)
                .orient("bottom");
              var yAxis = d3.svg.axis()
                .scale(y)
                .orient("left");
              // If percentage, add to ticks.
              if (isPercentageAxis(postData.graphData.yAxes)) {
                yAxis.tickFormat(function(d) { return parseInt(d, 10) + "%"; });
              }
              var svg = d3.select("#tabs-visualization-bar")
                .append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
              // X axis with rotated labels.
              svg.append("g")
                .attr("class", "x axis")
                .attr("transform", "translate(0," + height + ")")
                .call(xAxis)
                .selectAll("text")
                .style("text-anchor", "end")
                .attr("dx", "-.8em")
                .attr("dy", ".15em")
                .attr("transform", function(d) {
                  return "rotate(-45)"
                })
                .call(wrap);
              svg.append("g")
                .attr("class", "y axis")
                .call(yAxis)
                .append("text")
                .attr("x", 0)
                .attr("y", 0)
                .attr("dy", "-1em")
                .style("text-anchor", "end")
                .text("Value");

              var legend = svg.selectAll(".legend")
                .data(seriesNames)
                .enter()
                .append("g")
                .attr("class", "legend")
                .attr("transform", function(d, i) {
                  return "translate(0," + (i * 20 - margin.top + 30) + ")";
                });

              legend.append("rect")
                .attr("x", width - 18)
                .attr("width", 18)
                .attr("height", 18)
                .style("fill", color);

              legend.append("text")
                .attr("x", width - 24)
                .attr("y", 9)
                .attr("dy", ".35em")
                .style("text-anchor", "end")
                .text(function(d) {
                  return d;
                });

              // Add label groups.
              var gLabels = svg.selectAll(".label")
                .data(labels)
                .enter()
                .append("g")
                .attr("class", "g")
                .attr("transform", function(d) {
                  return "translate(" + x0(d) + ",0)";
                });
              gLabels
                .append("line")
                .attr("x1", 0)
                .attr("x2", x0.rangeBand())
                .attr("y1", height)
                .attr("y2", height)
                .style('stroke-width', 0.5)
                .style('stroke', 'black');
              // Add bars to all label groups.
              gLabels.selectAll("rect")
                .data(function(d) {
                  // Filter by label.
                  var res = [];
                  for (var yid in series) {
                    var items = series[yid];
                    for (var i = 0; i < items.length; ++i) {
                      if (d == items[i].x) {
                        res.push({
                          series: yid,
                          value: items[i].value
                        });
                      }
                    }
                  }
                  return res;
                })
                .enter()
                .append("rect")
                .attr("width", x1.rangeBand())
                .attr("x", function(d) {
                  return x1(d.series);
                })
                .attr("y", function(d) {
                  return y(d.value);
                })
                .attr("height", function(d) {
                  return height - y(d.value);
                })
                .style("fill", function(d) {
                  return color(d.series);
                });
            } else if (chartType[0] == 'donut') {
              $("#tabs-visualization-donut").empty();
              var label = Object.keys(series)[0];
              var data = series[label];
              data.sort(function(a, b) {
                return a.value - b.value;
              });
              var sum = d3.sum(data, function(d) {
                return d.value;
              });
              var margin = {
                  top: 20,
                  right: 10,
                  bottom: 50,
                  left: 20
                },
                width = 960 - margin.left - margin.right,
                height = 460 - margin.top - margin.bottom;
              var color = d3.scale.category20c();
              var radius = Math.min(width, height) / 2 - margin.top;

              var arc = d3.svg.arc()
                .outerRadius(radius * 0.8)
                .innerRadius(radius * 0.4);

              var outerArc = d3.svg.arc()
                .outerRadius(radius * 0.9)
                .innerRadius(radius * 0.9);

              var angleShift = Math.min(-0.1, -Math.min(0.25, data[data.length - 1].value / sum));
              var pie = d3.layout.pie()
                .startAngle(angleShift * Math.PI)
                .endAngle((2 + angleShift) * Math.PI)
                .value(function(d) {
                  return d.value;
                });
              var svg = d3.select("#tabs-visualization-donut")
                .append("svg")
                .attr("width", width)
                .attr("height", height)
                .append("g")
                .attr("transform", "translate(" + (margin.left + width / 2) + "," + (margin.top + height / 2) + ")");

              svg.append("text")
                .attr("left", margin.left + width / 2)
                .attr("text-anchor", "middle")
                .attr("y", 10 - height / 2)
                .attr("font-size", 20)
                .text(label);

              var g = svg.selectAll(".arc")
                .data(pie(data))
                .enter().append("g")
                .attr("class", "arc");

              var key = function(d) {
                return d.data.x;
              };
              g.append("path")
                .attr("d", arc)
                .style("fill", function(d) {
                  return color(key(d));
                });

              svg.append("g")
                .attr("class", "labels");
              svg.append("g")
                .attr("class", "lines");
              // Text labels.
              var text = svg.select(".labels").selectAll("text")
                .data(pie(data), key);

              var opacityFn = function(d) {
                var x = Math.sin(d.endAngle - d.startAngle);
                return Math.min(0.5, Math.pow(x, 1.5) * 15);
              };
              var isPercentage = isPercentageAxis(postData.graphData.yAxes);
              text.enter()
                .append("text")
                .style('opacity', opacityFn)
                .attr("dy", ".35em")
                .text(function(d) {
                  return key(d) + " = " + d.value.toLocaleString() + 
                    (isPercentage ? '%' : '');
                });

              var midAngle = function(d) {
                return d.startAngle + (d.endAngle - d.startAngle) / 2;
              };

              text.transition().duration(1000)
                .attrTween("transform", function(d) {
                  this._current = this._current || d;
                  var interpolate = d3.interpolate(this._current, d);
                  this._current = interpolate(0);
                  return function(t) {
                    var d2 = interpolate(t);
                    var pos = outerArc.centroid(d2);
                    pos[0] = radius * (midAngle(d2) < Math.PI ? 1 : -1);
                    return "translate(" + pos + ")";
                  };
                })
                .styleTween("text-anchor", function(d) {
                  this._current = this._current || d;
                  var interpolate = d3.interpolate(this._current, d);
                  this._current = interpolate(0);
                  return function(t) {
                    var d2 = interpolate(t);
                    return midAngle(d2) < Math.PI ? "start" : "end";
                  };
                });

              text.exit()
                .remove();

              // Polylines to labels.
              var polyline = svg.select(".lines").selectAll("polyline")
                .data(pie(data), key);

              polyline.enter()
                .append("polyline");

              polyline.transition().duration(1000)
                .style('opacity', opacityFn)
                .attrTween("points", function(d) {
                  this._current = this._current || d;
                  var interpolate = d3.interpolate(this._current, d);
                  this._current = interpolate(0);
                  return function(t) {
                    var d2 = interpolate(t);
                    var pos = outerArc.centroid(d2);
                    pos[0] = radius * 0.95 * (midAngle(d2) < Math.PI ? 1 : -1);
                    return [arc.centroid(d2), outerArc.centroid(d2), pos];
                  };
                });

              polyline.exit()
                .remove();
            }
          }).done(function() {
            $("#sv-loader").addClass("display-none");
          }).fail(function (xhr, status, error) {
            options.errorMessage = error;
            $("#sv-loader").addClass("display-none");
            $("#sv-loader-error").removeClass("display-none");
          });
        } else {
          // TODO: Clear existing chart?
        }
      });
  } else if (currentTab == 'maps') {
    $("#sv-loader").removeClass("display-none");
    $("#animation-container").addClass("display-none");
    $("#maps").addClass("display-none");
    // TODO: Map year should be computed based on year range of search.
    // We can do it in the client side (easier).
    // for reference: voyages.apps.assessment.globals.get_map_year
    var postData = {
      searchData: currentSearchObj,
      output: 'mapFlow'
    };
    var mapFlowSearchCallback = function() {
      var $map = $('#map');
      $.post(searchUrl, JSON.stringify(postData), function(result) {
        $("#sv-loader").removeClass("display-none");

        eval(result);
        voyagesMap.clear();
      }).done(function(){
        $("#sv-loader").addClass("display-none");
        $("#maps").removeClass("display-none");
        loader.resizeMap(); // resize first before adding the networkflow
        try {
          voyagesMap.setNetworkFlow(ports, flows);
        } catch (e) {
          console.log(e);
        }
        }).fail(function (xhr, status, error) {
          options.errorMessage = error;
          $("#sv-loader").addClass("display-none");
          $("#sv-loader-error").removeClass("display-none");
        });
    };
    loader.loadMap(mapFlowSearchCallback);
  } else if (currentTab == 'animation') {
    $("#maps").addClass("display-none");
    $("#sv-loader").removeClass("display-none");
    $("#animation-container").removeClass("display-none");
    
    var postData = {
      searchData: currentSearchObj,
      output: 'mapAnimation'
    };
    var mapAnimationSearchCallback = function() {
      var $map = $('#map');
      $.post(searchUrl, JSON.stringify(postData), function(result) {
        $("#sv-loader").removeClass("display-none");

        if (result) { // add title to the chart
          $("#tab-map-voyage-value").text(numberWithCommas(result.length));
        }
        voyagesMap.clear();
        $('.animationElement').show();
        animationHelper.startAnimation(result);
      }).done(function(){
        animationHelper.reset();
        $("#sv-loader").addClass("display-none");
        $("#maps").removeClass("display-none");
        loader.resizeMap();
        // get title here I'd say
        }).fail(function (xhr, status, error) {
          options.errorMessage = error;
          $("#sv-loader").addClass("display-none");
          $("#sv-loader-error").removeClass("display-none");
        });
    };
    // $('#loading').show();
    loader.loadMap(function() {
      loader.loadAnimationScripts(mapAnimationSearchCallback);
    });
  }
}

// helpers

var loader = new LazyLoader();

// Helper to load CSS files and scripts on demand.
function LazyLoader() {
  var self = this;
  self.loadedFiles = {};
  self.loadCss = function(url) {
    $('head').append('<link rel="stylesheet" href="' + url + '" type="text/css" />');
  };
  self.loadScript = function(url) {
    var dfd = new $.Deferred();
    var callback = function() {
      dfd.resolve('script loaded');
      self.loadedFiles[url] = true;
    };
    if (self.loadedFiles.hasOwnProperty(url)) {
      callback();
    } else {
      var script = document.createElement('script');
      script.type = 'text/javascript';
      script.async = false;
      script.onreadystatechange = callback;
      script.onload = callback;
      script.src = url;
      document.getElementsByTagName('head')[0].appendChild(script);
    }
    return dfd;
  };
  self.animationScriptsLoaded = false;
  self.mapLoaded = false;
  self.resizeMap = function() {
    $("#map").height($(window).height() - 200);
    voyagesMap._map.invalidateSize();
  };
  self.loadMap = function(done) {
    if (self.animationScriptsLoaded) {
      animationHelper.stopAnimation();
    }
    $('#map').show();
    if (!self.mapLoaded) {
      self.loadCss(STATIC_URL + 'maps/css/leaflet.css');
      self.loadCss(STATIC_URL + 'maps/css/MarkerCluster.css');
      self.loadCss(STATIC_URL + 'maps/css/MarkerCluster.Default.css');
      self.loadScript(STATIC_URL + 'maps/js/leaflet.js')
        .then(self.loadScript(STATIC_URL + 'maps/js/leaflet.markercluster.js'))
        .then(self.loadScript(STATIC_URL + 'maps/js/leaflet.polylineDecorator.js'))
        .then(function() {
          $.when(
              self.loadScript(STATIC_URL + 'maps/js/routeNodes.js'),
              self.loadScript(STATIC_URL + 'maps/js/voyagesMap.js'),
            )
            .then(function() {
              voyagesMap.
              init('1750', STATIC_URL + 'maps/', routeNodes, links).
              setMaxPathWidth(20).
              setPathOpacity(0.75);
              $(window).on("resize", self.resizeMap).trigger("resize");
              voyagesMap._map.invalidateSize();
              self.mapLoaded = true;
              done();
            });
        });
    } else {
      done();
    }
  };
  self.loadAnimationScripts = function(done) {
    if (!self.animationScriptsLoaded) {
      self.loadCss(STATIC_URL + 'scss/legacy/animation.css');
      $.when(
          self.loadScript(STATIC_URL + 'scripts/library/d3.min.js'),
          self.loadScript(STATIC_URL + 'scripts/library/jquery-ui@1.12.1.min.js'),
          self.loadScript(STATIC_URL + 'maps/js/arc.js'),
          self.loadScript(STATIC_URL + 'maps/js/leaflet.geodesic.min.js')
        )
        .then(self.loadScript(STATIC_URL + 'scripts/vue/includes/animation.js'))
        .then(function() {
          self.animationScriptsLoaded = true;
          done();
        });
    } else {
      done();
    }
  };
  return self;
}
