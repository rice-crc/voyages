import Ember from 'ember';

export default Ember.Component.extend({
  attributeBindings: ["data-submenu-id"],
  "data-submenu-id": "submenu-vin",
  filter: Ember.inject.service("voyagesSearch"),
  fieldId: "voyage_id",
  options: ['equals', 'is at most', 'is at least', 'is between'],
  option: 'equals',
  fromVid: null,
  toVid: null,
  count: 0,
  applyDisabled: Ember.computed("fromVid", "toVid", "option", function(){
    if (this.get("option") == "is between") {
      if (this.get("fromVid") == null || this.get("toVid") == null) {
        return true;
      } else {
        return false;
      }
    } else {
      if (this.get("fromVid") == null) {
        return true;
      } else {
        return false;
      }
    }
  }),
  resetDisabled: Ember.computed("count", function(){
    return (this.get("count") <= 0);
  }),
  isBetween: Ember.computed("option", function(){
    return this.get("option") === "is between";
  }),
  fromLabel: Ember.computed("option", function(){
    return this.get("isBetween") ? "Starting Voyage ID" : "Voyage ID";
  }),
  toLabel: Ember.computed("option", function(){
    return this.get("isBetween") ? "Ending Voyage ID" : "Voyage ID";
  }),
  fieldRequired: Ember.computed("option", function(){
    return this.get("isBetween") ? true : false;
  }),

  actions: {
    applyVid: function(){
      var filter = this.get("filter");
      var fieldId = this.get("fieldId");
      var op = this.get("option");
      var activeSearchTerms = {
        varName: fieldId,
        op: op,
        searchTerm: [parseInt(this.get("fromVid")), parseInt(this.get("toVid"))]
      };
      if (!this.get("count")){
        this.set("count", 1);
        filter.set("shipNationOwnerCount", filter.get("shipNationOwnerCount") + 1);
      }
      filter.updateSearch(activeSearchTerms);
    },
    
    removeSearch: function(){
      var filter = this.get("filter");
      var fieldId = this.get("fieldId");
      this.set("fromVid", null);
      this.set("toVid", null);
      this.set("option", "equals");
      if (this.get("count")){
        this.set("count", 0);
        filter.set("shipNationOwnerCount", filter.get("shipNationOwnerCount") - 1);
      }
      filter.removeSearch(fieldId);
    }
  }
});
