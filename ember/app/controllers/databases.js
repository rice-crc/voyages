import Ember from 'ember';

export default Ember.Controller.extend({
  // This was used in the POC - It is obsolete
  // Keep it for reference - will remove soon
  // cdromChecked: false,
  //
  // count: Ember.computed("updateBtnEnabled", function() {
  //   if (this.get("updateBtnEnabled")) {
  //     return 0;
  //   } else {
  //     return 1;
  //   }
  // }),
  //
  // exisitingState: Ember.computed('', function() { 
  //   return this.get('cdromChecked');
  // }),
  //
  // modifiedState: Ember.computed('cdromChecked', function() { 
  //   return this.get('cdromChecked'); 
  // }),
  //
  // updateBtnEnabled: Ember.computed('modifiedState', function() {
  //   var modifiedState = this.get('modifiedState');
  //   var exisitingState = this.get('exisitingState');
  //   return modifiedState === exisitingState;
  // }),
  //
  // resetBtnEnabled: Ember.computed('updateBtnEnabled', function() {
  //   return this.get('cdromChecked') === this.get('exisitingState');;
  // }),
  //
  // actions: {
  //   toggleCdrom() {
  //     alert('Will update search parameter')
  //   },
  //
  //   resetCdrom() {
  //     this.set('cdromChecked', this.get("exisitingState"));
  //   },
  //
  //   saveSearch() {
  //     alert('Will save search');
  //   }
  // },
});
