import Ember from 'ember';

export default Ember.Route.extend({
  filter: Ember.inject.service("voyagesSearch"),
  // setupController() {
  //   this.controllerFor("databases.voyages.search").set(fromYear, SEARCH_MIN_YEAR);
  //   this.controllerFor("databases.voyages.search").set(toYear, SEARCH_MAX_YEAR);
  // },

  // automatically load results tab when navigated to voyages database search
  redirect: function () {
    this.transitionTo('databases.voyages.search.results');
  },

  actions: {
    alert(message){
      alert(message);
    },

    willTransition() {
      // rollbackAttributes() removes the record from the store
      // if the model 'isNew'
      // this.controller.get('model').rollbackAttributes();
      // can design this in different ways
      // let confirmation = confirm("Leaving this page will reset your search filters. Would you like to leave?");
      // if (confirmation) {
      //   var filter = this.get("filter");
      //   filter.resetAll();
      // } else {
      //   transition.abort();
      // }
    },

  }
});
