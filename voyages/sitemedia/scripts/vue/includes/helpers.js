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

function countChanged(object) {
	var count = 0;
	for (key1 in object) {
		if (key1 !== "count") {
			if (object[key1].changed) {
				count += 1;
			}
		}
	}
	return count;
}

function countActivated(object) {
	var count = 0;
	for (key1 in object) {
		if (key1 !== "count") {
			if (object[key1].activated) {
				count += 1;
			}
		}
	}
	return count;
}

function countMenuChanged(object) {
	var count = 0;
	for (key1 in object) {
		if (key1 !== "count") {
			count = count + object[key1].count.changed;
		}
	}
	return count;
}

function countMenuActivated(object) {
	var count = 0;
	for (key1 in object) {
		if (key1 !== "count") {
			count = count + object[key1].count.activated;
		}
	}
	return count;
}

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
	debugger;
	for (key1 in filter[group][subGroup]) {
		if (key1 !== "count") {
			filter[group][subGroup][key1].value["searchTerm0"] = null;
			filter[group][subGroup][key1].value["searchTerm1"] = null;
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
	} else if (key == "is between") {
		return "is between";
	} else if (key == "equals to") {
		return "equals";
	} else if (key == "contains") {
    return "contains";
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
								console.log(filter[key1][key2][key3].value["op"]);
								console.log(item["op"]);

								item["searchTerm"] = [filter[key1][key2][key3].value["searchTerm0"], filter[key1][key2][key3].value["searchTerm1"]];
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
// helpers
