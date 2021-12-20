// main app
var searchBar = new Vue({
  el: "#search-bar",
  delimiters: ["{{", "}}"],
  components: {
    vuejsDatepicker
  },
  data: {
    isAdvanced: false,
    filter: {
      africanName: africanName,
      identity: identity,
      personalData: personalData,
      itinerary: itinerary,
      culturalAssociation: culturalAssociation,
      fate: fate,
      sources: sources,
      settings: settings
    },
    filterData: {
      treeselectOptions: {
        gender: [{
          id: "male",
          label: gettext("Male")
        },{
          id: "female",
          label: gettext("Female")
        }],
        voyage_dataset: [{
          id: "trans",
          label: gettext("Transatlantic")
        },{
          id: "african",
          label: gettext("Intra-African")
        }]
      }
    },
    enslaverRoles: {
      1: "Captain",
      2: "Investor",
      3: "Buyer",
      4: "Seller",
      5: "Owner",
      6: "Shipper",
      7: "Consignor",
    },
    activated: false,
    saved: [],
    options: {
      debug: false,
      errorMessage: null,
      isTimelapseVisible: false
    },
    tabs: tabs, // dropdown options for each tab | vue/variables/tabs.js
    row: {
      // store current row's data; used for displaying entry full details
      data: null,
      collapseVisible: true
    },
    currentQuery: {},
    hasCurrentQuery: false,
    rowModalShow: false,
    enslavedDatasetModalShow: false,
    currentTab: "results", // currently active tab
    timelapse: {
      ui: {},
      options: {},
      isVisible: null,
      data: {},
      control: {},
      currentYear: null
    },
  },
  watch: {
    tabs: {
      // when tab search option updates, refresh the UI
      handler: function() {
        this.refresh();
      },
      deep: true
    },

    filter: {
      handler: function(val) {
        var activated = false;
        this.currentQuery = {};

        // count all
        for (group in this.filter) {
          // group: slave
          var groupCount = {
            changed: 0,
            activated: 0
          };
          for (subGroup in this.filter[group]) {
            // subGroup: overallNumbers
            if (subGroup !== "count") {
              var subGroupCount = {
                changed: 0,
                activated: 0
              };
              for (variable in this.filter[group][subGroup]) {
                // variable: var_imp_port_voyage_begin
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
              this.filter[group][subGroup].count.changed =
                subGroupCount.changed;
              this.filter[group][subGroup].count.activated =
                subGroupCount.activated;

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
                    for (variable in this.filter[group][subGroup]) {
                      if (variable !== "count") {
                        if (
                          this.filter[group][subGroup][variable]["activated"]
                        ) {
                          var currentVariable = this.filter[group][subGroup][
                            variable
                          ];
                          labels = [];
                          if (currentVariable["value"]["searchTerm"]) {
                            if (
                              currentVariable instanceof PlaceVariable ||
                              currentVariable instanceof LanguageGroupVariable ||
                              currentVariable instanceof TreeselectVariable
                            ) {
                              labels = getTreeselectLabel(
                                currentVariable,
                                currentVariable.value.searchTerm,
                                this.filterData.treeselectOptions
                              );
                            } else {
                              labels = currentVariable["value"]["searchTerm"];
                            }
                            var newVariable = {
                              label: currentVariable["label"],
                              op: currentVariable["value"]["op"],
                              searchTerm: labels,
                              varName: currentVariable["varName"]
                            };
                            Vue.set(
                              this.currentQuery,
                              currentVariable["varName"],
                              newVariable
                            );
                          } else if (
                            currentVariable instanceof PercentageVariable
                          ) {
                            var searchTerm0 =
                              currentVariable["value"]["searchTerm0"] + "%";
                            var searchTerm1 = currentVariable["value"][
                              "searchTerm1"
                            ]
                              ? currentVariable["value"]["searchTerm1"] + "%"
                              : currentVariable["value"]["searchTerm1"];
                            var newVariable = {
                              label: currentVariable["label"],
                              op: currentVariable["value"]["op"],
                              searchTerm0: searchTerm0,
                              searchTerm1: searchTerm1,
                              varName: currentVariable["varName"]
                            };
                            Vue.set(
                              this.currentQuery,
                              currentVariable["varName"],
                              newVariable
                            );
                          } else {
                            var newVariable = {
                              label: currentVariable["label"],
                              op: currentVariable["value"]["op"],
                              searchTerm0:
                                currentVariable["value"]["searchTerm0"],
                              searchTerm1:
                                currentVariable["value"]["searchTerm1"],
                              varName: currentVariable["varName"]
                            };
                            Vue.set(
                              this.currentQuery,
                              currentVariable["varName"],
                              newVariable
                            );
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
        this.hasCurrentQuery =
          Object.keys(this.currentQuery).length > 0 ? true : false;
        localStorage.displaySettings =
          this.filter.settings.settings.var_display_settings.value
            .searchTerm === true;
      },
      deep: true
    },

    displayChanged() {
      // display settings
      if (this.filter.settings.settings.var_display_settings.value.searchTerm) {
        $(".dataTable").removeClass("dt-font-md");
        $(".dataTable").addClass("dt-font-sm");
      } else {
        $(".dataTable").removeClass("dt-font-sm");
        $(".dataTable").addClass("dt-font-md");
      }
      this.refresh();
    },

    // row in a datatable
    row: {
      handler: function() {
        var results = [];
        var rowData = this.row.data;
        voyageColumns.forEach(function(group, key){
          if (group.group !== "year") {
            var datum = {
              group: group.group,
              groupName: group.groupName,
              variables: {}
            };
            group.fields.forEach(function(field, key){
              var varName = field.data;
              var label = field.label !== undefined ? field.label : field.data;
              var value = rowData[varName];
              var isImputed = field.isImputed !== undefined ? field.isImputed : false;

              if (varName.indexOf('percentage') != -1 || varName.indexOf('mortality') != -1) {
                value = roundDecimal(value * 100, 1) + "%";
              }
              else if (varName == 'var_sources') {
                value = getVoyageFormattedSource(value);
              }

              datum.variables[varName] = {
                varName: varName,
                label: label,
                value: value,
                isImputed: isImputed
              };
            });
            results.push(datum);
          }
        });
        this.row.results = results;

        // collect ids for the group collapse. there might be a better way
        var ids = "";
        for (group in this.row.results) {
          ids = ids + this.row.results[group]["group"] + ".";
        }
        this.row.ids = ids.slice(0, -1);
      },
      deep: true
    },

    currentTab: {
      handler: function() {
        this.refresh();
      }
    }
  },

  computed: {
    displayChanged() {
      return this.filter.settings.settings.var_display_settings.value
        .searchTerm;
    },
    enslavedDataset() {
      return localStorage.enslavedDataset !== undefined ? localStorage.enslavedDataset : null;
    }
  },

  filters: {
    // a function made for the display panel to show human readable form of operators
    opLabelize: function(value) {
      if (!value) return "";
      if (value == "is one of") return "is";
      if (value == "is equal to") return "is";
      return value;
    },

    // a function made for the display panel to show human readable form of operators
    termLabelize: function(value) {
      if (!value) return "";
      if (value == "Select All") return "All";
      // if (Array.isArray(value)) return value.toString();
      if (/[0-9]{4}-[0-9]{2}-[0-9]{2}/.test(value))
        return value.match(/[0-9]{4}-[0-9]{2}-[0-9]{2}/)[0];
      if (Array.isArray(value)) return '"' + value.join('", "') + '"';
      return value;
    }
  },

  methods: {
    // close timelapse info card
    closeTimelapseInfo() {
      this.timelapse.isVisible = false;
    },

    // set current query
    setRowData(data) {
      Vue.set(this.row, "data", data[0]);
    },

    // toggle timelapse play/pause
    timelapseTogglePlay(value) {
      if (value == "play") {
        searchBar.$refs["timelapse-play"].ui.play();
      } else if (value == "pause") {
        searchBar.$refs["timelapse-play"].ui.pause();
      }
    },

    // toggle whether we'd like to see empty items in the tables
    toggleTableOmitEmpty() {
      this.tabs.tables.options.omitEmpty = !this.tabs.tables.options.omitEmpty;
    },

    // set the current tab to be the active tab
    setActive(tab) {
      this.currentTab = tab;
      if (location.href != location.origin + location.pathname + "#" + tab) {
        location.href = location.origin + location.pathname + "#" + tab;
      }
    },

    // update tab options
    updateTabOptions(variable, value) {
      levels = variable.split(".");
      var currentObjState = this;
      for (var i = 0; i < levels.length; i++) {
        currentObjState = currentObjState[levels[i]];
      }
      currentObjState.value = value;
      var refreshTabs = ["tables", "visualization", "timeline"];
      if (refreshTabs.indexOf(this.currentTab) >= 0) {
        this.refresh();
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
                if (
                  this.filter[key1][key2][key3].value["searchTerm0"] ===
                  undefined
                ) {
                  this.filter[key1][key2][key3].value["searchTerm"] =
                    variable["searchTerm"];
                } else {
                  this.filter[key1][key2][key3].value["searchTerm0"] =
                    variable["searchTerm0"];
                  this.filter[key1][key2][key3].value["searchTerm1"] =
                    variable["searchTerm1"];
                }
                this.filter[key1][key2][key3].changed = changed;
                this.filter[key1][key2][key3].value["op"] = variable["op"];
              }
            }
          }
        }
      }
    },

    // turn changed items into activated state; then execute search
    apply(group, subGroup, filterValues) {
      // hide all menu upon search
      $(".dropdown-menu").removeClass("show");
      $("a.maintainHover").removeClass("maintainHover");
      // hide all menu upon search
      activateFilter(this.filter, group, subGroup, filterValues);
      // var searchTerms = searchAll(this.filter, this.filterData);
      // alert(JSON.stringify(searchTerms));
      // search(this.searchFilter, searchTerms);
      this.refresh();
    },

    // reset inputs, filters, and counts back to default state
    reset(group, subGroup) {
      resetFilter(this.filter, group, subGroup);
      this.refresh();
    },

    clearFilter(filter) {
      for (group in filter) {
        if (group !== "settings") {
          for (subGroup in filter[group]) {
            if (subGroup !== "count") {
              resetFilter(filter, group, subGroup);
            }
          }
        }
      }
    },

    resetAll() {
      this.refreshPage();
      this.resetURL();
    },

    refresh() {
      refreshUi(
        this.filter,
        this.filterData,
        this.currentTab,
        this.tabs,
        this.options
      );
    },

    load(value) {
      var url = "/voyage/get-saved-query/" + value;
      var vm = this;
      axios
        .get(url, {})
        .then(function(response) {
          var query;
          if (Array.isArray(response.data.items) || typeof response.data.items == 'object') {
            query = response.data.items;
          } else {
            query = JSON.parse(response.data.items);
          }

          var mappedVarNames = $.map(query, function(value, varName) {
            return 'var_' + varName;
          });

          vm.clearFilter(vm.filter);

          // fill a loaded search query into the UI elements
          for (group in vm.filter) {
            for (subGroup in vm.filter[group]) {
              if (subGroup != "count") {
                for (varName in vm.filter[group][subGroup]) {
                  if (mappedVarNames.includes(varName)) {
                    var varNameMapping = varName.replace('var_', '');
                    var variable = query[varNameMapping];

                    vm.filter[group][subGroup][varName].activated = true;
                    vm.filter[group][subGroup][varName].changed = true;

                    if (vm.filter[group][subGroup][varName] instanceof PlaceVariable ||
                      vm.filter[group][subGroup][varName] instanceof LanguageGroupVariable ||
                      vm.filter[group][subGroup][varName] instanceof TreeselectVariable)
                    {
                      vm.filter[group][subGroup][varName].value.searchTerm = variable;
                    }
                    else if (vm.filter[group][subGroup][varName] instanceof PercentageVariable ||
                      Array.isArray(variable))
                    {
                      vm.filter[group][subGroup][varName].value.searchTerm0 = variable[0];
                      vm.filter[group][subGroup][varName].value.searchTerm1 = variable[1];
                    }
                    else
                    {
                      vm.filter[group][subGroup][varName].value.searchTerm = variable;
                    }
                  }
                }
              }
            }
          }
          vm.refresh();
        })
        .catch(function(error) {
          vm.options.errorMessage = error;
          $("#sv-loader").addClass("display-none");
          $("#sv-loader-error").removeClass("display-none");
          $(".sv-loader-error-message-container")
            .children(".v-panel-description")
            .html(
              gettext(
                "This search is either no longer valid or causing an error."
              )
            );
          console.log(error);
        });
    },

    save() {
      var items = searchAll(this.filter, this.filterData);
      var vm = this;
      axios
        .post("/voyage/save-query", {
          items: items
        })
        .then(function(response) {
          var exists = false;
          vm.saved.forEach(function(saved) {
            if (response.data.saved_query_id == saved.saved_query_id) {
              exists = true;
            }
          });

          if (!exists) {
            vm.saved.unshift({
              saved_query_id: response.data.saved_query_id,
              saved_query_url:
                window.location.origin +
                "/" +
                TRANS_PATH +
                response.data.saved_query_id
            });

            localStorage.setItem("saved", JSON.stringify(vm.saved));
          }
        })
        .catch(function(error) {
          vm.options.errorMessage = error;
          $("#sv-loader").addClass("display-none");
          $("#sv-loader-error").removeClass("display-none");
          console.log(error);
        });
    },

    clear() {
      localStorage.removeItem("saved");
      this.saved = [];
    },

    reportError() {
      // draft an email
      var voyagesTeamEmail = "voyages@emory.edu";
      var title = "[ISSUE] Report an issue with Slave Voyages";
      var message =
        "There is an issue with Slave Voyages and is reported in this Email by a user.";
      var originalURL = location.href;

      // compose this email
      var mailtourl =
        "mailto:" +
        voyagesTeamEmail +
        "?subject=" +
        title +
        "&body=" +
        message +
        encodeURIComponent("\n\n") +
        "Error: " +
        this.options.errorMessage +
        encodeURIComponent("\n\n") +
        "Filter: " +
        JSON.stringify(searchAll(this.filter, this.filterData)) +
        encodeURIComponent("\n\n") +
        "URL: " +
        encodeURIComponent(originalURL) +
        encodeURIComponent("\n\n") +
        "Datetime: " +
        Date().toString();

      // send
      location.href = mailtourl;
    },

    refreshPage() {
      window.location.reload();
    },

    resetURL() {
      if (location.href.includes(SAVED_SEARCH_LABEL)) {
        location.href = location.href.split(SAVED_SEARCH_LABEL).shift();
      }
    }
  },

  mounted: function() {
    if (localStorage.displaySettings) {
      this.filter.settings.settings.var_display_settings.value.searchTerm =
        localStorage.displaySettings == "true";
    }

    if (localStorage.saved) {
      try {
        this.saved = JSON.parse(localStorage.getItem("saved"));
      } catch (err) {
        console.log(err);
        localStorage.removeItem("saved");
      }
    }

    $(".search-menu").on("click.bs.dropdown", function(e) {
      e.stopPropagation();
      e.preventDefault();
    });

    // load a search when present in URL
    if (location.href.includes(SAVED_SEARCH_LABEL)) {
      var savedSearchId = location.href.split(SAVED_SEARCH_LABEL).pop();
      this.load(savedSearchId);
    } else {
      if (this.enslavedDataset) {
        if (localStorage.directLinkFilter) {
          var filter;
          if (this.enslavedDataset == 0) {
            this.filter.africanName.name.var_enslaved_id.activated = true;
            this.filter.africanName.name.var_enslaved_id.changed = true;
            this.filter.africanName.name.var_enslaved_id.value.op = "is equal to";
            this.filter.africanName.name.var_enslaved_id.value.searchTerm0 = localStorage.directLinkFilter;
            this.filter.africanName.name.var_enslaved_id.value.searchTerm1 = localStorage.directLinkFilter;
          } else if (this.enslavedDataset == 1) {
            this.filter.identity.name.var_enslaved_id.activated = true;
            this.filter.identity.name.var_enslaved_id.changed = true;
            this.filter.identity.name.var_enslaved_id.value.op = "is equal to";
            this.filter.identity.name.var_enslaved_id.value.searchTerm0 = localStorage.directLinkFilter;
            this.filter.identity.name.var_enslaved_id.value.searchTerm1 = localStorage.directLinkFilter;
          }
          localStorage.removeItem("directLinkFilter");
        }
        this.refresh();
      }
    }
  },

  // event loop - update the menuAim everytime after it's re-rendered
  updated: function() {
    // $menu.menuAim({
    //   activate: activateSubmenu,
    //   deactivate: deactivateSubmenu
    // });
  }
});

// Parse URL and activate Animation tab

var readURL = function() {
  var url = window.location.href;
  if (url.includes("#")) {
    var activeTab = url.substring(url.indexOf("#") + 1);
    var presetTabs = [
      "results",
    ];

    if (presetTabs.includes(activeTab)) {
      $('.nav-tabs a[href="#' + activeTab + '"]').tab("show"); // Activate a Bootstrap 4 tab
      searchBar.setActive(activeTab);
    }
  }
};

// onload and on hash change, reprocess URL
window.addEventListener("load", readURL);
window.addEventListener("popstate", readURL);

// Make Highcharts work with Bootstrap Tabs
jQuery(document).on("shown.bs.tab", 'a[data-toggle="tab"]', function(e) {
  // on tab selection event
  // jQuery( "#hc-container, #graph-container-red").each(function() {
  //     var chart = jQuery(this).highcharts(); // target the chart itself
  //     chart.reflow() // reflow that chart
  // });

  // datatable
  $($.fn.dataTable.tables(true))
    .DataTable()
    .columns.adjust()
    .responsive.recalc();
});
