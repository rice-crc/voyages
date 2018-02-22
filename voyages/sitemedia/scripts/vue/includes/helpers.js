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
        filter[group][subGroup][key1].value["searchTerm"] = [];
      } else {
        filter[group][subGroup][key1].value["searchTerm0"] = null;
  			filter[group][subGroup][key1].value["searchTerm1"] = null;
      }
      // TODO accomodate has one of; contains; equals to;
			filter[group][subGroup][key1].value["op"] = "equals to";
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
                  item["searchTerm"] = filter[key1][key2][key3].value["searchTerm"];
                } else {
                  item["searchTerm"] = [filter[key1][key2][key3].value["searchTerm0"], filter[key1][key2][key3].value["searchTerm1"]];
                }
								item["varName"] = filter[key1][key2][key3].varName;
								items.push(item);
							}
						}
					}
				}
			}
		}
	}

	// placeholder
	var item = {};
	item["op"] = "is between";
	item["searchTerm"] = [1514, 1866];
	item["varName"] = "imp_arrival_at_port_of_dis";
	items.push(item);
	// placeholder

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

// helpers
