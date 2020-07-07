var categoryNames = [
  gettext("African Name"),
  gettext("Personal Data"),
  gettext("Itinerary"),
  gettext("Cultural Association"),
  gettext("Fate"),
  gettext("Sources"),
];

var allColumns = [

  // name
  { data: "documented_name", category: 0, header: gettext("Documented Name"), isImputed: false },
  { data: "name_first", category: 0, header: gettext("Name First"), isImputed: false },
  { data: "name_second", category: 0, header: gettext("Name Second"), isImputed: false },
  { data: "name_third", category: 0, header: gettext("Name Third"), isImputed: false },

  // personal data
  { data: "age", category: 1, header: gettext("Age"), isImputed: false },
  { data: "gender", category: 1, header: gettext("Gender"), isImputed: false },
  { data: "height", category: 1, header: gettext("Height"), isImputed: false },

  // itinerary
  { data: "voyage__id", category: 2, header: gettext("Voyage ID"), isImputed: false },
  { data: "voyage__voyage_ship__ship_name", category: 2, header: gettext("Ship Name"), isImputed: false },
  { data: "voyage__voyage_itinerary__imp_principal_place_of_slave_purchase__place", category: 2, header: gettext("Embarkation Port"), isImputed: false },
  { data: "voyage__voyage_itinerary__imp_principal_port_slave_dis__place", category: 2, header: gettext("Disembarkation Port"), isImputed: false },
  // { data: "geocode", category: 2, header: gettext("Geocode"), isImputed: false },
  { data: "voyage__voyage_dates__first_dis_of_slaves", category: 2, header: gettext("Arrival Date"), isImputed: false },
  { data: "voyage__voyage_itinerary__int_first_port_dis__place", category: 2, header: gettext("Intended Disembarkation Port"), isImputed: false },

  // cultural association
  // { data: "register_country", category: 3, header: gettext("Register Country"), isImputed: false },
  { data: "language_group__modern_country__name", category: 3, header: gettext("Modern Country"), isImputed: false },
  { data: "ethnicity__name", category: 3, header: gettext("Ethnicity"), isImputed: false },
  { data: "language_group__name", category: 3, header: gettext("Language Group"), isImputed: false },

  //fate
  // { data: "post_disembarkation_location", category: 4, header: gettext("Post Disembarkation Location"), isImputed: false },

  // sources
  // { data: "source", category: 5, header: gettext("Source"), isImputed: false },

];

var categories = $.map(categoryNames, function(name) {
  return {
    name: name,
    columns: []
  };
});

allColumns.forEach(function(c, index) {

  var title = c.isImputed ? "<span class='imputed-result'>" + c.header + "</span> <span class='badge badge-pill badge-secondary' data-toggle='tooltip' data-placement='top' title='" + gettext("Imputed results are calculated by an algorithm.") + "'> IMP </span>" : gettext(c.header);

  categories[c.category].columns.push({
    extend: 'columnToggle',
    text: title,
    columns: index,
  });

  // add render function to customize the display of imputed variables
  if (c.isImputed) {
    c.title = "<span class='imputed-result'>" + c.header + "</span>" + ' <span class="badge badge-pill badge-secondary tooltip-pointer" data-toggle="tooltip" data-placement="top" title="' + gettext("Imputed results are calculated by an algorithm.") + '"> IMP </span>'; // italicized column title
  } else {
    c.title = c.header;
  }

  c.render = function (data) {
    var formattedString = "";
    if (data !== null) {
      formattedString = "<span class='imputed-result'>" + data + "</span>";
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
