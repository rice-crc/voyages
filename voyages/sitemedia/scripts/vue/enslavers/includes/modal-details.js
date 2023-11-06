var enslaverColumns = [
  {
    group : 'name',
    groupName : gettext('Name'),
    fields : [
      { data: "principal_alias", label: gettext("Full Name"), isImputed: false },
      { data: "alias_list", label: gettext("Alias List"), isImputed: false },
    ]
  },
  {
    group : 'personal_data',
    groupName : gettext('Personal Data'),
    fields : [
      { data: "birth_day", label: gettext("Birth Day"), isImputed: false },
      { data: "birth_month", label: gettext("Birth Month"), isImputed: false },
      { data: "birth_year", label: gettext("Birth Year"), isImputed: false },
      { data: "death_day", label: gettext("Death Day"), isImputed: false },
      { data: "death_month", label: gettext("Death Month"), isImputed: false },
      { data: "death_year", label: gettext("Death Year"), isImputed: false }
    ]
  },
  {
    group : 'voyages',
    groupName : gettext('Voyages'),
    fields : [
      { data: "voyages_list", label: gettext("Voyages"), isImputed: false },
    ]
  },
  {
    group : 'details',
    groupName : gettext('Details'),
    fields : [
      { data: "relations_list", label: gettext("Relations"), isImputed: false },
      { data: "cached_properties__enslaved_count", label: gettext("Number of Captives"), isImputed: false },
    ]
  },
  {
    group : 'sources',
    groupName : gettext('Biographical Sources'),
    fields : [
      { data: "sources_list", label: gettext("Biographical Source of data"), isImputed: false }
    ]
  }
];

function getFormattedSourceInTable(sources) {
  var value = ""; // empty value string
  try {
    sources.forEach(function(source) {
      value +=
        "<div><span data-toggle='tooltip' data-placement='top' data-html='true' data-original-title='" +
        source.full_ref +
        "'>" +
        source.text_ref +
        "</span></div>";
    });
  }
  catch(err) {
    console.log(`Error in getFormattedSourceInTable: ${err.message}`);
  }
  return value;
}

function processResponseItem(row) {
  row.names = $.map(row.names, function(s) { return s.replace(' ', '&nbsp;'); }).join('<br>');

  var arrivalDateArray = row.voyage__voyage_dates__first_dis_of_slaves ? row.voyage__voyage_dates__first_dis_of_slaves.split([',']) : '';
  var arrivalDate = '';

  if (arrivalDateArray.length == 3) {
    arrivalDate = arrivalDateArray[2];
  } else if (arrivalDateArray.length == 1) {
    arrivalDate = arrivalDateArray[0];
  }
  row.voyage__voyage_dates__first_dis_of_slaves = arrivalDate;

  var gender = '';
  if (row.gender == 1) {
    gender = gettext("Male");
  } else if (row.gender == 2) {
    gender = gettext("Female");
  }
  row.gender = gender;

  if (!row.ranking) {
    row.ranking = '1';
  } else {
    row.ranking++;
  }

  if (row.alias_list) {
    var aliasList = {};
    aliasList = row.alias_list.filter((element) => {
      return row.principal_alias != element;
    });
    row.alias_list = aliasList;
  }

  if (row.voyages_list) {
    row.voyages_list.forEach((value) => {
      var arrivalDateArray = value.voyage_year ? value.voyage_year.split([',']) : '';
      var arrivalDate = '';

      if (arrivalDateArray.length == 3) {
        arrivalDate = arrivalDateArray[2];
      } else if (arrivalDateArray.length == 1) {
        arrivalDate = arrivalDateArray[0];
      }
      value.voyage_year = arrivalDate;
    });
  }

  if (row.relations_list) {
    row.relations_list.forEach((value) => {
      var arrivalDateArray = value.date ? value.date.split([',']) : '';
      var arrivalDate = '';

      if (arrivalDateArray.length == 3) {
        arrivalDate = arrivalDateArray[2];
      } else if (arrivalDateArray.length == 1) {
        arrivalDate = arrivalDateArray[0];
      }
      value.relation_year = arrivalDate;
    });
  }

  if (!row.cached_properties__enslaved_count) {
    row.cached_properties__enslaved_count = 0;
  }

  // source formatting
  row.sources_raw = row.sources_list;
  row.sources_list = getFormattedSourceInTable(
    row.sources_list
  );

  return row;
}

function formatVoyages ( d, tableId, modalTable ) {
  tableId = tableId === undefined ? 'nested_enslaver_voyage_table' : tableId;
  var voyagesTable = `<div style="width: 100%; background-color: #FFFFFF;" class="d-flex flex-row-reverse enslaver-voyages"><table id="${tableId}" cellpadding="5" cellspacing="0" border="0" width="100%">`+
    '<thead><tr>'+
      '<th>'+gettext("Voyage ID")+'</th>'+
      '<th>'+gettext("Enslaver Alias")+'</th>'+
      '<th>'+gettext("Voyage Year")+'</th>'+
      '<th>'+gettext("Disembarkation Port")+'</th>'+
      '<th>'+gettext("Embarkation Port")+'</th>'+
      '<th>'+gettext("Role")+'</th>'+
      '<th>'+gettext("Ship Name")+'</th>'+
      '<th><span>' + gettext("Captives Embarked") + '</span> <span class="badge badge-pill badge-secondary" data-toggle="tooltip" data-placement="top" title="' + gettext("Imputed results are calculated by an algorithm.") + '"> IMP </span></th>'+
    '</tr></thead>';
    d.voyages_list.forEach((item) => {
      voyagesTable += '<tr>'+
        '<td class="text-right">'+'<a href="javascript:void(0)" onclick="openVoyageModal(' + item.voyage_id + ');">' + item.voyage_id + '</a>'+'</td>'+
        '<td>'+item.alias+'</td>'+
        '<td class="text-right">'+item.voyage_year+'</td>'+
        '<td>'+item.disembarkation_port+'</td>'+
        '<td>'+item.embarkation_port+'</td>'+
        '<td>'+item.role+'</td>'+
        '<td>'+item.ship_name+'</td>'+
        '<td class="text-right">'+item.slaves_embarked+'</td>'+
      '</tr>';
    });
    voyagesTable += '</table></div>';
    if (modalTable === undefined || modalTable === false) {
      voyagesTable += '</td></tr><tr>';
    }
  return voyagesTable;
}

function formatRelations ( d, tableId, modalTable ) {
  tableId = tableId === undefined ? 'nested_enslaver_relations_table' : tableId;
  var relationsTable = `<div style="width: 100%; background-color: #FFFFFF; max-height:200px; overflow:auto;" class="d-flex flex-row-reverse enslaver-relations"><table id="${tableId}" cellpadding="5" cellspacing="0" border="0">`+
    '<tr>'+
      '<th>'+gettext("Relation ID")+'</th>'+
      '<th>'+gettext("Alias")+'</th>'+
      '<th>'+gettext("Role")+'</th>'+
      '<th>'+gettext("Year")+'</th>'+
    '</tr>';
  d.relations_list.forEach((relation) => {
    relation.enslaved.forEach((person) => {
      relationsTable += '<tr>'+
        '<td class="text-right">'+relation.relation_id+'</td>'+
        '<td>'+person.alias+'</td>'+
        '<td>'+relation.role+'</td>'+
        '<td class="text-right">'+relation.relation_year+'</td>'+
      '</tr>';
    });
    relation.enslavers.forEach((person) => {
      relationsTable += '<tr>'+
        '<td class="text-right">'+relation.relation_id+'</td>'+
        '<td>'+person.alias+'</td>'+
        '<td>'+relation.role+'</td>'+
        '<td class="text-right">'+relation.relation_year+'</td>'+
      '</tr>';
    });
  });
  relationsTable += '</table></div>';
  if (modalTable === undefined || modalTable === false) {
      relationsTable += '</td></tr><tr>';
    }
  return relationsTable;
}

function openEnslaverModal(data) {
  axios
    .get(`/past/api/get_enslaver/${data}`)
    .then(function(response) {
      if (response.data) {
        searchBar.enslaverRow.data = processResponseItem(response.data);
        searchBar.rowModalShow = true;
      }
      return;
    })
    .then(function() {
        $("#modal-enslaver-voyages-table").css('width', '100%').addClass('table').addClass('table-striped').addClass('table-bordered');
        var tableVoyages = $("#modal-enslaver-voyages-table").DataTable({
          paging: false,
          searching: false,
          info: false,
          destroy: true,
          scrollY: "200px",
        });
        

        $("#modal-enslaver-relations-table").css('width', '100%').addClass('table').addClass('table-striped').addClass('table-bordered');
        $("#modal-enslaver-relations-table").DataTable({
          paging: false,
          searching: false,
          info: false,
          destroy: true,
          scrollY: "200px"
        });

    })
    .catch(function(error) {
      return error;
    });
}