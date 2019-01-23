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
  "Itinerary",
  "Slave",
  "Year range",
  "Dates",
  "Captain and crew",
  "Outcome",
  "Source",
];

var allColumns = [

  // ship nation owner
  { data: "var_voyage_id", category: 0, header: gettext("Voyage ID"), isImputed: false },
  { data: "var_ship_name", category: 0, header: gettext("Vessel name"), isImputed: false },
  { data: "var_owner", category: 0, header: gettext("Vessel owner"), "visible": false, isImputed: false },
  { data: "var_year_of_construction", category: 0, header: gettext("Year constructed"), "visible": false, isImputed: false },
  { data: "var_vessel_construction_place", category: 0, header: gettext("Place constructed"), "visible": false, isImputed: false },
  { data: "var_registered_year", category: 0, header: gettext("Year registered"), "visible": false, isImputed: false },
  { data: "var_registered_place", category: 0, header: gettext("Place registered"), "visible": false, isImputed: false },
  { data: "var_nationality", category: 0, header: gettext("Flag"), "visible": false, isImputed: false },
  { data: "var_imputed_nationality", category: 0, header: gettext("Flag (imputed)"), "visible": false, isImputed: true },
  { data: "var_rig_of_vessel", category: 0, header: gettext("Rig of vessel"), "visible": false, isImputed: false },
  { data: "var_tonnage", category: 0, header: gettext("Tonnage"), "visible": false, isImputed: false },
  { data: "var_tonnage_mod", category: 0, header: gettext("Standardized tonnage"), "visible": false, isImputed: true },
  { data: "var_guns_mounted", category: 0, header: gettext("Guns mounted"), "visible": false, isImputed: false },

  // itinerary
  { data: "var_imp_port_voyage_begin", category: 1, header: gettext("Place where voyage began"), isImputed: true },
  { data: "var_imp_principal_place_of_slave_purchase", category: 1, header: gettext("Principal place of purchase"), isImputed: true },
  { data: "var_first_place_slave_purchase", category: 1, header: gettext("1st place of purchase"), "visible": false, isImputed: false },
  { data: "var_second_place_slave_purchase", category: 1, header: gettext("2nd place of purchase"), "visible": false, isImputed: false },
  { data: "var_third_place_slave_purchase", category: 1, header: gettext("3rd place of purchase"), "visible": false, isImputed: false },
  { data: "var_port_of_call_before_atl_crossing", category: 1, header: gettext("Places of call before Atlantic crossing"), "visible": false, isImputed: false },
  { data: "var_imp_principal_port_slave_dis", category: 1, header: gettext("Principal place of slave landing"), isImputed: true },
  { data: "var_first_landing_place", category: 1, header: gettext("1st place of slave landing"), "visible": false, isImputed: false },
  { data: "var_second_landing_place", category: 1, header: gettext("2nd place of slave landing"), "visible": false, isImputed: false },
  { data: "var_third_landing_place", category: 1, header: gettext("3rd place of slave landing"), "visible": false, isImputed: false },
  { data: "var_place_voyage_ended", category: 1, header: gettext("Place where voyage ended"), "visible": false, isImputed: false },

  // slaves
  { data: "var_imp_total_num_slaves_purchased", category: 2, header: gettext("Total embarked"), "visible": false, isImputed: true },
  { data: "var_total_num_slaves_purchased", category: 2, header: gettext("Total embarked"), "visible": false, isImputed: false },
  { data: "var_imp_total_slaves_disembarked", category: 2, header: gettext("Total disembarked"), "visible": false, isImputed: true },
  { data: "var_num_slaves_intended_first_port", category: 2, header: gettext("Slaves intended"), "visible": false, isImputed: false },
  { data: "var_num_slaves_carried_first_port", category: 2, header: gettext("Slaves from 1st port"), "visible": false, isImputed: false },
  { data: "var_num_slaves_carried_second_port", category: 2, header: gettext("Slaves from 2nd port"), "visible": false, isImputed: false },
  { data: "var_num_slaves_carried_third_port", category: 2, header: gettext("Slaves from 3rd port"), "visible": false, isImputed: false },
  { data: "var_total_num_slaves_arr_first_port_embark", category: 2, header: gettext("Slaves arrived 1st port"), isImputed: false },
  { data: "var_num_slaves_disembark_first_place", category: 2, header: gettext("Slaves landed 1st port"), "visible": false, isImputed: false },
  { data: "var_num_slaves_disembark_second_place", category: 2, header: gettext("Slaves landed 2nd port"), "visible": false, isImputed: false },
  { data: "var_num_slaves_disembark_third_place", category: 2, header: gettext("Slaves landed 3rd port"), "visible": false, isImputed: false },
  { data: "var_imputed_percentage_men", category: 2, header: gettext("Percent men"), "visible": false, isImputed: false },
  { data: "var_imputed_percentage_women", category: 2, header: gettext("Percent women"), "visible": false, isImputed: false },
  { data: "var_imputed_percentage_boys", category: 2, header: gettext("Percent boys"), "visible": false, isImputed: false },
  { data: "var_imputed_percentage_girls", category: 2, header: gettext("Percent girls"), "visible": false, isImputed: false },
  { data: "var_imputed_percentage_male", category: 2, header: gettext("Percent males"), "visible": false, isImputed: false },
  { data: "var_imputed_percentage_child", category: 2, header: gettext("Percent children"), "visible": false, isImputed: false },
  { data: "var_imputed_sterling_cash", category: 2, header: gettext("Sterling cash price in Jamaica"), "visible": false, isImputed: false },
  { data: "var_imputed_death_middle_passage", category: 2, header: gettext("Captives died during middle passage"), "visible": false, isImputed: false },
  { data: "var_imputed_mortality", category: 2, header: gettext("Mortality rate"), "visible": false, isImputed: false },

  // year range
  {
    data: "var_" + YEAR_RANGE_VARNAME,
    category: 3,
    header: gettext("Year"),
    isImputed: true,
  },

  // dates
  { data: "var_length_middle_passage_days", category: 4, header: gettext("Middle passage (days)"), "visible": false, isImputed: false },
  { data: "var_imp_length_home_to_disembark", category: 4, header: gettext("Voyage length, homeport to landing (days)"), "visible": false, isImputed: false },
  { data: "var_voyage_began", category: 4, header: gettext("Year disembarked"), "visible": false, isImputed: true },
  { data: "var_slave_purchase_began", category: 4, header: gettext("Date trade began in Africa"), "visible": false, isImputed: false },
  { data: "var_date_departed_africa", category: 4, header: gettext("Date vessel departed Africa"), "visible": false, isImputed: false },
  { data: "var_first_dis_of_slaves", category: 4, header: gettext("Date vessel arrived with slaves"), "visible": false, isImputed: false },
  { data: "var_departure_last_place_of_landing", category: 4, header: gettext("Date vessel departed for homeport"), "visible": false, isImputed: false },
  { data: "var_voyage_completed", category: 4, header: gettext("Date voyage completed"), "visible": false, isImputed: false },

  // captain and crew
  { data: "var_captain", category: 5, header: gettext("Captain's name"), isImputed: false },
  { data: "var_crew_voyage_outset", category: 5, header: gettext("Crew at voyage outset"), "visible": false, isImputed: false },
  { data: "var_crew_first_landing", category: 5, header: gettext("Crew at first landing of slaves"), "visible": false, isImputed: false },
  { data: "var_crew_died_complete_voyage", category: 5, header: gettext("Crew deaths during voyage"), "visible": false, isImputed: false },

  // outcome
  { data: "var_outcome_voyage_lang", category: 6, header: gettext("Particular outcome of voyage"), "visible": false, isImputed: false },
  { data: "var_outcome_slaves", category: 6, header: gettext("Outcome of voyage for slaves"), "visible": false, isImputed: false },
  { data: "var_outcome_ship_captured", category: 6, header: gettext("Outcome of voyage if ship captured"), "visible": false, isImputed: false },
  { data: "var_outcome_owner", category: 6, header: gettext("Outcome of voyage for owner"), "visible": false, isImputed: false },
  { data: "var_resistance", category: 6, header: gettext("African resistance"), "visible": false, isImputed: false },

  // sources
  {
    data: "var_sources",
    category: 7,
    header: gettext("Sources"),
    "visible": false,
    render: function ( data ) {
      var sourceString = "";
      var count = 0;
      if (data !== null) {
        data.forEach(function(source) {
          count += 1;
          var elements = source.split("<>");
          // var postfix = data.length == count ? "" : ";";
          var postfix = "";
          sourceString += "<span data-toggle='tooltip' data-placement='top' data-html='true' title='" + elements[1] + "'>" + elements[0] + postfix + " </span><br/>";
        });
      }
      return sourceString;
    },
    isImputed: false,
  },
];


var categories = $.map(categoryNames, function(name) {
  return {
    name: name,
    columns: []
  };
});

allColumns.forEach(function(c, index) {

  var title = c.isImputed ? "<span class='imputed-result'>" + c.header + "</span> <span class='badge badge-pill badge-secondary' data-toggle='tooltip' data-placement='top' title='Imputed results are calculated by an algorithm.'> IMP </span>" : c.header;

  categories[c.category].columns.push({
    extend: 'columnToggle',
    text: title,
    columns: index,
  });

  // add render function to customize the display of imputed variables
  if (c.isImputed) {
    c.title = "<span class='imputed-result'>" + c.header + "</span>" + ' <span class="badge badge-pill badge-secondary" data-toggle="tooltip" data-placement="top" title="Imputed results are calculated by an algorithm."> IMP </span>'; // italicized column title
    c.render = function(data) {
      var formatedString = "";
      if (data !== null) {
        formattedString = "<span class='imputed-result'>" + data + "</span>";
      } else {
        formattedString = data
      }
      return formattedString;
    };
  }
});

var defaultBtns = $.map(categories, function (category) {
  return category.columns.length == 1 && category.columns[0].text === category.name ?
    category.columns[0] :
    {
      extend: 'collection',
      text: category.name,
      buttons: category.columns
    };
});

var restoreBtn = {
  extend: 'colvis',
  buttons: 'colvisRestore',
  text: "Restore visibility",
};

defaultBtns.push(restoreBtn);

var columnToggleMenu = {
  extend: 'collection',
  text: 'Configure columns',
  titleAttr: 'Configure visible columns',
  className: 'btn btn-info buttons-collection dropdown-toggle',
  buttons: defaultBtns,
};

var pageLength = {
  extend: 'pageLength',
  className: 'btn btn-info buttons-collection dropdown-toggle',
};
