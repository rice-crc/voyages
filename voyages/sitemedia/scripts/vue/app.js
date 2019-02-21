// main app
var searchBar = new Vue({
  el: "#search-bar",
  delimiters: ['{{', '}}'],
  components: {
    vuejsDatepicker
  },
  data: {
    isAdvanced: false,
    filter: {
      year: year,
      shipNationOwner: shipNationOwner,
      outcome: outcome,
      itinerary: itinerary,
      dates: dates,
      captainAndCrew: captainAndCrew,
      slave: slave,
      source: source,
      settings: settings,
    },
    filterData: {
      treeselectOptions: {
      },
    },
    activated: false,
    query: {
      // put the search query in here
    },
    saved: [],
    options: {
      debug: false,
      errorMessage: null,
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

    tabs: {
      handler: function() {
        refreshUi(this.filter, this.filterData, this.currentTab, this.tabs, this.options);
      },
      deep: true,
    },

    filter: {
      handler: function(val) {

        var activated = false;
        this.currentQuery = {};

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
                              labels = getTreeselectLabel(currentVariable, currentVariable.value.searchTerm, this.filterData.treeselectOptions);
                            } else {
                              labels = currentVariable["value"]["searchTerm"];
                            }
                            var newVariable = {
                              label: currentVariable["label"],
                              op: currentVariable["value"]["op"],
                              searchTerm: labels,
                              varName: currentVariable["varName"]
                            }
                            Vue.set(this.currentQuery, currentVariable["varName"], newVariable);
                          } else if (currentVariable instanceof PercentageVariable) {
                            var searchTerm0 = currentVariable["value"]["searchTerm0"] + "%";
                            var searchTerm1 = currentVariable["value"]["searchTerm1"] ? currentVariable["value"]["searchTerm1"] + "%" : currentVariable["value"]["searchTerm1"];
                            var newVariable = {
                              label: currentVariable["label"],
                              op: currentVariable["value"]["op"],
                              searchTerm0: searchTerm0,
                              searchTerm1: searchTerm1,
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
        localStorage.displaySettings = (this.filter.settings.settings.var_display_settings.value.searchTerm === true);
      },
      deep: true,
    },

    displayChanged() {
      // display settings
      if (this.filter.settings.settings.var_display_settings.value.searchTerm) {
        $( ".dataTable" ).removeClass( "dt-font-md" );
        $( ".dataTable" ).addClass( "dt-font-sm" );
        refreshUi(this.filter, this.filterData, this.currentTab, this.tabs, this.options);
      } else {
        $( ".dataTable" ).removeClass( "dt-font-sm" );
        $( ".dataTable" ).addClass( "dt-font-md" );
        refreshUi(this.filter, this.filterData, this.currentTab, this.tabs, this.options);
      }
    },

    // row in a datatable
    row: {
      handler: function(){
        this.rowModalShow = true;
        var results = [];
        // console.log(JSON.stringify(this.row.data));
        for (group in this.filter) {
          if (group !== "year" && group !== "settings") {
            var datum = {
              group: group,
              groupName: sentenceCase(group),
              variables: {}
            };
            for (subGroup in this.filter[group]) {
              for (variable in this.filter[group][subGroup]){
                if (variable !== "count" && variable != "changed"){
                  var item = this.filter[group][subGroup][variable];
                  var varName = "var_" + item["varName"];
                  var value = this.row.data[varName];
                  var isImputed = (item.options) ? item.options.isImputed : false;

                  // Patch
                  if (varName == "var_sources_plaintext") {
                    value = ""; // empty value string
                    var sources = this.row.data["var_sources"];
                    sources.forEach(function(source){
                      var first = source.split("<>")[0];
                      var second = source.split("<>")[1];
                      value += "<div><span class='source-title'>" + first +": </span>";
                      value += "<span class='source-content'>" + second + "</span></div>";
                    })
                  }

                  // Patch outcome
                  if (varName.includes("outcome") || varName.includes("resistance")) {
                    value = this.row.data[varName + "_lang"];
                  }

                  // Patch place variables
                  if (item.type == "place") {
                    value = this.row.data[varName.slice(0, -3) + "_lang"];
                  }

                  // Patch two special place variables (after generic)
                  if (varName == "var_vessel_construction_place_idnum" || varName == "var_registered_place_idnum") {
                    value = this.row.data[varName.slice(0, -6) + "_lang"];
                  }

                  datum.variables[varName] = {
                    varName: varName,
                    label: item["label"],
                    value: value,
                    isImputed: isImputed
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
        refreshUi(this.filter, this.filterData, this.currentTab, this.tabs, this.options);
      }
    }

  },

  computed: {
    displayChanged() {
      return this.filter.settings.settings.var_display_settings.value.searchTerm;
    }
  },

  filters: {
    // a function made for the display panel to show human readable form of operators
    opLabelize: function (value) {
      if (!value) return '';
      if (value == "is one of") return "is";
      if (value == "is equal to") return "is";
      return value;
    },

    // a function made for the display panel to show human readable form of operators
    termLabelize: function(value) {
      if (!value) return '';
      if (value == "Select All") return "All";
      // if (Array.isArray(value)) return value.toString();
      if (/[0-9]{4}-[0-9]{2}-[0-9]{2}/.test(value)) return value.match(/[0-9]{4}-[0-9]{2}-[0-9]{2}/)[0];
      if (Array.isArray(value)) return '"' + value.join('", "') + '"';
      return value;
    },
  },

  methods: {

    // toggle whether we'd like to see empty items in the tables
    toggleTableOmitEmpty(){
      this.tabs.tables.options.omitEmpty = !this.tabs.tables.options.omitEmpty;
    },

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
        refreshUi(this.filter, this.filterData, this.currentTab, this.tabs, this.options);
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
      var searchTerms = searchAll(this.filter, this.filterData);
      // alert(JSON.stringify(searchTerms));
      //search(this.searchFilter, searchTerms);
      // TEMP Yang: once this is working, we should wrap
      // this call in a single instance method.
      refreshUi(this.filter, this.filterData, this.currentTab, this.tabs, this.options);
    },

    // reset inputs, filters, and counts back to default state
    reset(group, subGroup) {
      resetFilter(this.filter, group, subGroup);
      var searchTerms = searchAll(this.filter, this.filterData);
      //search(this.searchFilter, searchTerms);
      refreshUi(this.filter, this.filterData, this.currentTab, this.tabs, this.options);
    },

    resetAll() {
      window.location.reload(); // forced reload
      // for (group in this.filter) {
      //   if (group !== "settings") {
      //     for (subGroup in this.filter[group]) {
      //       if (subGroup !== "count"){
      //         resetFilter(this.filter, group, subGroup);
      //       }
      //     }
      //   }
      // }
      // var searchTerms = searchAll(this.filter, this.filterData);
      // this.currentQuery = {};
      // //search(this.searchFilter, searchTerms);
      // this.resetURL();
      // refreshUi(this.filter, this.filterData, this.currentTab, this.tabs, this.options);
    },

    refresh() {
      refreshUi(this.filter, this.filterData, this.currentTab, this.tabs, this.options);
    },

    save() {
      var searchTerms = searchAll(this.filter, this.filterData);
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
            saved_query_url: window.location.origin + "/" + TRANS_PATH + SAVED_SEARCH_LABEL + response.data.saved_query_id
          });

          localStorage.setItem("saved", JSON.stringify(vm.saved));
        }
      })
      .catch(function (error) {
        options.errorMessage = error;
        $("#sv-loader").addClass("display-none");
        $("#sv-loader-error").removeClass("display-none");
        console.log(error);
      });

    },

    clear() {
      localStorage.removeItem("saved");
      this.saved = [];
    },

    load(value) {
      console.log(value);
      var url = "/voyage/get-saved-query/" + value;
      var vm = this;
      axios.get(url, {})
      .then(function (response) {
        var query = JSON.parse(response.data.query);
        vm.filter = query.filter;
        vm.refresh();
      })
      .catch(function (error) {
        options.errorMessage = error;
        $("#sv-loader").addClass("display-none");
        $("#sv-loader-error").removeClass("display-none");
        console.log(error);
      });
    },

    reportError(){
      // draft an email
      var voyagesTeamEmail = "voyages@emory.edu";
      var title = "[ISSUE] Report an issue with Slave Voyages";
      var message = "There is an issue with Slave Voyages and is reported in this Email by a user.";
      var originalURL = location.href;

      // compose this email
      var mailtourl = "mailto:" + voyagesTeamEmail + 
                      "?subject=" + title + 
                      "&body=" + message + encodeURIComponent("\n\n") +
                      "Error: " + this.options.errorMessage + encodeURIComponent("\n\n") + 
                      "Filter: " + JSON.stringify(this.filter) + encodeURIComponent("\n\n") + 
                      "URL: " + encodeURIComponent(originalURL)+ encodeURIComponent("\n\n") + 
                      "Datetime: " + Date().toString();

      // send
      location.href = mailtourl;
    },

    refreshPage(){
      location.reload();
    },

    resetURL() {
      if (location.href.includes(SAVED_SEARCH_LABEL)) {
        location.href = location.href.split(SAVED_SEARCH_LABEL).shift();
      }
    }
  },

  mounted: function() {
    if (localStorage.displaySettings) {
      this.filter.settings.settings.var_display_settings.value.searchTerm = (localStorage.displaySettings == 'true');
    }

    if (localStorage.saved) {
      try {
        this.saved = JSON.parse(localStorage.getItem("saved"));
      }
      catch (err) {
        console.log(err);
        localStorage.removeItem("saved");
      }
    }

    $('.search-menu').on("click.bs.dropdown", function(e) {
      e.stopPropagation();
      e.preventDefault();
    });
    var self = {};
    var $vm = this;

    // load a search when present in URL
    if (location.href.includes(SAVED_SEARCH_LABEL)) {
      var savedSearchId = location.href.split(SAVED_SEARCH_LABEL).pop();
      this.load(savedSearchId);
    }

    refreshUi(this.filter, this.filterData, this.currentTab, this.tabs, this.options);
  },

  // event loop - update the menuAim everytime after it's re-rendered
  updated: function() {
    // $menu.menuAim({
    //   activate: activateSubmenu,
    //   deactivate: deactivateSubmenu
    // });
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

    // datatable
    $($.fn.dataTable.tables(true)).DataTable()
      .columns.adjust()
      .responsive.recalc();

});
