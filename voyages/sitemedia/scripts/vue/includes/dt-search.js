
  var SEARCH_MIN_YEAR = 1514;
  var SEARCH_MAX_YEAR = 1866;
  var YEAR_RANGE_VARNAME = 'imp_arrival_at_port_of_dis';
  var selectize = null;
  var minLengthValidator = function(minLength) {
      var error = 'The entry must have at least ' + minLength + ' characters';
      return function(s) {
        return s.length >= minLength ? [] : [error];
      }
    };
  var dateRangeValidation = function(arr) {
    var errors = [];
    for (var i = 0; errors.length == 0 && i < 2; ++i) {
      var value = parseInt(arr[i]);
      if (isNaN(value)) continue;
      if (value < SEARCH_MIN_YEAR) {
        errors.push('Year is below minimum value: ' + SEARCH_MIN_YEAR);
      }
      if (value > SEARCH_MAX_YEAR) {
        errors.push('Year is above maximum value: ' + SEARCH_MAX_YEAR);
      }
    }
    return errors;
  };
  var searchTerms = [
    RangeSearchTerm(new VariableInfo('voyage_id', 'ship_nation_owners', 'Voyage ID'), '', null, 'Voyage id help text'),
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

  var mainDatatable = null;
  var currentSearchObj = {items: []};
  var resultsTableSearchCallback = function() {
    // Reload datatables.
    if (mainDatatable) {
      mainDatatable.ajax.reload();
    }
  }
  var searchCallback = resultsTableSearchCallback;

  var allColumns = [
    { "data": "var_voyage_id" },
    { "data": "var_ship_name" },
    { "data": "var_captain" },
    { "data": "var_" + YEAR_RANGE_VARNAME },
    { "data": "var_imp_principal_place_of_slave_purchase_lang_en" },
    { "data": "var_imp_principal_port_slave_dis_lang_en" },
    { "data": "var_sources_plaintext" }
  ];

  // var ajax = this.get('ajax');
  // var ajaxResult = ajax.request('/voyage/api/beta_ajax_search', {
  //   method: 'POST',
  //   data: function(d) {
  //     if (d.order) {
  //       currentSearchObj.orderBy = $.map(d.order, function(item) {
  //         var columnIndex = mainDatatable
  //           ? mainDatatable.colReorder.order()[item.column]
  //           : item.column;
  //         return {name: allColumns[columnIndex].data.substring(4), direction: item.dir};
  //       });
  //     }
  //     return JSON.stringify({ searchData: currentSearchObj, tableParams: d, output: 'resultsTable' });
  //   }
  // })
