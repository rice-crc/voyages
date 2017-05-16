import Ember from 'ember';

export default Ember.Component.extend({
  attributeBindings: ["data-submenu-id"],
  "data-submenu-id": "submenu-vessel-name",
  filter: Ember.inject.service("voyagesSearch"),
  fieldId: "ship_name",
  op: "contains",
  label: "Vessel Name",
  vesslName: "",
  count: 0,
  resetDisabled: Ember.computed("count", function() {
    return (this.get("count") <= 0);
  }),
  applyDisabled: Ember.computed("vesselName", function() {
    return (this.get("vesselName") == "" || typeof(this.get("vesselName")) == "undefined");
  }),

  actions: {
    applyVesselName: function() {
      var filter = this.get("filter");
      var fieldId = this.get("fieldId");
      var op = this.get("op");
      var vesselName = this.get("vesselName");
      var activeSearchTerms = {
        varName: fieldId,
        op: op,
        searchTerm: vesselName
      };
      if (!this.get("count")) {
        this.set("count", 1);
        filter.set("shipNationOwnerCount", filter.get("shipNationOwnerCount") + 1);
      }
      filter.updateSearch(activeSearchTerms);
    },

    removeSearch: function() {
      var filter = this.get("filter")
      var fieldId = this.get("fieldId");
      this.set("vesselName", "");
      if (this.get("count")) {
        this.set("count", 0);
        filter.set("shipNationOwnerCount", filter.get("shipNationOwnerCount") - 1);
      }
      filter.removeSearch(fieldId);
    }
  }
});
