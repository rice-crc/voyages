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
    query: {
      // put the search query in here
    },
    saved: [],
    options: {
      debug: false,
    }
  },
  computed: {},
  watch: {
    filter: {
      handler: function(val) {

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
        }

      },
      deep: true,
    },

  },

  methods: {
    // go over items and update counts when the inputs are changed
    changed(variable, changed) {
      var varName = "var_" + variable.varName;
      // function to locate a variable
      for (key1 in this.filter) {
        for (key2 in this.filter[key1]) {
          if (key2 !== "count") {
            for (key3 in this.filter[key1][key2]) {
              if (key3 == varName) {

                // if (["text", "treeselect", "place"].indexOf(this.filter[key1][key2][key3].type) !== -1) {
                //   // by type - searchTerm = [];
                //   this.filter[key1][key2][key3].value["searchTerm"] = variable["searchTerm"];
                // } else if (["number"].indexOf(this.filter[key1][key2][key3].type) !== -1) {
                //   // by type - searchTerm0 = Integer, searchTerm0 = Integer;
                //   this.filter[key1][key2][key3].value["searchTerm0"] = variable["searchTerm0"];
                //   this.filter[key1][key2][key3].value["searchTerm1"] = variable["searchTerm1"];
                // } else if (["boolean"].indexOf(this.filter[key1][key2][key3].type) !== -1) {
                //   // by type - searchTerm = Boolean;
                //   this.filter[key1][key2][key3].value["searchTerm"] = variable["searchTerm"];
                // };

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
      activateFilter(this.filter, group, subGroup, filterValues);
      var searchTerms = searchAll(this.filter);
      alert(JSON.stringify(searchTerms));
      search(this.searchFilter, searchTerms);
    },

    // reset inputs, filters, and counts back to default state
    reset(group, subGroup) {
      resetFilter(this.filter, group, subGroup);
      var searchTerms = searchAll(this.filter);
      search(this.searchFilter, searchTerms);
    },

    save() {
      var searchTerms = searchAll(this.filter);
      var existingKeys = []
      var key = generateUniqueRandomKey(existingKeys);
      this.saved.unshift({
        key: key,
        searchTerms: searchTerms
      });
    },
  },

  mounted: function() {
    $('.search-menu').on("click.bs.dropdown", function(e) {
      e.stopPropagation();
      e.preventDefault();
    });
    var self = {};
    var $vm = this;

    // // load places
    // axios.get('/contribute/places_ajax').then(function(response) {
    //   var data = processPlacesAjax(response.data);
    //   var options = [{
    //     id: 0,
    //     label: "Select All",
    //     children: null
    //   }];
    //
    //   // fill select all
    //   options = [{
    //     id: 0,
    //     code: 0,
    //     label: "Select All",
    //     children: [],
    //   }];
    //
    //   // fill broad regions
    //   for (key in data.broadRegions) {
    //     options[0].children.push({
    //       id: data.broadRegions[key].order,
    //       label: data.broadRegions[key].broad_region,
    //       children: [],
    //     })
    //   }
    //
    //   // build regions
    //   for (regionId in data.regions) {
    //     var broadRegion = data.regions[regionId].broad_region;
    //     for (broadRegionId in options[0].children) {
    //       if (options[0].children[broadRegionId].id == broadRegion.order) {
    //         options[0].children[broadRegionId].children.push({
    //           id: data.regions[regionId].code,
    //           label: data.regions[regionId].region,
    //           children: []
    //         })
    //       }
    //     }
    //   }
    //
    //   // fill ports
    //   for (portId in data.ports) {
    //     // get basic information about a port
    //     var code = data.ports[portId].code;
    //     var label = data.ports[portId].port;
    //     var regionId = data.ports[portId].region.code;
    //     var broadRegionId = data.ports[portId].region.broad_region.order;
    //
    //     // locate corresponding location in the options tree
    //     options[0].children.map(function(broadRegion) {
    //       if (broadRegion.id == broadRegionId) {
    //         broadRegion.children.map(function(region) {
    //           if (region.id == regionId) { // in the correct region
    //             region.children.push({ // fill port
    //               id: code,
    //               label: label
    //             })
    //           }
    //         })
    //       }
    //     });
    //
    //   }
    //
    //   $vm.places = options;
    // })
    // .catch(function(error) {
    //   console.log(error);
    // });

    // load place related variables
    loadPlaces(this, $vm.filter.itinerary);
    loadIndividualPlace(this, $vm.filter.shipNationOwner.constructionAndRegistration.var_registered_place);
    loadIndividualPlace(this, $vm.filter.shipNationOwner.constructionAndRegistration.var_vessel_construction_place);


    // load treeselect variable
    loadOptions(this, [
      $vm.filter.outcome.outcome.var_outcome_voyage,
      $vm.filter.outcome.outcome.var_outcome_slaves,
      $vm.filter.outcome.outcome.var_outcome_ship_captured,
      $vm.filter.outcome.outcome.var_outcome_owner,
      $vm.filter.outcome.outcome.var_resistance,
      $vm.filter.shipNationOwner.rigTonnageAndGunsMounted.var_rig_of_vessel,
      $vm.filter.shipNationOwner.flag.var_nationality,
      // $vm.filter.shipNationOwner.flag.var_imputed_nationality,
    ]);

    search(this.filter, []);
  },

  // event loop - update the menuAim everytime after it's re-rendered
  updated: function() {
    $menu.menuAim({
      activate: activateSubmenu,
      deactivate: deactivateSubmenu
    });
  },
})
