import Ember from 'ember';

export default Ember.Service.extend({
  items: null,
  hasChanged: false,
  shipNationOwnerCount: 0,
  captainCrewCount: 0,
  showAdvanced: true,

  // collection of search params
  // this is the default search object that only contains the default year range filter
  activeSearchTerms: [{ // required for all searches
    varName: YEAR_RANGE_VARNAME,
    op: 'is between',
    searchTerm: [SEARCH_MIN_YEAR, SEARCH_MAX_YEAR]
  }],

  // final search object
  // it is observing activeSearchTerms, which gets updated by the UI,
  // triggering the currentSearchObj to be updating itself
  currentSearchObj: Ember.computed("activeSearchTerms", function() {
    var newSearchObj = {
      items: this.get("activeSearchTerms"),
      orderBy: []
    }
    currentSearchObj = newSearchObj;
    return newSearchObj;
  }),

  // show reset all button or not
  showReset: Ember.computed("shipNationOwnerCount", "captainCrewCount", function() {
    var totalCount = this.get("shipNationOwnerCount") + this.get("captainCrewCount");
    return totalCount > 0 ? true : false;
  }),

  // stringified version of the current search object
  readable: Ember.computed("currentSearchObj", function() {
    var currentSearchObj = this.get("currentSearchObj");
    return JSON.stringify(this.get('currentSearchObj'));
  }),

  // function to reset this search filter to initial state
  resetAll() {
    this.set("shipNationOwnerCount", 0);
    this.set("captainCrewCount", 0);
    this.set("activeSearchTerms", [{ // required for all searches
      varName: YEAR_RANGE_VARNAME,
      op: 'is between',
      searchTerm: [SEARCH_MIN_YEAR, SEARCH_MAX_YEAR]
    }]);
  },

  // go over the current search object and update existing search object(s)
  // if it already is included in the search object collection
  // if it is not a previously set search object, add it to the collection
  // this method is called by each of the "Apply" buttons in the Ember components
  updateSearch(newSearchTerms) {
    var activeSearchTerms = JSON.parse(JSON.stringify(this.get("activeSearchTerms")));
    var exists = false;
    for (var i = 0; i < activeSearchTerms.length; i++) {
      if (activeSearchTerms[i].varName === newSearchTerms.varName) {
        exists = true;
        activeSearchTerms[i].varName = newSearchTerms.varName;
        activeSearchTerms[i].op = newSearchTerms.op;
        activeSearchTerms[i].searchTerm = newSearchTerms.searchTerm;
        break;
      }
    }
    if (exists) { // do just an update
      this.set("activeSearchTerms", activeSearchTerms);
    } else { // add new, non-existing search objects
      activeSearchTerms.push(newSearchTerms);
      this.set("activeSearchTerms", activeSearchTerms);
    }
  },

  // remove a particular search object (e.g. ship_name)
  // varName is the search object id (e.g. ship_name)
  // what it does is it removes this specific varName search from the search object collection
  removeSearch(varName) {
    var activeSearchTerms = JSON.parse(JSON.stringify(this.get("activeSearchTerms")));
    for (var i = 0; i < activeSearchTerms.length; i++) {
      if (activeSearchTerms[i].varName === varName) {
        activeSearchTerms.splice(i, 1);
        break;
      }
    }
    this.set("activeSearchTerms", activeSearchTerms);
  },

  // init() {
  //   this.set('items', ["helloworld"]);
  // },
  // remove(item) {
  //   this.get('items').removeObject(item);
  // },
  //
  // empty() {
  //   this.get('items').setObjects([]);
  // }

});
