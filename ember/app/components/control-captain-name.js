import Ember from 'ember';

export default Ember.Component.extend({
  attributeBindings: ["data-submenu-id"],
  "data-submenu-id": "submenu-captain-name",
  filter: Ember.inject.service("voyagesSearch"),
  fieldId: "captain",
  op: "contains",
  label: "Captain's name",
  count: 0,
  resetDisabled: Ember.computed("count", function() {
    return (this.get("count") <= 0);
  }),
  applyDisabled: Ember.computed("captainName", function() {
    return (this.get("captainName") == "" || typeof(this.get("captainName")) == "undefined");
  }),

  actions: {
    apply: function() {
      var filter = this.get("filter");
      var fieldId = this.get("fieldId");
      var op = this.get("op");
      var captainName = this.get("captainName");
      var activeSearchTerms = {
        varName: fieldId,
        op: op,
        searchTerm: captainName
      };
      if (!this.get("count")) {
        this.set("count", 1);
        filter.set("captainCrewCount", filter.get("captainCrewCount") + 1);
      }
      filter.updateSearch(activeSearchTerms);
    },

    removeSearch: function() {
      var filter = this.get("filter")
      var fieldId = this.get("fieldId");
      this.set("captainName", "");
      if (this.get("count")) {
        this.set("count", 0);
        filter.set("captainCrewCount", filter.get("captainCrewCount") - 1);
      }
      filter.removeSearch(fieldId);
    }
  }
});
