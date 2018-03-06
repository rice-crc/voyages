// helpers

var generateRandomKey = function() {
  var ALPHABET = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
  var ID_LENGTH = 8;
  var rtn = '';
  for (var i = 0; i < ID_LENGTH; i++) {
    rtn += ALPHABET.charAt(Math.floor(Math.random() * ALPHABET.length));
  }
  return rtn;
}

var generateUniqueRandomKey = function(previous) {
  var UNIQUE_RETRIES = 9999;
  previous = previous || [];
  var retries = 0;
  var id;
  // Try to generate a unique ID,
  // i.e. one that isn't in the previous.
  while(!id && retries < UNIQUE_RETRIES) {
    id = generateRandomKey();
    if(previous.indexOf(id) !== -1) {
      id = null;
      retries++;
    }
  }
  return id;
};

function activateFilter(filter, group, subGroup, filterValues) {
	for (key1 in filter[group][subGroup]) {
		if (key1 !== "count") {
			if (filter[group][subGroup][key1].changed) {
				// filter[group][subGroup][key1].value["searchTerm0"] = filter[group][subGroup][key1].value["searchTerm0"];
				// filter[group][subGroup][key1].value["searchTerm1"] = filter[group][subGroup][key1].value["searchTerm1"];
				// filter[group][subGroup][key1].value["op"] = filter[group][subGroup][key1].value["op"];
				filter[group][subGroup][key1].changed = true;
				filter[group][subGroup][key1].activated = true;
			}
		}
	}
}

function resetFilter(filter, group, subGroup) {
	for (key1 in filter[group][subGroup]) {
		if (key1 !== "count") {
      if (filter[group][subGroup][key1].value["searchTerm0"] === undefined) {
        filter[group][subGroup][key1].value["searchTerm"] = filter[group][subGroup][key1].default["searchTerm"];
      } else {
        filter[group][subGroup][key1].value["searchTerm0"] = filter[group][subGroup][key1].default["searchTerm0"];
  			filter[group][subGroup][key1].value["searchTerm1"] = filter[group][subGroup][key1].default["searchTerm1"];
      }
			filter[group][subGroup][key1].value["op"] = filter[group][subGroup][key1].default["op"];
			filter[group][subGroup][key1].changed = false;
			filter[group][subGroup][key1].activated = false;
		}
	}
}

function replaceKey(key) {
	if (key == "is less than") {
		return "is at most"
	} else if (key == "is more than") {
		return "is at least";
	} else if (key == "equals to") {
		return "equals";
	} else {
    return key;
  }
}

function searchAll(filter) {
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
                      if (selection == filter[key1][key2][key3].options.data[0].id) {
                        // select all
                        filter[key1][key2][key3].options.data[0].children.forEach(function(broadRegion) {
                          broadRegion.children.forEach(function(region) {
                            region.children.forEach(function(subRegion) {
                              searchTerm.push(subRegion.id);
                            })
                          })
                        });
                      } else {
                        // broadRegion
                        filter[key1][key2][key3].options.data[0].children.forEach(function(broadRegion) {
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
                      filter[key1][key2][key3].options.data[0].children.forEach(function(options) {
                        searchTerm.push(options.id);
                      });
                    } else {
                      searchTerm = filter[key1][key2][key3].value["searchTerm"];
                    }

                    item["searchTerm"] = searchTerm;
                  } else {
                    item["searchTerm"] = filter[key1][key2][key3].value["searchTerm"];
                  }
                } else {
                  item["searchTerm"] = [filter[key1][key2][key3].value["searchTerm0"], filter[key1][key2][key3].value["searchTerm1"]];
                }

                // TODO: fix a bug with the backend: it should use _idnum and not _id
                if (filter[key1][key2][key3].varName.slice(-3) == "_id") {
                  item["varName"] = filter[key1][key2][key3].varName + "num";
                } else {
                  item["varName"] = filter[key1][key2][key3].varName;
                }

                // TODO: backend patch
                if (filter[key1][key2][key3].varName == "nationality"
                  || filter[key1][key2][key3].varName == "rig_of_vessel"
                  || filter[key1][key2][key3].varName == "outcome_voyage"
                  || filter[key1][key2][key3].varName == "outcome_slaves"
                  || filter[key1][key2][key3].varName == "outcome_ship_captured"
                  || filter[key1][key2][key3].varName == "outcome_owner"
                  || filter[key1][key2][key3].varName == "resistance"

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
  items.map(function(item){
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

	// placeholder

alert(JSON.stringify(items));
	return items;
}

function resetAll() {

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

// load options to the main search filter, such as flag, rig, outcomes
function loadOptions(vm, variables) {
  var promises = [];
  for (variable in variables) {
    var varName = "var_" + variables[variable].varName;
    promises.push(axios.post('/voyage/var-options', {
      var_name: varName,
    }));
  }
  // fulfil promises
  axios.all(promises).then(function(results) {
    results.forEach(function(response) {
      // fill in
      for (variable in variables) {
        var varName = "var_" + variables[variable].varName;
        if ( varName == response.data.var_name) {
          response.data.data.map(function(data) {
            data["id"] = data["value"];
          });
          variables[variable]["options"].data[0]["children"] = response.data.data;
        }
      }
    })
  });
}

// loadPlaces
function loadPlaces(vm, groups) {
  var promises = [];
  for (subGroup in groups) {
    if (subGroup !== "count") {
      for (variable in groups[subGroup]) {
        if (variable !== "count") {
          var varName = groups[subGroup][variable].varName;
          promises.push(axios.post('/voyage/filtered-places', {
            var_name: varName,
          }));
        }
      }
    }
  }

  axios.all(promises).then(function(results) {
    results.forEach(function(response) {
      var varName = response.data.filtered_var_name;
      var options = parsePlaces(response);

      // fill in
      for (subGroup in groups) {
        if (subGroup !== "count") {
          for (variable in groups[subGroup]) {
            if (variable !== "count") {
              if (groups[subGroup][variable].varName == varName) {
                // groups[subGroup][variable]["options"].data = response.data;
                groups[subGroup][variable]["options"].data = options;
              }
            }
          }
        }
      }
    })
  });
}


// loadPlaces
function loadIndividualPlace(vm, variable) {
  var promises = [];

  // var varName = "var_" + variable.varName;
  // promises.push(axios.post('/voyage/filtered-places', {
  //   var_name: varName,
  // }));
  promises.push(axios.post('/voyage/filtered-places', {}));

  axios.all(promises).then(function(results) {
    results.forEach(function(response) {
      var varName = response.data.filtered_var_name;
      var options = parsePlaces(response);

      // fill in
      variable["options"].data = options;
    });
  });
}

// parsePlaces function
var parsePlaces = function(response) {
  var data = processPlacesAjax(response.data.data);
  var options = [{
    id: 0,
    label: "Select All",
    children: null
  }];

  // fill select all
  options = [{
    id: 0,
    code: 0,
    label: "Select All",
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

function sortNumber(a,b) {
    return a - b;
}

// helpers
