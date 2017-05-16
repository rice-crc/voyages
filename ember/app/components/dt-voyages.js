import Ember from 'ember';

export default Ember.Component.extend({
  filter: Ember.inject.service("voyagesSearch"),

  // trigger to update datatable everytime the voyagesSearch filter updates
  updateSearch: Ember.observer("vs", function() {
    if (mainDatatable) {
      mainDatatable.ajax.reload();
    } else {
      this.executeSearch();
    }
  }),

  // main function to execute the datatable load/reload
  executeSearch: function() {
    mainDatatable = $('#results_main_table').DataTable({
      ajax: {
        url: "http://localhost:8000/voyage/876167cf-bc40-44f7-9557-ee8117d94008/beta_ajax_search",
        type: 'POST',
        data: function(d) {
          if (d.order) {
            currentSearchObj.orderBy = $.map(d.order, function(item) {
              var columnIndex = mainDatatable ?
                mainDatatable.colReorder.order()[item.column] :
                item.column;
              return {
                name: allColumns[columnIndex].data.substring(4),
                direction: item.dir
              };
            });
          }
          return JSON.stringify({
            searchData: currentSearchObj,
            tableParams: d,
            output: 'resultsTable'
          });
        }
      },
      dom: 'Bfrtip',
      lengthMenu: [
        [10, 25, 50, 100],
        ['10 rows', '25 rows', '50 rows', '100 rows']
      ],
      buttons: [
        'pageLength',
        {
          extend: 'collection',
          text: '<span class="glyphicon glyphicon-cog"></span> <span class="caret"></span>',
          titleAttr: 'Configure visible columns',
          buttons: [{
              extend: 'collection',
              text: 'Ship, nation, owners',
              buttons: [{
                  extend: 'columnToggle',
                  text: 'Voyage ID',
                  columns: 0,
                },
                {
                  extend: 'columnToggle',
                  text: 'Vessel name',
                  columns: 1,
                },
                {
                  extend: 'columnToggle',
                  text: 'Captain\'s name',
                  columns: 2,
                },
              ]
            },
            {
              extend: 'collection',
              text: 'Voyage Itinerary',
              buttons: [{
                  extend: 'columnToggle',
                  text: 'Year arrived with slaves*',
                  columns: 3,
                },
                {
                  extend: 'columnToggle',
                  text: 'Principal region of slave purchase*',
                  columns: 4,
                },
                {
                  extend: 'columnToggle',
                  text: 'Principal region of slave landing*',
                  columns: 5,
                },
              ]
            },
            {
              extend: 'columnToggle',
              text: 'Sources',
              columns: 6,
            },
          ]
        },
        {
          extend: 'collection',
          text: '<span class="glyphicon glyphicon-cloud-download"></span>',
          titleAttr: 'Download results',
          buttons: [{
              text: 'CSV - not implemented',
              action: function() {
                alert('not implemented yet');
              },
            },
            {
              text: 'Excel - this one works!',
              action: function() {
                var visibleColumns = $.map($.makeArray(mainDatatable.columns().visible()), function(visible, index) {
                  return visible ? allColumns[index].data : undefined;
                });
                var form = $("<form action='876167cf-bc40-44f7-9557-ee8117d94008/beta_ajax_download' method='post'>{% csrf_token %}</form>");
                form.append($("<input name='data' type='hidden'></input>").attr('value', JSON.stringify({
                  searchData: currentSearchObj,
                  cols: visibleColumns
                })));
                form.appendTo('body').submit().remove();
              },
            }
          ]
        }
      ],
      bFilter: false,
      processing: true,
      serverSide: true,
      columns: allColumns,
      stateSave: true,
      stateDuration: -1,
      colReorder: true,
    });
  },

  didInsertElement: function() {
    // trigger datatable reload after the HTML DOM is loaded
    this.executeSearch();
  }

});
