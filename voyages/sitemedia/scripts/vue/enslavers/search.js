var categoryNames = [
  gettext("Name"),
  gettext("Itinerary"),
  gettext("Personal Data"),
  gettext("Biographical Sources")
];

function bioSourceHeader() {
  return `${gettext("Biographical Sources")} <span class="badge badge-pill badge-secondary tooltip-pointer" data-toggle="tooltip" data-placement="top" title="${gettext("Sources for associated voyages appear in each voyage record")}"> SRC </span>`;
}

const contributeCol = { data: "id", header: "", name: "contribute", className: "text-center", isImputed: false, isContribute: true, orderable: false, visible: false };

var allColumns = [
  // name
  { data: "alias_list", category: 0, header: gettext("Full Name"), isImputed: false, orderable: true },
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

  contributeCol
  
];

var categories = $.map(categoryNames, function(name) {
  return {
    name: name,
    columns: []
  };
});

const contribStateStorageKey = "enslaverContributeState";

const contribMergeChange = (sel) => {
  try {
    const contribState = JSON.parse(sessionStorage.getItem(contribStateStorageKey));
    const { selection } = contribState;
    const key = parseInt(sel.value);
    if (!!sel.checked === selection.includes(key)) {
      // Nothing changes.
      return;
    }
    if (sel.checked) {
      selection.push(key);
      if (selection.length >= 2) {
        // Ready to merge.
        sessionStorage.setItem(contribStateStorageKey, "{}");
        window.location.href = `/past/enslavers_contribute/merge/${selection[0]}/${selection[1]}`;
        return;
      }
    } else {
      selection.splice(selection.indexOf(key), 1);
    }
    updateContribState(contribState);
  } catch {
  }
};

allColumns.forEach(function(c, index) {
  var title = c.isImputed ? "<span>" + c.header + "</span> <span class='badge badge-pill badge-secondary' data-toggle='tooltip' data-placement='top' title='" + gettext("Imputed results are calculated by an algorithm.") + "'> IMP </span>" : gettext(c.header);

  if (c.category) {
    categories[c.category].columns.push({
      extend: 'columnToggle',
      text: title,
      columns: index,
    });
  }
  
  if (c.isContribute) {
  } else {
    c.title = "<span class='column-header'>" + c.header + "</span>";
  }

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
        try {
          const contribState = JSON.parse(sessionStorage.getItem(contribStateStorageKey) || "{}");
          if (contribState?.mode === 'edit' || contribState?.mode === 'split' || contribState?.mode === 'delete') {
            let icon = get_enslaver_contrib_icon(contribState.mode);
            formattedString = `<a href="/past/enslavers_contribute/${contribState.mode}/${data}"><i class="fas fa-blended-color fa-${icon} btn btn-transparent"></i></a>`;
          } else if (contribState?.mode === 'merge') {
            const isChecked = contribState.selection.includes(data);
            formattedString = `<input onchange="contribMergeChange(this)" type="checkbox" value="${data}"${isChecked ? " checked" : ""}></input>`;
          }
        } catch {
        }
      } else if (c.data == 'voyages_list' || c.data == 'relations_list') {
        if (data.length > 0) {
          formattedString = '<i class="fa fa-plus-square fa-blended-color" aria-hidden="true"></i>';
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

const contributeColHeaders = {
  "edit": gettext("Edit"),
  "merge": gettext("Merge"),
  "delete": gettext("Delete"),
  "split": gettext("Split aliases"),
}

const updateContribState = (state) => {
  const col = mainDatatable.column("contribute:name");
  const btn = mainDatatable.button('hide_enslaver_contrib_action:name');
  const prev = JSON.parse(sessionStorage.getItem(contribStateStorageKey) || "{}");
  if (!!state?.mode) {
    sessionStorage.setItem(contribStateStorageKey, JSON.stringify(state));
    let header = contributeColHeaders[state.mode];
    if (state.mode === 'merge' && state.selection.length > 0) {
      header = `${header} <span class="badge badge-pill badge-secondary tooltip-pointer" data-toggle="tooltip" data-placement="top" title="${gettext('There is already an enslaver selected for the merge operation')}" data-original-title=""> ${state.selection.length} </span>`;
    }
    col.header().innerHTML = header;
    btn.enable();
  } else {
    sessionStorage.setItem(contribStateStorageKey, "{}");
    btn.disable();
  }
  col.visible(!!state?.mode);
  if (prev?.mode !== state?.mode) {
    mainDatatable.draw();
  }
}

const enslaversContributeMenu = {
  extend: 'collection',
  autoClose: true,
  text: gettext('Edit Database'),
  titleAttr: gettext('Propose changes or additions to the Enslavers dataset'),
  className: 'btn btn-info buttons-collection dropdown-toggle',
  buttons: [{
    text: gettext('New enslaver record'),
    action: function() {
      window.location.href = "/past/enslavers_contribute/new";
    }
  }, {
    text: gettext('Edit an enslaver record'),
    action: function() {
      updateContribState({ mode: "edit" });
    }
  }, {
    text: gettext('Merge duplicate enslaver records'),
    action: function() {
      updateContribState({ mode: "merge", selection: [] });
    }
  }, {
    text: gettext('Delete an enslaver record'),
    action: function() {
      updateContribState({ mode: "delete" });
    }
  }, {
    text: gettext('Delink an alias from the enslaver'),
    action: function() {
      updateContribState({ mode: "split" });
    }
  }, {
    text: gettext('Hide action column'),
    name: 'hide_enslaver_contrib_action',
    action: function() {
      updateContribState(null);
    }
  }]
};

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

