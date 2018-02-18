
var searchTerms = [
	RangeSearchTerm(new VariableInfo('voyage_id', 'ship_nation_owners', 'Voyage ID'), '', null, 'Voyage id help text'),
	TextSearchTerm(new VariableInfo('intra_american_voyage', 'ship_nation_owners', 'Is I-Am voyage?'), 'equals', null, 'Type true or false.', minLengthValidator(4)),
	TextSearchTerm(new VariableInfo('ship_name', 'ship_nation_owners', 'Vessel Name'), 'contains', null, 'Please type one or more words (or even partial words) that should appear in the name of the vessel. The search is case insensitive.', minLengthValidator(3)),
	TextSearchTerm(new VariableInfo('owner', 'ship_nation_owners', 'Vessel Owners'), 'contains', null, 'Look for names of slave vessel owners.', minLengthValidator(3)),
	PlaceSearchTerm(new VariableInfo('imp_port_voyage_begin_idnum', 'itinerary', 'Place voyage began*'), 'is one of', null, 'Select the places where voyages began.', null),
	PlaceSearchTerm(new VariableInfo('imp_principal_place_of_slave_purchase_idnum', 'itinerary', 'Principal place of slave purchase*'), 'is one of', null, 'help text.', null),
	PlaceSearchTerm(new VariableInfo('imp_principal_port_slave_dis_idnum', 'itinerary', 'Principal place of slave landing*'), 'is one of', null, 'help text.', null),
	PlaceSearchTerm(new VariableInfo('place_voyage_ended_idnum', 'itinerary', 'Place voyage ended'), 'is one of', null, 'Select the places where voyages ended.', null),
	RangeSearchTerm(new VariableInfo(YEAR_RANGE_VARNAME, 'dates', 'Year arrived with slaves*'), '', null, 'The imputed year in which the ship arrived with slaves at the first? port of disembarkation', dateRangeValidation),
	TextSearchTerm(new VariableInfo('captain', 'captain_crew', 'Captain\'s Name'), 'contains', null, 'Look for names of slave vessel captains.', minLengthValidator(3)),
	RangeSearchTerm(new VariableInfo('imp_total_num_slaves_purchased', 'numbers', 'Total slaves embarked*'), '', null, 'total_slaves_embarked help text', null, 3),
	RangeSearchTerm(new VariableInfo('imp_total_slaves_disembarked', 'numbers', 'Total slaves disembarked*'), '', null, 'total_slaves_disembarked help text', null, 3),
	RangeSearchTerm(new VariableInfo('year_range', 'numbers', 'Year range of your search'), '', null, 'year_range help text', null, 3),
	TextSearchTerm(new VariableInfo('sources_plaintext_search', 'source', 'Source'), 'contains', null, 'Please type one or more words (or even partial words) that should appear in the source references for the voyage. The search is case insensitive.', minLengthValidator(3)),
];

var searchTermsDict = {};
for (var i = 0; i < searchTerms.length; ++i) {
	var item = searchTerms[i];
	searchTermsDict[item.varName] = item;
}

var categoryNames = [
				"Ship, nation, owners",
				"Voyage Dates",
				"Voyage Itinerary",
				"Slave (numbers)",
				"Voyage Outcome",
				"Sources",
			];
			var allColumns = [
				{ data: "var_voyage_id", category: 0, header: "Voyage identification number" },
				{ data: "var_ship_name", category: 0, header: "Vessel name" },
				{ data: "var_captain_plaintext", category: 0, header: "Capitain's name" },
				{ data: "var_" + YEAR_RANGE_VARNAME, category: 1, header: "Year arrived with slaves*" },
				{ data: "var_imp_principal_place_of_slave_purchase_lang_en", category: 2, header: "Principal region of slave purchase*" },
				{ data: "var_imp_principal_port_slave_dis_lang_en", category: 2, header: "Principal region of slave landing*" },
				{ data: "var_imp_port_voyage_begin_lang_en", category: 2, header: "Place where voyage began*", "visible": false },
				{ data: "var_imp_total_num_slaves_purchased", category: 3, header: "Total slaves embarked*", "visible": false },
				{ data: "var_outcome_ship_captured_lang_en", category: 4, header: "Outcome of voyage if ship captured*", "visible": false },
				{ data: "var_sources_plaintext", category: 5, header: "Sources", "visible": false },
			];
			var categories = $.map(categoryNames, function(name) {
				return { name: name, columns: [] };
			});
			allColumns.forEach(function(c, index) {
				categories[c.category].columns.push({
					extend: 'columnToggle',
					text: c.header,
					columns: index,
				});
			});

var columnToggleMenu = {
				extend: 'collection',
				text: 'Columns',
				titleAttr: 'Configure visible columns',
				className: 'btn btn-info buttons-collection dropdown-toggle',
				buttons: $.map(categories, function(category) {
					return category.columns.length == 1 && category.columns[0].text === category.name
						? category.columns[0]
						: {
								extend: 'collection',
								text: category.name,
								buttons: category.columns
							};
				})
			};

var pageLength = {
	extend: 'pageLength',
	className: 'btn btn-info buttons-collection dropdown-toggle',
};

function search(query) {
	var query = query;

	var activeSearchTerms = jQuery.map(query, function(val, id) {
		if (val.hasChanged) {
			var term = searchTermsDict[val.varName];
			// Here we allow custom search types to generate their backend terms.
			var backendSearchTerm = term.hasOwnProperty('getBackendSearchTerm')
				? term.getBackendSearchTerm()
				: term.getSearchTerm();

			// return { varName: term.varName, op: term.operatorLabel, searchTerm: backendSearchTerm };
			return { varName: term.varName, op: val.current.op , searchTerm: val.current.searchTerm };
		}
	});

	// var activeSearchTerms = function(query) {
	// 	var term = searchTermsDict[id];
	// 	// Here we allow custom search types to generate their backend terms.
	// 	var backendSearchTerm = term.hasOwnProperty('getBackendSearchTerm')
	// 		? term.getBackendSearchTerm()
	// 		: term.getSearchTerm();
	// 	return { varName: term.varName, op: term.operatorLabel, searchTerm: backendSearchTerm };
	// }

	var currentSearchObj = {items: activeSearchTerms, orderBy: []};
	// Store current search on session storage.
	var searchState = {
		currentSearchObj: currentSearchObj,
		searchTerms: jQuery.map(["voyage_id"], function(id) { return searchTermsDict[id].serialize(); }),
		yearRange: "1514 - 1866"
	};
	var serializedSearch = JSON.stringify(searchState);
	sessionStorage.setItem('searchState', serializedSearch);
	// Check if this is a new search
	var d = new Date();
	var isRepeat = false;
	var searchHistory = [];
	searchHistory.some(function(h) {
		isRepeat = h.search == serializedSearch;
		if (isRepeat) {
			h.date = d;
		}
		return isRepeat;
	});
	if (!isRepeat) {
		var label = ["voyage_id"];
		searchHistory.push({ label: label == '' ? '*' : label, search: serializedSearch, date: d });
	}
	sessionStorage.setItem('searchHistory', JSON.stringify(searchHistory));

	if ( $.fn.DataTable.isDataTable('#results_main_table') ) {
	  $('#results_main_table').DataTable().destroy();
	}

	var mainDatatable = $('#results_main_table').DataTable({
        ajax: {
					url: "876167cf-bc40-44f7-9557-ee8117d94008/beta_ajax_search",
					type: 'POST',
					data: function(d) {
						if (d.order) {
							currentSearchObj.orderBy = $.map(d.order, function(item) {
								var columnIndex = mainDatatable
									? mainDatatable.colReorder.order()[item.column]
									: item.column;
								return {name: allColumns[columnIndex].data.substring(4), direction: item.dir};
							});
						}
						// console.log(JSON.stringify({ searchData: currentSearchObj, tableParams: d, output: 'resultsTable' }))
						return JSON.stringify({ searchData: currentSearchObj, tableParams: d, output: 'resultsTable' });
					}
				},
				dom: 'ifrtBp',
				lengthMenu: [
            [ 10, 25, 50, 100 ],
            [ '10 rows', '25 rows', '50 rows', '100 rows' ]
        ],

				buttons: [
					pageLength,
					columnToggleMenu,
					{
						extend: 'collection',
						// text: '<span class="fa fa-columns" style="vertical-align: middle;"></span>',
						className: 'btn btn-info buttons-collection dropdown-toggle',
						text: 'Download',
						titleAttr: 'Download results',
						buttons: [
							// {
							// 	text: 'CSV - not implemented',
							// 	action: function() { alert('not implemented yet'); },
							// },
							{
								text: 'Excel',
								action: function() {
									var visibleColumns = $.map($.makeArray(mainDatatable.columns().visible()), function(visible, index) {
										return visible ? allColumns[index].data : undefined;
									});
									var form = $("<form action='876167cf-bc40-44f7-9557-ee8117d94008/beta_ajax_download' method='post'>{% csrf_token %}</form>");
									form.append($("<input name='data' type='hidden'></input>").attr('value', JSON.stringify({ searchData: currentSearchObj, cols: visibleColumns })));
									form.appendTo('body').submit().remove();
								},
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
				colReorder: true,
    	});

	// console.log(activeSearchTerms);

	// var $yearRange = $("#year_range");
  //
	// // Check if the user explicitly specified the year search.
	// var hasYearSearch = activeSearchTerms.some(function(t) {
	// 	var match = t.varName == YEAR_RANGE_VARNAME;
	// 	if (match) {
	// 		var range = t.searchTerm;
	// 		range = [range[0], range[1] || range[0]];
	// 		$yearRange.val(range[0] + ' - ' + range[1]);
	// 		$yearRange.change();
	// 	}
	// 	return match;
	// });
  //
	// if (!hasYearSearch) {
	// 	// Add year range to search.
	// 	var yearRange = $yearRange.val().split('-');
	// 	if (yearRange.length == 2) {
	// 		var first = parseInt(yearRange[0]);
	// 		var last = parseInt(yearRange[1]);
	// 		if (!isNaN(first) && !isNaN(last)) {
	// 			activeSearchTerms.push({varName: YEAR_RANGE_VARNAME, op: 'is between', searchTerm: [first, last]});
	// 		}
	// 	}
	// }
  //
	// currentSearchObj = {items: activeSearchTerms, orderBy: []};
	// // Store current search on session storage.
	// var searchState = {
	// 	currentSearchObj: currentSearchObj,
	// 	searchTerms: jQuery.map($('#current_search').val(), function(id) { return searchTermsDict[id].serialize(); }),
	// 	yearRange: $("#year_range").val()
	// };
  //
	// var serializedSearch = JSON.stringify(searchState);
  //
	// sessionStorage.setItem('searchState', serializedSearch);
	// // Check if this is a new search
	// var d = new Date();
	// var isRepeat = false;
	// searchHistory.some(function(h) {
	// 	isRepeat = h.search == serializedSearch;
	// 	if (isRepeat) {
	// 		h.date = d;
	// 	}
	// 	return isRepeat;
	// });
	// if (!isRepeat) {
	// 	var label = $('#current_search').val();
	// 	searchHistory.push({ label: label == '' ? '*' : label, search: serializedSearch, date: d });
	// }
	// sessionStorage.setItem('searchHistory', JSON.stringify(searchHistory));
	// updateHistory();
	// searchCallback();
}

// helpers

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

function activateFilter(filter, group, filterValues) {
	for (key1 in filter[group]) {
		if (key1 !== "count") {
			for (key2 in filter[group][key1]) {
				if (key2 !== "count") {
					if (filter[group][key1][key2].changed) {
						// filter[group][key1][key2].value["searchTerm0"] = filterValues[group][key1][key2].value["searchTerm0"];
						// filter[group][key1][key2].value["searchTerm1"] = filterValues[group][key1][key2].value["searchTerm1"];
						// filter[group][key1][key2].value["op"] = filterValues[group][key1][key2].value["op"];
						filter[group][key1][key2].changed = true;
						filter[group][key1][key2].activated = true;
					}
				}
			}
		}
	}
}

function resetFilter(filter, group) {
	for (key1 in filter[group]) {
		if (key1 !== "count") {
			for (key2 in filter[group][key1]) {
				if (key2 !== "count") {
					filter[group][key1][key2].value["searchTerm0"] = null;
					filter[group][key1][key2].value["searchTerm1"] = null;
					filter[group][key1][key2].value["op"] = "equals to";
					filter[group][key1][key2].changed = false;
					filter[group][key1][key2].activated = false;
				}
			}
		}
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
								item["op"] = filter[key1][key2][key3].value["op"];
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
	return items;
}

function resetAll() {

}
// helpers

// main app
var searchBar = new Vue({
	el: "#search-bar",
	delimiters: ['{{', '}}'],
	data: {
		isAdvanced: true,
		searchFilter: {

			groups: {
				slave: {
					overallNumbers: {
						var_imp_total_num_slaves_purchased: {
							varName: 'var_imp_total_num_slaves_purchased',
							value: {
								op: "is between",
								searchTerm0: null,
								searchTerm1: null,
							},
							changed: false,
							activated: false,
						},

						var_total_num_slaves_purchased: {
							varName: 'var_total_num_slaves_purchased',
							value: {
								op: "is between",
								searchTerm0: null,
								searchTerm1: null,
							},
							changed: false,
							activated: false,
						},

						var_imp_total_slaves_disembarked: {
							varName: 'var_imp_total_slaves_disembarked',
							value: {
								op: "is between",
								searchTerm0: null,
								searchTerm1: null,
							},
							changed: false,
							activated: false,
						},

						count: {
							changed: 0,
							activated: 0,
						}
					},

					// purchaseNumbers: {
					// 	var_num_slaves_intended_first_port: {
					// 		value: {
					// 			op: "is between",
					// 			searchTerm0: null,
					// 			searchTerm1: null,
					// 		},
					// 		activated: false,
					// 	},
					// 	var_num_slaves_carried_first_port: {
					// 		value: {
					// 			op: "is between",
					// 			searchTerm0: null,
					// 			searchTerm1: null,
					// 		},
					// 		activated: false,
					// 	},
					// 	var_num_slaves_carried_second_port: {
					//
					// 	},
					// 	var_num_slaves_carried_third_port: {
					//
					// 	},
					// 	count: 0
					// },
					landingNumbers: {
						count: {
							changed: 0,
							activated: 0,
						}
					},
					percentageBySexAndAgeGroup: {
						count: {
							changed: 0,
							activated: 0,
						}
					},
					otherCharacteristics: {
						count: {
							changed: 0,
							activated: 0,
						}
					},

					count: {
						changed: 0,
						activated: 0,
					},
				}
			},

			yearRange: {
				default: {
					op: "is between",
					searchTerm: [1514, 1866],
				},
				current: {
					op: "is between",
					searchTerm: [1514, 1866],
				},
				value: {
					op: "is between",
					searchTerm: [1514, 1866],
				},
				varName: "imp_arrival_at_port_of_dis",
				hasChanged: true,
				count: 0,
			},

			outcome1: outcome1,
			outcome2: outcome2,
			outcome3: outcome3,
			outcome4: outcome4,
			outcome5: outcome5,
		},
		searchQuery: {
			// put the search query in here
		},
	},
	computed: {
	},
	watch: {
		isAdvanced: function(val){
			$menu.menuAim({
					activate: activateSubmenu,
					deactivate: deactivateSubmenu
			});
		},

		searchFilter: {
			handler: function(val){
				// slave overallNumbers count
				this.searchFilter.groups.slave.overallNumbers.count.activated = countActivated(this.searchFilter.groups.slave.overallNumbers);
				this.searchFilter.groups.slave.overallNumbers.count.changed = countChanged(this.searchFilter.groups.slave.overallNumbers);

				// slave count
				this.searchFilter.groups.slave.count.activated = countMenuActivated(this.searchFilter.groups.slave);
				this.searchFilter.groups.slave.count.changed = countMenuChanged(this.searchFilter.groups.slave);

			},
			deep: true,
		},
	},

	methods: {
		changed() {
      debugger;
    },
		apply(group, filterValues) {
			activateFilter(this.searchFilter.groups, group, filterValues);
			var searchTerms = searchAll(this.searchFilter.groups);
			alert(JSON.stringify(this.searchFilter.groups));
			alert(JSON.stringify(searchTerms));
		},
		reset(group) {
			resetFilter(this.searchFilter.groups, group);
		},
		itemChanged(variable, changed) {
			// function to locate a variable
			for (key1 in this.searchFilter.groups) {
				for (key2 in this.searchFilter.groups[key1]) {
					if (key2 !== "count") {
						for (key3 in this.searchFilter.groups[key1][key2]) {
							if (key3 == variable.varName) {
								console.log(key3);
								console.log(this.searchFilter.groups[key1][key2][key3]);
								this.searchFilter.groups[key1][key2][key3].changed = changed;
								this.searchFilter.groups[key1][key2][key3].value["searchTerm0"] = variable["searchTerm0"];
								this.searchFilter.groups[key1][key2][key3].value["searchTerm1"] = variable["searchTerm1"];
								this.searchFilter.groups[key1][key2][key3].value["op"] = variable["op"];
							}
						}
					}
				}
			}
			// function to locate a variable

		},


		startTour() {
			// Instance the tour
			$(function () {
			    $('[data-toggle="popover"]').popover()
			});

			var tour = new Tour({
				steps: [
				// {
				//   element: ".trans-search-bar",
				//   title: "Search Filter",
				//   content: "This is where you can set up your search filter."
				// },
				{
					element: "#show-query",
					title: "Show Query",
					content: "You can view your current query here."
				},
				{
					element: "#configure-query",
					title: "Configure Query",
					content: "You can choose to show or hide advanced filters."
				},
				{
					element: "#heart-query",
					title: "Save/Load Query",
					content: "You can a particular query and/or load a particular query."
				}
			]});

			// Initialize the tour
			tour.init();

			// Start the tour
			tour.start();
		}
	},

	mounted: function() {
		search(this.searchFilter);
	}

})
