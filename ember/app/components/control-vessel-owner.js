import Ember from 'ember';

export default Ember.Component.extend({
  attributeBindings: ["data-submenu-id"],
  "data-submenu-id": "submenu-vessel-owner",
  filter: Ember.inject.service("voyagesSearch"),
  fieldId: "owner",
  op: "contains",
  label: "Owner Name",
  count: 0,
  resetDisabled: Ember.computed("count", function(){
    return (this.get("count") <= 0);
  }),
  applyDisabled: Ember.computed("ownerName", function(){
    return (this.get("ownerName") == "" || typeof(this.get("ownerName")) == "undefined");
  }),

  actions: {
    apply: function(){
      var filter = this.get("filter");
      var fieldId = this.get("fieldId");
      var op = this.get("op");
      var ownerName = this.get("ownerName");
      var activeSearchTerms = {
        varName: fieldId,
        op: op,
        searchTerm: ownerName
      };
      if (!this.get("count")){
        this.set("count", 1);
        filter.set("shipNationOwnerCount", filter.get("shipNationOwnerCount") + 1);
      }
      filter.updateSearch(activeSearchTerms);
    },
    
    removeSearch: function(){
      var filter = this.get("filter")
      var fieldId = this.get("fieldId");
      this.set("ownerName", "");
      if (this.get("count")){
        this.set("count", 0);
        filter.set("shipNationOwnerCount", filter.get("shipNationOwnerCount") - 1);
      }
      filter.removeSearch(fieldId);
    }
  }
});
