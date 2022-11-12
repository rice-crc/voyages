var categoryNames = [
  gettext("Name"),
  gettext("Itinerary"),
  gettext("Personal Data"),
  gettext("Biographical Sources"),
  gettext("Contribution"),
];

function bioSourceHeader() {
  return `${gettext("Biographical Sources")} <span class="badge badge-pill badge-secondary tooltip-pointer" data-toggle="tooltip" data-placement="top" title="${gettext("Sources for associated voyages appear in each voyage record")}"> SRC </span>`;
}

var allColumns = [
  // name
  { data: "alias_list", category: 0, header: gettext("Full Name"), isImputed: false, orderable: false },
  { data: "ranking", category: 0, header: gettext("Search Ranking"), isImputed: false, isUserSearchBased: true, visible: false },
  
  // voyages
  { data: "voyages_list", className: "dt-control text-center voyages", category: 1, header: gettext("Voyages"), isImputed: false, orderable: false, defaultContent: '' },
  { data: "relations_list", className: "dt-control text-center relations", category: 1, header: gettext("Relations"), isImputed: false, orderable: false, defaultContent: '' },
  { data: "cached_properties__enslaved_count", className: "text-right", category: 1, header: gettext("Number of Captives"), isImputed: false, defaultContent: '' },

  // personal data
  { data: "birth_day", className: "text-right", category: 2, header: gettext("Birth Day"), isImputed: false },
  { data: "birth_month", className: "text-right", category: 2, header: gettext("Birth Month"), isImputed: false },
  { data: "birth_year", className: "text-right", category: 2, header: gettext("Birth Year"), isImputed: false },
  { data: "death_day", className: "text-right", category: 2, header: gettext("Death Day"), isImputed: false },
  { data: "death_month", className: "text-right", category: 2, header: gettext("Death Month"), isImputed: false },
  { data: "death_year", className: "text-right", category: 2, header: gettext("Death Year"), isImputed: false },

  // sources
  { data: "sources_list", category: 3, header: bioSourceHeader(), isImputed: false, visible: false, orderable: false },

  { data: "id", category: 4, header: gettext("Contribute"), isImputed: false, isContribute: true, orderable: false },
  
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
  else if (c.nameBadge) {
    c.title += ' <span class="badge badge-pill badge-secondary tooltip-pointer" data-toggle="tooltip" data-placement="top" title="' + gettext("Some individuals had multiple names listed in the historical record.") + '"> NAME </span>';
  }
  // add render function to customize the display of data based on user's search
  if (c.isUserSearchBased) {
    c.title += ' <span class="badge badge-pill badge-secondary tooltip-pointer" data-toggle="tooltip" data-placement="top" title="' + gettext("Data based on the user's search and that is not part of the database.") + '"> USER </span>';
  }

  c.render = function (data, type, row, meta) {
    var formattedString = "";
    if (data !== null) {
      if (c.data == 'sources_list') {
        formattedString = data;
      } else if (c.isContribute) {
        // Read local storage to determine what type of contribution was
        // started in the UI.
        formattedString = "";
        //formattedString = `<a href="/past/enslavers_contribute/edit/${data}"><i class="fas fa-edit btn btn-transparent"></i></a>`;
      } else if (c.data == 'voyages_list' || c.data == 'relations_list') {
        if (data.length > 0) {
          formattedString = '<i class="fa fa-plus-square" aria-hidden="true"></i>';
        }
      } else if (c.data == 'alias_list') {
        formattedString += "<span class=\"h6 pr-2\"><span class=\"badge badge-pill badge-secondary\">"+row.principal_alias+"</span></span>";
        data.forEach((value) => {
          formattedString += "<span class=\"h6 pr-2\"><span class=\"badge badge-pill badge-secondary font-weight-normal\">"+value+"</span></span>";
        });
      } else {
        formattedString = "<span>" + data + "</span>";
        var column = c.data;
        if (column == 'voyage_id') {
          formattedString = '<a href="javascript:void(0)" onclick="openVoyageModal(' + data + ');">' + formattedString + '</a>'
        }
      }
    } else {
      formattedString = data;
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

$('body').on('click', function (e) {
  //did not click a popover toggle, or icon in popover toggle, or popover
  if ($(e.target).parents('.popover').length === 0) {
    $('[data-toggle="popover"]').popover('hide');
  }
  var toggle = $(e.target).data('toggle');
  if (toggle == "popover") {
    $(e.target).popover('show');
  }
});

