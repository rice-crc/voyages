
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
				text: '<span class="glyphicon glyphicon-cog"></span> <span class="caret"></span>',
				titleAttr: 'Configure visible columns',
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

function search(query) {
	var query = query;
	var activeSearchTerms = function(query) {
		var term = searchTermsDict[id];
		// Here we allow custom search types to generate their backend terms.
		var backendSearchTerm = term.hasOwnProperty('getBackendSearchTerm')
			? term.getBackendSearchTerm()
			: term.getSearchTerm();
		return { varName: term.varName, op: term.operatorLabel, searchTerm: backendSearchTerm };
	}

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
						// debugger;
						// return JSON.stringify({ searchData: currentSearchObj, tableParams: d, output: 'resultsTable' });
						return `{"searchData":{"items":[{"varName":"voyage_id","op":"equals","searchTerm":[1232,null]},{"varName":"imp_arrival_at_port_of_dis","op":"is between","searchTerm":[1514,1866]}],"orderBy":[{"name":"voyage_id","direction":"asc"}]},"tableParams":{"draw":2,"columns":[{"data":"var_voyage_id","name":"","searchable":true,"orderable":true,"search":{"value":"","regex":false}},{"data":"var_ship_name","name":"","searchable":true,"orderable":true,"search":{"value":"","regex":false}},{"data":"var_captain_plaintext","name":"","searchable":true,"orderable":true,"search":{"value":"","regex":false}},{"data":"var_imp_arrival_at_port_of_dis","name":"","searchable":true,"orderable":true,"search":{"value":"","regex":false}},{"data":"var_imp_principal_place_of_slave_purchase_lang_en","name":"","searchable":true,"orderable":true,"search":{"value":"","regex":false}},{"data":"var_imp_principal_port_slave_dis_lang_en","name":"","searchable":true,"orderable":true,"search":{"value":"","regex":false}},{"data":"var_imp_port_voyage_begin_lang_en","name":"","searchable":true,"orderable":true,"search":{"value":"","regex":false}},{"data":"var_imp_total_num_slaves_purchased","name":"","searchable":true,"orderable":true,"search":{"value":"","regex":false}},{"data":"var_outcome_ship_captured_lang_en","name":"","searchable":true,"orderable":true,"search":{"value":"","regex":false}},{"data":"var_sources_plaintext","name":"","searchable":true,"orderable":true,"search":{"value":"","regex":false}}],"order":[{"column":0,"dir":"asc"}],"start":0,"length":10,"search":{"value":"","regex":false}},"output":"resultsTable"}`
					}
				},
				dom: 'Bfrtip',
				lengthMenu: [
            [ 10, 25, 50, 100 ],
            [ '10 rows', '25 rows', '50 rows', '100 rows' ]
        ],
				buttons: [
					'pageLength',
					columnToggleMenu,
					{
						extend: 'collection',
						text: '<span class="glyphicon glyphicon-cloud-download"></span>',
						titleAttr: 'Download results',
						buttons: [
							{
								text: 'CSV - not implemented',
								action: function() { alert('not implemented yet'); },
							},
							{
								text: 'Excel - this one works!',
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

// value component
Vue.component("form-value-component", {
	props: ["tagId", "formLabel", "value"],
	template: `
	<div class="form-group">
		<label :for="tagId">{{formLabel}}</label>
		<input type="number" :id="tagId" v-bind:value="value" @input="updateValue($event.target.value)" class="form-control" >
	</div>`,
	methods: {
		updateValue: function (value) {
      this.$emit('input', value)
    }
	}
});

// select2 multiple component
Vue.component("form-select2-multiple", {
	props: {
		tagId: String,
		tagName: String,
		data: Array
	},
	template: `<select :id="tagId" :name="tagName" multiple="multiple"></select>`,
	mounted: function() {
    $(this.$el).select2({
			 width: '100%',
			 data: this.data
		});
  }
});

Vue.component("form-checkbox", {
	props: {
		checked: Boolean,
		formLabel: String,
		tagId: String
	},

	template: `
		<div class="form-check">
			<label class="form-check-label">
				<input class="form-check-input" :tag-id="tagId" type="checkbox" :checked="checked" @change="$emit('input', $event.target.checked)">
				{{formLabel}} ha {{checked}}
			</label>
		</div>`,

	mounted: function(){

	},
	methods: {
		updateValue: function (value) {
      this.$emit('input', value)
    }
	}
});




		// main app
		var searchBar = new Vue({
			el: "#search-bar",
			delimiters: ['{{', '}}'],
			data: {
				text: "text",
				isAdvanced: true,
				searchFilter: {
					yearRange: {
						default: {
							op: "",
							searchTerm: ["1514", "1866"],
							varName: "year_range",
						},
						current: {
							op: "",
							searchTerm: ["1514", "1866"],
							varName: "year_range",
						},
						value: {
							op: "",
							searchTerm: ["1514", "1866"],
							varName: "year_range",
						},
						hasChanged: false,
					},
					vin: {
						default: {
							op: "equals",
							searchTerm: [null, null],
							varName: "voyage_id",
						},
						current: {
							op: "equals",
							searchTerm: [null, null],
							varName: "voyage_id",
						},
						hasChanged: false,
					},
					vesselName: {
						default: "",
						current: "",
						hasChanged: false,
					},
					vesselOwner: {
						default: "",
						current: "",
						hasChanged: false,
					},
					vessel: {
						hasChanged: false,
					},
					flag: {
						default: "",
						current: "",
						data: flagData,
						hasChanged: false,
					},
					flagImputed: {
						default: "",
						current: "",
						data: flagImputedData,
						hasChanged: false,
					},
					rig: {
						default: "",
						current: "",
						data: rigData,
						hasChanged: false,
					},
					cdrom: {
						default: false,
						current: false,
						hasChanged: false,
					},
					tonnage: {
						default: "",
						current: "",
						hasChanged: false,
					},
					standardizedTonnage: {
						default: "",
						current: "",
						hasChanged: false,
					},
					guns: {
						default: "",
						current: "",
						hasChanged: false,
					},
					yearRegistration: {
						default: "",
						current: "",
						hasChanged: false,
					},
					yearConstruction: {
						default: "",
						current: "",
						hasChanged: false,
					}
				},
				searchQuery: {
					vin: {
						value: null
					},
					vesselName: {
						value: null
					},
					vesselOwner: {
						value: null
					},
					flag: {
						value: null
					},
					flagImputed: {
						value: null
					}
				}
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
							// voyage yearRange
							val.yearRange.hasChanged = val.yearRange.current.searchTerm !== val.yearRange.default.searchTerm

							// voyage identification number
							val.vin.hasChanged = val.vin.default !== val.vin.current

							// vessel name
							val.vesselName.hasChanged = val.vesselName.default !== val.vesselName.current

							// vessel owner
							val.vesselOwner.hasChanged = val.vesselOwner.default !== val.vesselOwner.current

							// vessel
							val.vessel.hasChanged = val.vesselName.hasChanged || val.vesselOwner.hasChanged

							// flag
							val.flag.hasChanged = val.flag.default !== val.flag.current

							// flagImputed
							val.flagImputed.hasChanged = val.flagImputed.default !== val.flagImputed.current

							// execute search

						},
						deep: true,
				},
			},

			methods: {
				yearRangeApply: function(val){
					this.searchQuery.yearRange.value = this.searchFilter.yearRange.current;
					search(val.searchFilter);
				},
				yearRangeReset: function(val){
					this.searchFilter.yearRange.current = jQuery.extend(true, {}, this.searchFilter.yearRange.default);
					this.searchFilter.yearRange.value = jQuery.extend(true, {}, this.searchFilter.yearRange.default);
				},

				vinApply: function(val){
					this.searchQuery.vin.value = this.searchFilter.vin.current;
					search(val.searchFilter);
				},
				vinReset: function(val){
					this.searchFilter.vin.current = jQuery.extend(true, {}, this.searchFilter.vin.default);
					this.searchQuery.vin.value = jQuery.extend(true, {}, this.searchFilter.vin.default);
				},
				vesselApply: function(val){
					this.searchQuery.vesselName.value = this.searchFilter.vesselName.current;
					this.searchQuery.vesselOwner.value = this.searchFilter.vesselOwner.current;
				},
				vesselReset: function(val){
					this.searchFilter.vesselName.current = this.searchFilter.vesselName.default;
					this.searchFilter.vesselOwner.current = this.searchFilter.vesselOwner.default;
					this.searchQuery.vesselName.value = this.searchFilter.vesselName.default;
					this.searchQuery.vesselOwner.value = this.searchFilter.vesselOwner.default;
				}
			}

		})
