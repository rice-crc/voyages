import Ember from 'ember';

export default Ember.Component.extend({
  filter: Ember.inject.service("voyagesSearch"),
  fieldId: YEAR_RANGE_VARNAME,
  op: "is between",
  fromYear: SEARCH_MIN_YEAR, // current from year (bound to UI)
  toYear: SEARCH_MAX_YEAR, // current to year (bound to UI)
  _fromYear: SEARCH_MIN_YEAR, // existing from year
  _toYear: SEARCH_MAX_YEAR, // exisiting to year
  minYear: SEARCH_MIN_YEAR, // lower bound of year range allowed (like a constant)
  maxYear: SEARCH_MAX_YEAR, // upper bound of year range allowed (like a constant)
  count: 0,
  resetDisabled: Ember.computed("fromYear", "toYear", function(){
    return this.get("fromYear") == this.get("_fromYear") && this.get("toYear") == this.get("_toYear");
  }),
  actions: {
    applyYearRange: function(){
      var fromYear = parseInt(this.get("fromYear"));
      var toYear = parseInt(this.get("toYear"));
      var fieldId = this.get("fieldId");
      var op = this.get("op");
      var activeSearchTerms = {
        varName: fieldId,
        op: op,
        searchTerm: [fromYear, toYear]
      };

      // update properties used for search title
      this.set("_fromYear", fromYear);
      this.set("_toYear", toYear);

      // update search
      this.get("filter").updateSearch(activeSearchTerms);
      this.set("count", 1);
    },

    removeSearch: function(){
      this.set("fromYear", this.get("minYear"));
      this.set("toYear", this.get("maxYear"));

      var fromYear = parseInt(this.get("fromYear"));
      var toYear = parseInt(this.get("toYear"));
      var fieldId = this.get("fieldId");
      var op = this.get("op");
      var activeSearchTerms = {
        varName: fieldId,
        op: op,
        searchTerm: [fromYear, toYear]
      };

      // update properties used for search title
      this.set("_fromYear", fromYear);
      this.set("_toYear", toYear);

      // update search
      this.get("filter").updateSearch(activeSearchTerms);
      this.set("count", 0);
    }
  }

});
