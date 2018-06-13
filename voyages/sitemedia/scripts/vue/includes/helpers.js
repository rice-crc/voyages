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
	} else if (key == "is equal to") {
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

function destroyPreviousTable(id) {
  try {
    if ($.fn.DataTable.isDataTable(id)) {
      $(id).DataTable().destroy();
    }
  } catch(e) {
    console.log(e);
  }
}

function refreshUi(filter, currentTab, tabData) {
  // Update UI after search query was changed,
  // or a tab was selected.
  $('.animationElement, #map').hide();
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
    destroyPreviousTable('#results_main_table');
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
          $('#results_main_table  > tbody').on( 'click', 'tr', function () {
              searchBar.row.data = mainDatatable.row( this ).data();
          });

          // console.log(JSON.stringify({ searchData: currentSearchObj, tableParams: d, output: 'resultsTable' }))
          return JSON.stringify({
            searchData: currentSearchObj,
            tableParams: d,
            output: 'resultsTable',

          });
        }
      },

      scrollX: true,
      columnDefs: [
        { width: "10%", targets: 2 },
        { width: "10%", targets: 3 },
        { width: "15%", targets: 62 },
        { width: "5%", targets: 32 },
        { width: "10%", targets: 50 },
        { width: "5%", targets: 33 },
        { width: "5%", targets: 34 },
        { width: "5%", targets: 25 },
        { width: "5%", targets: 25 },
      ],

      // page length Default
      pageLength: 20,

      // dom: 'ifrtBp',
      dom:  "<'flex-container'iB>" +
            "<'row'<'col-sm-12'tr>>" +
            "<'row'<'col-sm-5'><'col-sm-7'p>>",
      lengthMenu: [
        [20, 50, 100],
        ['20 rows', '50 rows', '100 rows']
      ],

      language: {
        info: "Showing _START_ to _END_ of _TOTAL_ entries <i class='fa fa-question-circle' data-toggle='tooltip' data-placement='top' title='Italicized results are calculated by an algorithm.'></i> ",
      },

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
    destroyPreviousTable(tableId);
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
    var cell = getTableElement("cell");
    var rowElement = getTableElement("row");
    var postData = {
      searchData: currentSearchObj,
      output: "pivotTable",
      row_field: getField("row"),
      col_field: getField("column"),
      pivot_functions: cell ? cell.functions : null,
    };
    var isRange = rowElement && rowElement.hasOwnProperty('range');
    if (isRange) {
      postData.range = rowElement.range;
    }
    // Validate post before issuing AJAX call.
    if (postData.row_field && postData.col_field && postData.pivot_functions) {
      $.post(searchUrl, JSON.stringify(postData), function(result) {
        $( "#sv-loader" ).removeClass( "display-none" );

        // Produce a table with data content.
        var table = $('#v-tables');
        destroyPreviousTable('#v-tables');
        var columnHeaderRows = 1 + (result.col_extra_headers ? result.col_extra_headers.length : 0);
        var thead = table.find('thead');
        thead.empty();
        // Top-left row is blank.
        var subCells = $.map(Object.keys(cell.functions), function(key) { return key[0] == '_' ? undefined : key; });
        var totalsHeader = '<th colspan="' + subCells.length + '" rowspan="' + columnHeaderRows + '">' + gettext('Totals') + '</th>';
        var tr = '<tr><th rowspan="' + (columnHeaderRows + (subCells.length > 1 ? 1 : 0)) + '">Year Range</th>';
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
          scrollCollapse: true
        });
      }).done(function(){
        $( "#sv-loader" ).addClass( "display-none" );
      });
    }
  } else if (currentTab == 'timeline') {
    // TODO!
    $('#timelineChart').empty();
    var timelineVariableId = tabs.timeline.chart.value;
    var timelineVariable = tabs.timeline.chart.options[timelineVariableId]["varName"];
    var postData = {
      searchData: currentSearchObj,
      output: 'timeline',
      timelineVariable: timelineVariable,
    };
    if (postData.timelineVariable) {
      loader.loadScript(STATIC_URL + 'scripts/d3.min.js')
        .then(function() {
          $( "#sv-loader" ).removeClass( "display-none" );
          $.post(searchUrl, JSON.stringify(postData), function(result) {
            result = result.data;
            var margin = {top: 20, right: 10, bottom: 40, left: 40},
              width = 960 - margin.left - margin.right,
              height = 400 - margin.top - margin.bottom;
            var minYear = result[0].year;
            var maxYear = result[result.length - 1].year;
            var indexByYear = {};
            for (var i = 0; i < result.length; ++i) {
                indexByYear[result[i].year] = i;
            }
            var x = d3.scale.ordinal()
              .domain(d3.range(minYear, maxYear + 1))
              .rangeRoundBands([0, width]);
            var xShift = -x(minYear);
            var maxValue = d3.max(result, function(d) { return d.value; });
            var y = d3.scale.linear()
                .domain([0, maxValue * 1.1])
                .range([height, 0]);
            var tickSet = [];
            var firstOrdinal = x.domain()[0];
            var lastOrdinal = x.domain()[x.domain().length - 1];
            var modulus = 10;
            if (lastOrdinal > firstOrdinal + 200) {
                modulus = 50;
            } else if (lastOrdinal > firstOrdinal + 100) {
                modulus = 25;
            } else if (lastOrdinal > firstOrdinal + 50) {
                modulus = 10;
            } else if (lastOrdinal > firstOrdinal + 25) {
                modulus = 5;
            } else {
                modulus = 1;
            }
            var t = firstOrdinal;
            if (firstOrdinal % modulus) {
                t += modulus - (firstOrdinal % modulus);
            }
            for (; t <= lastOrdinal; t += modulus) {
                tickSet.push(t);
            }
            var xAxis = d3.svg.axis()
              .scale(x)
              .tickValues(tickSet)
              .tickSize(-height)
              .tickPadding(5)
              .orient("top");

            var yTickFormat = function(d) {
              var formatNumber = d3.format("d");
              if (d >= 2000) {
                return formatNumber(d/1000) + "k";
              }
              return d;
            };
            var yAxis = d3.svg.axis()
              .scale(y)
              .ticks(5)
              .tickFormat(yTickFormat)
              .tickPadding(5)
              .tickSize(-width)
              .orient("left");

            var svg = d3.select("#timelineChart")
              .append("svg")
              .attr("width", width + margin.left + margin.right)
              .attr("height", height + margin.top + margin.bottom)
              .append("g")
              .attr("class", "timeline_main_g")
              .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

            var rect = svg.selectAll("rect")
              .data(result)
              .enter()
              .append("rect")
              .attr("x", function(d) { return x(d.year) + xShift; })
              .attr("y", height)
              .attr("width", x.rangeBand())
              .attr("height", 0);
            rect.transition()
              .attr("y", function(d) { return y(d.value); })
              .attr("height", function(d) { return y(0) - y(d.value); });
            var gx = svg.append("g")
                .attr("class", "x axis")
                //.attr("transform", "translate(0," + height + ")")
                .attr("transform", "translate(" + xShift + ", 0)")
                .call(xAxis);

            var gy = svg.append("g")
                .attr("class", "y axis")
                .call(yAxis);

            var vertical = svg
                .append("g")
                .attr("class", "vertical_highlight")
                .style("opacity", 0.0);

            vertical.append("line")
                .attr("class", "vertical_line")
                .attr("y2", height);

            var mouseover = function(d) {
              $('#mouseOverInfo').html("<strong>" + gettext('Year') + "</strong> " + d.year +
                  "<br /><strong>" + tabs.timeline.chart.value + ":</strong> " + Math.round(d.value).toLocaleString());
            };
            var changeHoveredBar = function(index) {
              var out = index === undefined;
              if (!out) {
                  mouseover(result[index]);
                  vertical.style("opacity", 1.0);
                  vertical.attr("transform", "translate(" + (x.rangeBand() / 2 + x(result[index].year) + xShift) + ",0)");
              }
              if (out && vertical.timeoutfn == null) {
                  vertical.timeoutfn = function() {
                      if (vertical.timeoutfn != null) {
                          vertical.style("opacity", 0.0);
                          vertical.timeoutfn = null;
                      }
                  };
                  setTimeout(vertical.timeoutfn, 3000);
              } else if (!out) {
                  vertical.timeoutfn = null;
              }
            };

            svg.on("mousemove", function() {
              var mouseX = d3.mouse(this)[0] - xShift;
              var year = d3.bisectLeft(x.range(), mouseX) + minYear - 1;
              var index = indexByYear[year];
              changeHoveredBar(index);
            });
          }).done(function(){
            $( "#sv-loader" ).addClass( "display-none" );
          });
        });
    }
  } else if (currentTab == 'visualization') {
    loader.loadScript(STATIC_URL + 'scripts/d3.min.js')
      .then(function() {
        $( "#sv-loader" ).removeClass( "display-none" );

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
          $.post(searchUrl, JSON.stringify(postData), function(series) {
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
              xValues = d3.set(xValues).values().map(function(s) { return parseFloat(s); });

              var margin = {top: 90 + 20 * (seriesNames.length - 2), right: 15, bottom: 110, left: 80},
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
                xAxis = xAxis.tickFormat(function(d, i) { return d.toString(); });
              }
              var yAxis = d3.svg.axis()
                .scale(y)
                .orient("left")
                .tickSize(-width);
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
                .attr("transform", function(d, i) { return "translate(0," + (i * 20 - margin.top + 30) + ")"; });

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
                .text(function(d) { return d; });

              for (var yid in series) {
                var line = d3.svg.line()
                  .x(function(d) { return x(d.x); })
                  .y(function(d) { return y(d.value); });
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

              var wrap = function (text) {
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
              var margin = {top: 90 + 20 * (seriesNames.length - 2), right: 10, bottom: 110, left: 80},
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
                .attr("transform", function(d, i) { return "translate(0," + (i * 20 - margin.top + 30) + ")"; });

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
                .text(function(d) { return d; });

              // Add label groups.
              var gLabels = svg.selectAll(".label")
                .data(labels)
                .enter()
                .append("g")
                .attr("class", "g")
                .attr("transform", function(d) { return "translate(" + x0(d) + ",0)"; });
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
                                res.push({ series: yid, value: items[i].value });
                            }
                        }
                    }
                    return res;
                })
                .enter()
                .append("rect")
                .attr("width", x1.rangeBand())
                .attr("x", function(d) { return x1(d.series); })
                .attr("y", function(d) { return y(d.value); })
                .attr("height", function(d) { return height - y(d.value); })
                .style("fill", function(d) { return color(d.series); });
            } else if (chartType[0] == 'donut') {
              $("#tabs-visualization-donut").empty();
              var label = Object.keys(series)[0];
              var data = series[label];
              data.sort(function(a, b) { return a.value - b.value; });
              var sum = d3.sum(data, function(d) { return d.value; });
              var margin = {top: 20, right: 10, bottom: 50, left: 20},
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
                .value(function(d) { return d.value; });
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

              var key = function(d) { return d.data.x; };
              g.append("path")
                .attr("d", arc)
                .style("fill", function(d) { return color(key(d)); });

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
              text.enter()
                .append("text")
                .style('opacity', opacityFn)
                .attr("dy", ".35em")
                .text(function(d) { return key(d) + " = " + d.value.toLocaleString(); });

              var midAngle = function(d) {
                return d.startAngle + (d.endAngle - d.startAngle)/2;
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
                    return "translate("+ pos +")";
                  };
                })
                .styleTween("text-anchor", function(d){
                  this._current = this._current || d;
                  var interpolate = d3.interpolate(this._current, d);
                  this._current = interpolate(0);
                  return function(t) {
                    var d2 = interpolate(t);
                    return midAngle(d2) < Math.PI ? "start":"end";
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
                .attrTween("points", function(d){
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
          }).done(function(){
            $( "#sv-loader" ).addClass( "display-none" );
          });
		    } else {
          // TODO: Clear existing chart?
        }
      }
    );
  } else if (currentTab == 'maps') {
    // TODO: Map year should be computed based on year range of search.
    // We can do it in the client side (easier).
    // for reference: voyages.apps.assessment.globals.get_map_year
    var postData = {
      searchData: currentSearchObj,
      output: 'mapFlow'
    };
		var mapFlowSearchCallback = function() {
			var $map = $('#map');
			$map.addClass('gray');
      $.post(searchUrl, JSON.stringify(postData), function(result) {
        eval(result);
        voyagesMap.clear();
        $('#loading').hide();
        try {
          voyagesMap.setNetworkFlow(ports, flows);
        } catch(e) {
          console.log(e);
        }
        $map.removeClass('gray');
        loader.resizeMap();
      });
		};
    $('#loading').show();
    loader.loadMap(mapFlowSearchCallback);
  } else if (currentTab == 'animation') {
    var postData = {
      searchData: currentSearchObj,
      output: 'mapAnimation'
    };
		var mapAnimationSearchCallback = function() {
			var $map = $('#map');
			$map.addClass('gray');
      $.post(searchUrl, JSON.stringify(postData), function(result) {
        voyagesMap.clear();
        $map.removeClass('gray');
        $('#loading').hide();
        $('.animationElement').show();
        animationHelper.startAnimation(result);
        $map.removeClass('gray');
        loader.resizeMap();
      });
		};
    $('#loading').show();
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
      self.loadCss(STATIC_URL + 'css/animation.css');
      $.when(
        self.loadScript(STATIC_URL + 'scripts/d3.min.js'),
        self.loadScript(STATIC_URL + 'scripts/voyage/beta/jquery-ui.min.js'),
        self.loadScript(STATIC_URL + 'maps/js/arc.js'),
        self.loadScript(STATIC_URL + 'maps/js/leaflet.geodesic.min.js')
      )
      .then(self.loadScript(STATIC_URL + 'scripts/voyage/beta/animation.js'))
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
