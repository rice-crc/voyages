// main app
var searchBar = new Vue({
  el: "#search-bar",
  delimiters: ['{{', '}}'],
  data: {
    isAdvanced: false,
    filter: {
      year: year,
      shipNationOwner: shipNationOwner,
      slave: slave,
      outcome: outcome,
      itinerary: itinerary,
      captainAndCrew: captainAndCrew,
      dates: dates,
      source: source,
      settings: settings,
    },
    activated: false,
    query: {
      // put the search query in here
    },
    saved: [],
    options: {
      debug: false,
    },
    tabs: tabs,
    row: {
      data: null,
      collapseVisible: true,
    },
    currentQuery: {},
    hasCurrentQuery: false,
    rowModalShow: false,
    currentTab: "results",
  },
  watch: {

    filter: {
      handler: function(val) {

        var activated = false;
        // count all
        for (group in this.filter) { // group: slave
          var groupCount = {
            changed: 0,
            activated: 0
          };
          for (subGroup in this.filter[group]) { // subGroup: overallNumbers
            if (subGroup !== "count") {
              var subGroupCount = {
                changed: 0,
                activated: 0
              };
              for (variable in this.filter[group][subGroup]) { // variable: var_imp_port_voyage_begin
                if (variable !== "count") {

                  if (this.filter[group][subGroup][variable].changed) {
                    subGroupCount.changed += 1;
                  }
                  if (this.filter[group][subGroup][variable].activated) {
                    subGroupCount.activated += 1;
                  }
                }
              }
              // calculate for subGroups
              this.filter[group][subGroup].count.changed = subGroupCount.changed;
              this.filter[group][subGroup].count.activated = subGroupCount.activated;

              // accumulate for the group count
              groupCount.changed += subGroupCount.changed;
              groupCount.activated += subGroupCount.activated;
            }
          }

          // set group to changed and activated
          this.filter[group].count.changed = groupCount.changed;
          this.filter[group].count.activated = groupCount.activated;
          if (this.filter[group].count.activated) {
            activated = true;
          }
        }
        this.activated = activated;

        // transform current search to a human readable form
        for (group in this.filter) {
          if (group !== "count") {
            if (this.filter[group]["count"]["activated"]) {
              for (subGroup in this.filter[group]) {
                if (subGroup !== "count") {

                  if (this.filter[group][subGroup]["count"]["activated"]) {
                    for (variable in this.filter[group][subGroup]){
                      if (variable !== "count") {
                        if (this.filter[group][subGroup][variable]["activated"]) {
                          var currentVariable = this.filter[group][subGroup][variable];
                          labels = [];
                          if (currentVariable["value"]["searchTerm"]) {
                            if (currentVariable instanceof PlaceVariable ||
                                currentVariable instanceof TreeselectVariable) {
                              var searchTerms = currentVariable.value.searchTerm;
                              var allRegion = currentVariable.options.data[0];
                              labels = getCurrentTreeselectLabel(searchTerms, allRegion);
                            } else {
                              labels = currentVariable["value"]["searchTerm"];
                            }
                            var newVariable = {
                              label: currentVariable["label"],
                              op: currentVariable["value"]["op"],
                              searchTerm: labels,
                              // searchTerm: currentVariable["value"]["searchTerm"],
                              varName: currentVariable["varName"]
                            }
                            Vue.set(this.currentQuery, currentVariable["varName"], newVariable);
                          } else {
                            var newVariable = {
                              label: currentVariable["label"],
                              op: currentVariable["value"]["op"],
                              searchTerm0: currentVariable["value"]["searchTerm0"],
                              searchTerm1: currentVariable["value"]["searchTerm1"],
                              varName: currentVariable["varName"]
                            };
                            Vue.set(this.currentQuery, currentVariable["varName"], newVariable);
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
        this.hasCurrentQuery = Object.keys(this.currentQuery).length > 0 ? true:false;
      },
      deep: true,
    },

    displayChanged() {
      // display settings
      if (this.filter.settings.settings.var_display_settings.value.searchTerm) {
        $( ".dataTable" ).removeClass( "dt-font-sm" );
        $( ".dataTable" ).addClass( "dt-font-md" );
        refreshUi(this.filter, this.currentTab, this.tabs);
      } else {
        $( ".dataTable" ).removeClass( "dt-font-md" );
        $( ".dataTable" ).addClass( "dt-font-sm" );
        refreshUi(this.filter, this.currentTab, this.tabs);
      }
    },

    // row in a datatable
    row: {
      handler: function(){
        this.rowModalShow = true;
        var results = [];
        // alert(JSON.stringify(this.row.data));
        for (group in this.filter) {
          if (group !== "year" && group !== "settings") {
            var datum = {
              group: group,
              groupName: camel2title(group),
              variables: {}
            };
            for (subGroup in this.filter[group]) {
              for (variable in this.filter[group][subGroup]){
                if (variable !== "count" && variable != "changed"){
                  var item = this.filter[group][subGroup][variable];
                  var varName = "var_" + item["varName"];
                  var value = this.row.data[varName];

                  // Patch
                  if (varName == "var_sources_plaintext") {
                    value = value.replace(/<>/g, ": ");
                  }

                  datum.variables[varName] = {
                    varName: varName,
                    label: item["label"],
                    value: value
                  }
                }
              }
            }
            results.push(datum);
          }
        }
        this.row.results = results;

        // collect ids for the group collapse. there might be a better way
        var ids = "";
        for (group in this.row.results) {
          ids = ids + this.row.results[group]["group"] + ".";
        }
        this.row.ids = ids.slice(0,-1);
      },
      deep: true
    },

    currentTab:{
      handler: function(){
        refreshUi(this.filter, this.currentTab, this.tabs);
      }
    }

  },

  computed: {
    displayChanged() {
      return this.filter.settings.settings.var_display_settings.value.searchTerm;
    }
  },

  methods: {

    // set the current tab to be the active tab
    setActive(tab) {
        this.currentTab = tab;
    },

    // update tab options
    updateTabOptions(variable, value) {
      levels = variable.split(".");
      var currentObjState = this;
      for (var i = 0; i < levels.length; i++){
          currentObjState = currentObjState[levels[i]];
      }
      currentObjState.value = value;
      var refreshTabs = ['tables', 'visualization', 'timeline'];
      if (refreshTabs.indexOf(this.currentTab) >= 0) {
        refreshUi(this.filter, this.currentTab, this.tabs);
      }
    },

    // go over items and update counts when the inputs are changed
    changed(variable, changed) {
      var varName = "var_" + variable.varName;
      // function to locate a variable
      for (key1 in this.filter) {
        for (key2 in this.filter[key1]) {
          if (key2 !== "count") {
            for (key3 in this.filter[key1][key2]) {
              if (key3 == varName) {
                if (this.filter[key1][key2][key3].value["searchTerm0"] === undefined) {
                  this.filter[key1][key2][key3].value["searchTerm"] = variable["searchTerm"];
                } else {
                  this.filter[key1][key2][key3].value["searchTerm0"] = variable["searchTerm0"];
                  this.filter[key1][key2][key3].value["searchTerm1"] = variable["searchTerm1"];
                }
                this.filter[key1][key2][key3].changed = changed;
                this.filter[key1][key2][key3].value["op"] = variable["op"];
              }
            }
          }
        }
      }
      // function to locate a variable
    },

    // turn changed items into activated state; then execute search
    apply(group, subGroup, filterValues) {
      // hide all menu upon search
      $('.dropdown-menu').removeClass('show');
      $("a.maintainHover").removeClass("maintainHover");
      // hide all menu upon search
      activateFilter(this.filter, group, subGroup, filterValues);
      var searchTerms = searchAll(this.filter);
      // alert(JSON.stringify(searchTerms));
      //search(this.searchFilter, searchTerms);
      // TEMP Yang: once this is working, we should wrap
      // this call in a single instance method.
      refreshUi(this.filter, this.currentTab, this.tabs);
    },

    // reset inputs, filters, and counts back to default state
    reset(group, subGroup) {
      resetFilter(this.filter, group, subGroup);
      var searchTerms = searchAll(this.filter);
      //search(this.searchFilter, searchTerms);
      refreshUi(this.filter, this.currentTab, this.tabs);
    },

    resetAll() {
      for (group in this.filter) {
        if (group !== "settings") {
          for (subGroup in this.filter[group]) {
            if (subGroup !== "count"){
              resetFilter(this.filter, group, subGroup);
            }
          }
        }
      }
      var searchTerms = searchAll(this.filter);
      this.currentQuery = {};
      //search(this.searchFilter, searchTerms);
      refreshUi(this.filter, this.currentTab, this.tabs);
    },

    refresh() {
      refreshUi(this.filter, this.currentTab, this.tabs);
    },

    save() {
      var searchTerms = searchAll(this.filter);
      // var existingKeys = []
      // var key = generateUniqueRandomKey(existingKeys);
      // this.saved.unshift({
      //   key: key,
      //   searchTerms: searchTerms
      // });

      var vm = this;
      axios.post('/voyage/save-query', {
        // query: serializeFilter({"filter": searchTerms}),
        query: serializeFilter({"filter": vm.filter}),
      })
      .then(function (response) {

        var exists = false;
        vm.saved.forEach(function(saved){
          if (response.data.saved_query_id == saved.saved_query_id) {
            exists = true;
          }
        })

        if (!exists) {
          vm.saved.unshift({
            saved_query_id: response.data.saved_query_id,
            saved_query_url: window.location.origin + "/" + response.data.saved_query_id
          });
        }
      })
      .catch(function (error) {
        console.log(error);
      });

    },

    load(value) {
      var url = "/voyage/get-saved-query/" + value;
      var vm = this;
      axios.get(url, {})
      .then(function (response) {
        var query = JSON.parse(response.data.query);
        vm.filter = query.filter;
        vm.refresh();
      })
      .catch(function (error) {
        console.log(error);
      });
    }
  },

  mounted: function() {
    $('.search-menu').on("click.bs.dropdown", function(e) {
      e.stopPropagation();
      e.preventDefault();
    });
    var self = {};
    var $vm = this;

    // load place related variables
    loadPlaces(this, $vm.filter.itinerary);
    loadIndividualPlace(this, $vm.filter.shipNationOwner.constructionAndRegistration.var_registered_place_idnum);
    loadIndividualPlace(this, $vm.filter.shipNationOwner.constructionAndRegistration.var_vessel_construction_place_idnum);

    // load treeselect variable
    loadOptions(this, [
      $vm.filter.outcome.outcome.var_outcome_voyage,
      $vm.filter.outcome.outcome.var_outcome_slaves,
      $vm.filter.outcome.outcome.var_outcome_ship_captured,
      $vm.filter.outcome.outcome.var_outcome_owner,
      $vm.filter.outcome.outcome.var_resistance,
      $vm.filter.shipNationOwner.rigTonnageAndGunsMounted.var_rig_of_vessel,
      $vm.filter.shipNationOwner.flag.var_nationality,
      $vm.filter.shipNationOwner.flag.var_imputed_nationality,
    ]);

    //search(this.filter, []);
    refreshUi(this.filter, this.currentTab, this.tabs);
  },

  // event loop - update the menuAim everytime after it's re-rendered
  updated: function() {
    $menu.menuAim({
      activate: activateSubmenu,
      deactivate: deactivateSubmenu
    });
  },
})

// Parse URL and activate Animation tab
window.onload = function(){
  var url = window.location.href;
  if (url.includes("#")) {
    var activeTab = url.substring(url.indexOf("#") + 1);
    if (activeTab == "animation") {
      $('#animation').click();
      searchBar.setActive("animation");
    }
  }
}

// Make Highcharts work with Bootstrap Tabs
jQuery(document).on( 'shown.bs.tab', 'a[data-toggle="tab"]', function (e) { // on tab selection event
    jQuery( "#hc-container, #graph-container-red").each(function() {
        // var chart = jQuery(this).highcharts(); // target the chart itself
        // chart.reflow() // reflow that chart
    });
});
