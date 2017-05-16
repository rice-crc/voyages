import Ember from 'ember';
import config from './config/environment';

const Router = Ember.Router.extend({
  location: config.locationType,
  rootURL: config.rootURL
});

Router.map(function() {
  this.route('index',  {path: '/'});
  this.route('databases', function() {
    this.route('voyages', function() {
      this.route('search', function() {
        this.route('results');
        this.route('statistics');
        this.route('tables');
        this.route('graphs');
        this.route('timeline');
        this.route('maps');
        this.route('animation');
      });
    });
    this.route('intra-american', function() {});
    this.route('slave-trade', function() {});
    this.route('african-names', function() {});
  });
  this.route('gallery');
});

export default Router;
