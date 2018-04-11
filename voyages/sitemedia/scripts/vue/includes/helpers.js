// helpers
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
                  // TODO patch for date variables
                  if (filter[key1][key2][key3].constructor.name === "DateVariable") {
                    var searchTerm0 = filter[key1][key2][key3].value["searchTerm0"] + "-01-01T00:00:00Z";
                    var searchTerm1 = null;
                    if (filter[key1][key2][key3].value["searchTerm1"] !== null) {
                      searchTerm1 = filter[key1][key2][key3].value["searchTerm1"] + "-12-31T23:59:59Z";
                    }
                    item["searchTerm"] = [searchTerm0, searchTerm1];
                  } else {
                    item["searchTerm"] = [filter[key1][key2][key3].value["searchTerm0"], filter[key1][key2][key3].value["searchTerm1"]];
                  }
                }

                // TODO: fix a bug with the backend: it should use _idnum and not _id except for voyage_id
                if (filter[key1][key2][key3].varName.slice(-3) == "_id" && filter[key1][key2][key3].varName !== "voyage_id") {
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

function initZeroArray(length) {
  var arr = [];
  while (length--) {
    arr.push(0);
  }
  return arr;
}

function refreshUi(filter, currentTab, tabData) {
  // Update UI after search query was changed,
  // or a tab was selected.
  var currentSearchObj = {
    items: searchAll(filter),
    orderBy: []
  };
  var searchUrl = "876167cf-bc40-44f7-9557-ee8117d94008/beta_ajax_search";
  if (currentTab == 'results') {
    // Results DataTable
    var pageLength = {
      extend: 'pageLength',
      className: 'btn btn-info buttons-collection dropdown-toggle',
    };
    // TEMP Yang: I think there is an option for destroying the
    // old table (destroy: true) that you can pass so we avoid 
    // this call?
    if ($.fn.DataTable.isDataTable('#results_main_table')) {
      $('#results_main_table').DataTable().destroy();
    }  
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
          $('#results_main_table').on( 'click', 'tr', function () {
              searchBar.row.data = mainDatatable.row( this ).data();
          });
  
          // console.log(JSON.stringify({ searchData: currentSearchObj, tableParams: d, output: 'resultsTable' }))
          return JSON.stringify({
            searchData: currentSearchObj,
            tableParams: d,
            output: 'resultsTable'
          });
        }
      },
  
  
      // dom: 'ifrtBp',
      dom:  "<'flex-container'iB>" +
            "<'row'<'col-sm-12'tr>>" +
            "<'row'<'col-sm-5'><'col-sm-7'p>>",
      lengthMenu: [
        [10, 25, 50, 100],
        ['10 rows', '25 rows', '50 rows', '100 rows']
      ],
  
      buttons: [
        columnToggleMenu,
        pageLength,
        // {
        //   extend: 'collection',
        //   // text: '<span class="fa fa-columns" style="vertical-align: middle;"></span>',
        //   className: 'btn btn-info buttons-collection dropdown-toggle',
        //   text: 'Download',
        //   titleAttr: 'Download results',
        //   buttons: [
        //     // {
        //     // 	text: 'CSV - not implemented',
        //     // 	action: function() { alert('not implemented yet'); },
        //     // },
        //     {
        //       text: 'Excel',
        //       action: function() {
        //         var visibleColumns = $.map($.makeArray(mainDatatable.columns().visible()), function(visible, index) {
        //           return visible ? allColumns[index].data : undefined;
        //         });
        //         var form = $("<form action='876167cf-bc40-44f7-9557-ee8117d94008/beta_ajax_download' method='post'>{% csrf_token %}</form>");
        //         form.append($("<input name='data' type='hidden'></input>").attr('value', JSON.stringify({
        //           searchData: currentSearchObj,
        //           cols: visibleColumns
        //         })));
        //         form.appendTo('body').submit().remove();
        //       },
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
      colReorder: true,
      initComplete: function() {
        $(function () {
          $('[data-toggle="tooltip"]').tooltip()
        })
      }
    });
  } else if (currentTab == 'statistics') {
    // Summary statistics.
    var tableId = '#v-summary-statistics';
    if ($.fn.DataTable.isDataTable(tableId)) {
      $(tableId).DataTable().destroy();
    }  
    var mainDatatable = $(tableId).DataTable({
      ajax: {
        url: searchUrl,
        type: 'POST',
        data: function(d) {
          return JSON.stringify({
            searchData: currentSearchObj,
            tableParams: d,
            output: 'summaryStats'
          });
        }
      },
      bFilter: false,
      paging: false,
      dom:  "<'flex-container'>" +
            "<'row'<'col-sm-12'tr>>"
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
    var cell = getTableElement('cell');
    var postData = {
      searchData: currentSearchObj,
      output: "pivotTable",
      row_field: getField("row"),
      col_field: getField("column"),
      pivot_functions: cell ? cell.functions : null,
    };
    // Validate post before issuing AJAX call.
    if (postData.row_field && postData.col_field && postData.pivot_functions) {
      $.post(searchUrl, JSON.stringify(postData), function(result) {
        // Produce a table with data content.
        var table = $('#v-tables');
        var columnHeaderRows = 1 + (result.col_extra_headers ? result.col_extra_headers.length : 0);
        var thead = table.find('thead');
        thead.empty();
        // Top-left row is blank.
        var subCells = $.map(Object.keys(cell.functions), function(key) { return key[0] == '_' ? undefined : key; });
        var totalsHeader = '<th colspan="' + subCells.length + '" rowspan="' + columnHeaderRows + '">' + gettext('Totals') + '</th>';
        var tr = '<tr><th rowspan="' + columnHeaderRows + (subCells.length > 1 ? 1 : 0) + '"></th>';
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
          tr = '<tr><th>' + result.rows[rowIdx] + '</th>';
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
      });
    }
  }
}

// helpers
