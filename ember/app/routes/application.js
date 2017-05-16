import Ember from 'ember';

export default Ember.Route.extend({

  setupController() {
    // WIP
    // reserved for getting the route name in template
    let routeName = this.get("routeName");
    if (routeName == "application") {
      this.controllerFor('application').set('isIndexPage', true);
    } else {
      this.controllerFor('application').set('isIndexPage', false);
    }
  },

  actions: {
    notify: function(item){
      console.log(`item notified ${item}`)
    }
  }

});
