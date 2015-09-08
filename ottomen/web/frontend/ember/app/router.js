import Ember from 'ember';
import config from './config/environment';

var Router = Ember.Router.extend({
  location: config.locationType
});

Router.map(function() {
  this.route('instructions', { path: '/instructions' });
  this.route('completed', { path: '/completed' });
  this.route('banned', { path: '/banned' });
  this.route('no_questions', { path: '/no_questions' });
  this.route('ready', { path: '/ready' });
  this.route('questions', function() {
    this.route('index', { path: '/' });
    this.route('show', { path: '/:id' });
  });
});

export default Router;
