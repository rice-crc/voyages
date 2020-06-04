var categoryNames = [
  gettext("African Name"),
];

var allColumns = [

  // name
  { data: "var_documented_name", category: 0, header: gettext("Documented name"), isImputed: false },
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
