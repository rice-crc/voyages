var categoryNames = [
  gettext("Year range"),
  gettext("Ship, nation, owners"),
  gettext("Itinerary"),
  gettext("Slave"),
  gettext("Dates"),
  gettext("Captain and crew"),
  gettext("Outcome"),
  gettext("Source"),
];

var allColumns = [

  // year range
  {
    data: "var_imp_arrival_at_port_of_dis",
    category: 0,
    header: gettext("Year arrived with slaves"),
    isImputed: true,
  },

  // ship nation owner
  { data: "var_voyage_id", category: 1, header: gettext("Voyage ID"), isImputed: false },
  { data: "var_ship_name", category: 1, header: gettext("Vessel name"), isImputed: false },
  { data: "var_owner", category: 1, header: gettext("Vessel owner"), visible: false, isImputed: false },
  { data: "var_year_of_construction", category: 1, header: gettext("Year constructed"), visible: false, isImputed: false },
  { data: "var_vessel_construction_place_lang", category: 1, header: gettext("Place constructed"), visible: false, isImputed: false },
  { data: "var_registered_year", category: 1, header: gettext("Year registered"), visible: false, isImputed: false },
  { data: "var_registered_place_lang", category: 1, header: gettext("Place registered"), visible: false, isImputed: false },
  { data: "var_nationality", category: 1, header: gettext("Flag"), visible: false, isImputed: false },
  { data: "var_imputed_nationality", category: 1, header: gettext("Flag"), visible: false, isImputed: true },
  { data: "var_rig_of_vessel", category: 1, header: gettext("Rig of vessel"), visible: false, isImputed: false },
  { data: "var_tonnage", category: 1, header: gettext("Tonnage"), visible: false, isImputed: false },
  { data: "var_tonnage_mod", category: 1, header: gettext("Standardized tonnage"), visible: false, isImputed: true },
  { data: "var_guns_mounted", category: 1, header: gettext("Guns mounted"), visible: false, isImputed: false },

  // itinerary
  { data: "var_imp_port_voyage_begin_lang", category: 2, header: gettext("Place where voyage began"), isImputed: true },
  { data: "var_imp_principal_place_of_slave_purchase_lang", category: 2, header: gettext("Principal place of purchase"), isImputed: true },
  { data: "var_first_place_slave_purchase_lang", category: 2, header: gettext("1st place of purchase"), visible: false, isImputed: false },
  { data: "var_second_place_slave_purchase_lang", category: 2, header: gettext("2nd place of purchase"), visible: false, isImputed: false },
  { data: "var_third_place_slave_purchase_lang", category: 2, header: gettext("3rd place of purchase"), visible: false, isImputed: false },
  { data: "var_port_of_call_before_atl_crossing_lang", category: 2, header: gettext("Places of call before Atlantic crossing"), visible: false, isImputed: false },
  { data: "var_imp_principal_port_slave_dis_lang", category: 2, header: gettext("Principal place of slave landing"), isImputed: true },
  { data: "var_first_landing_place_lang", category: 2, header: gettext("1st place of slave landing"), visible: false, isImputed: false },
  { data: "var_second_landing_place_lang", category: 2, header: gettext("2nd place of slave landing"), visible: false, isImputed: false },
  { data: "var_third_landing_place_lang", category: 2, header: gettext("3rd place of slave landing"), visible: false, isImputed: false },
  { data: "var_place_voyage_ended_lang", category: 2, header: gettext("Place where voyage ended"), visible: false, isImputed: false },

  // slaves
  { data: "var_imp_total_num_slaves_purchased", category: 3, header: gettext("Total embarked"), visible: false, isImputed: true },
  { data: "var_total_num_slaves_purchased", category: 3, header: gettext("Total embarked"), visible: false, isImputed: false },
  { data: "var_imp_total_slaves_disembarked", category: 3, header: gettext("Total disembarked"), visible: false, isImputed: true },
  { data: "var_num_slaves_intended_first_port", category: 3, header: gettext("Slaves intended"), visible: false, isImputed: false },
  { data: "var_num_slaves_carried_first_port", category: 3, header: gettext("Slaves from 1st port"), visible: false, isImputed: false },
  { data: "var_num_slaves_carried_second_port", category: 3, header: gettext("Slaves from 2nd port"), visible: false, isImputed: false },
  { data: "var_num_slaves_carried_third_port", category: 3, header: gettext("Slaves from 3rd port"), visible: false, isImputed: false },
  { data: "var_total_num_slaves_arr_first_port_embark", category: 3, header: gettext("Slaves arrived 1st port"), isImputed: false },
  { data: "var_num_slaves_disembark_first_place", category: 3, header: gettext("Slaves landed 1st port"), visible: false, isImputed: false },
  { data: "var_num_slaves_disembark_second_place", category: 3, header: gettext("Slaves landed 2nd port"), visible: false, isImputed: false },
  { data: "var_num_slaves_disembark_third_place", category: 3, header: gettext("Slaves landed 3rd port"), visible: false, isImputed: false },
  { data: "var_imputed_percentage_men", category: 3, header: gettext("Percent men"), visible: false, isImputed: false },
  { data: "var_imputed_percentage_women", category: 3, header: gettext("Percent women"), visible: false, isImputed: false },
  { data: "var_imputed_percentage_boys", category: 3, header: gettext("Percent boys"), visible: false, isImputed: false },
  { data: "var_imputed_percentage_girls", category: 3, header: gettext("Percent girls"), visible: false, isImputed: false },
  { data: "var_imputed_percentage_male", category: 3, header: gettext("Percent males"), visible: false, isImputed: false },
  { data: "var_imputed_percentage_child", category: 3, header: gettext("Percent children"), visible: false, isImputed: false },
  { data: "var_imputed_sterling_cash", category: 3, header: gettext("Sterling cash price in Jamaica"), visible: false, isImputed: false },
  { data: "var_imputed_death_middle_passage", category: 3, header: gettext("Captives died during middle passage"), visible: false, isImputed: false },
  { data: "var_imputed_mortality", category: 3, header: gettext("Mortality rate"), visible: false, isImputed: false },

  // dates
  { data: "var_length_middle_passage_days", category: 4, header: gettext("Middle passage (days)"), visible: false, isImputed: false },
  { data: "var_imp_length_home_to_disembark", category: 4, header: gettext("Voyage length, homeport to landing (days)"), visible: false, isImputed: false },
  { data: "var_voyage_began_partial", category: 4, header: gettext("Date that voyage began"), visible: false, isImputed: false },
  { data: "var_slave_purchase_began_partial", category: 4, header: gettext("Date trade began in Africa"), visible: false, isImputed: false },
  { data: "var_date_departed_africa_partial", category: 4, header: gettext("Date vessel departed Africa"), visible: false, isImputed: false },
  { data: "var_first_dis_of_slaves_partial", category: 4, header: gettext("Date vessel arrived with slaves"), visible: false, isImputed: false },
  { data: "var_departure_last_place_of_landing_partial", category: 4, header: gettext("Date vessel departed for homeport"), visible: false, isImputed: false },
  { data: "var_voyage_completed_partial", category: 4, header: gettext("Date voyage completed"), visible: false, isImputed: false },

  // captain and crew
  { data: "var_captain", category: 5, header: gettext("Captain's name"), isImputed: false },
  { data: "var_crew_voyage_outset", category: 5, header: gettext("Crew at voyage outset"), visible: false, isImputed: false },
  { data: "var_crew_first_landing", category: 5, header: gettext("Crew at first landing of slaves"), visible: false, isImputed: false },
  { data: "var_crew_died_complete_voyage", category: 5, header: gettext("Crew deaths during voyage"), visible: false, isImputed: false },

  // outcome
  { data: "var_outcome_voyage_lang", category: 6, header: gettext("Particular outcome of voyage"), visible: false, isImputed: false },
  { data: "var_outcome_slaves_lang", category: 6, header: gettext("Outcome of voyage for slaves"), visible: false, isImputed: false },
  { data: "var_outcome_ship_captured_lang", category: 6, header: gettext("Outcome of voyage if ship captured"), visible: false, isImputed: false },
  { data: "var_outcome_owner_lang", category: 6, header: gettext("Outcome of voyage for owner"), visible: false, isImputed: false },
  { data: "var_resistance_lang", category: 6, header: gettext("African resistance"), visible: false, isImputed: false },

  // sources
  {
    data: "var_sources",
    category: 7,
    header: gettext("Sources"),
    visible: false,
    render: function ( data ) {
      var sourceString = "";
      var count = 0;
      if (data !== null) {
        data.forEach(function(source) {
          count += 1;
          var elements = source.split("<>");
          // var postfix = data.length == count ? "" : ";";
          var postfix = "";
          sourceString += "<span data-toggle='tooltip' data-placement='top' data-html='true' title='" + gettext(elements[1]) + "'>" + gettext(elements[0]) + gettext(postfix) + " </span><br/>";
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

  var title = c.isImputed ? "<span>" + c.header + "</span> <span class='badge badge-pill badge-secondary' data-toggle='tooltip' data-placement='top' title='" + gettext("Imputed results are calculated by an algorithm.") + "'> IMP </span>" : gettext(c.header);

  categories[c.category].columns.push({
    extend: 'columnToggle',
    text: title,
    columns: index,
  });

  c.title = "<span class='column-header'>" + c.header + "</span>";
  
  // add render function to customize the display of imputed variables
  if (c.isImputed) {
    c.title += ' <span class="badge badge-pill badge-secondary tooltip-pointer" data-toggle="tooltip" data-placement="top" title="' + gettext("Imputed results are calculated by an algorithm.") + '"> IMP </span>';
  }
  
  c.render = function (data) {
    var formattedString = "";
    if (data !== null) {
      formattedString = "<span>" + data + "</span>";
    } else {
      formattedString = data
    }
    return formattedString;
  };

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
  buttons: { extend: 'colvisRestore', text: gettext('Restore default') },
  text: gettext("Restore default"),
};

defaultBtns.push(restoreBtn);

var columnToggleMenu = {
  extend: 'collection',
  text: gettext('Configure columns'),
  titleAttr: gettext('Configure visible columns'),
  className: 'btn btn-info buttons-collection dropdown-toggle',
  buttons: defaultBtns,
};

var pageLength = {
  extend: 'pageLength',
  className: 'btn btn-info buttons-collection dropdown-toggle',
};
