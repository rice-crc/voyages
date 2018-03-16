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
    },
    tabs: tabs,
    row: {
      data: null,
    },
    modalShow: false,
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

    // row in a datatable
    row: {
      handler: function(){
        this.modalShow = true;
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
      },
      deep: true
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

    clip(value) {
      alert("Short URL is: " + value);
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

// tabs
$(document).ready(function(){
    $('#v-summary-statistics').DataTable({
      dom:  "<'flex-container'>" +
            "<'row'<'col-sm-12'tr>>"
    });
    $('#v-tables').DataTable({
      dom:  "<'flex-container'>" +
            "<'row'<'col-sm-12'tr>>"
    });
});
// tabs
