var AppDispatcher = require('../dispatcher/AppDispatcher');
var EventEmitter = require('events').EventEmitter;
var SessionConstants = require('../constants/Session');
var SessionActions = require('../actions/Session');
var _ = require('underscore');

// Define initial data points
var _questions = {}, _loaded = false;

// Method to load session data from API
function loadSessionData(data) {
  _questions = data.questions;
  _loaded = true;
}

// Extend QuestionsStore with EventEmitter to add eventing capabilities
var QuestionsStore = _.extend({}, EventEmitter.prototype, {
  // Return Session data
  getQuestions: function() {
    return _questions;
  },

  // Return loaded
  getLoaded: function() {
    return _loaded;
  },

  // Set loaded
  setLoaded: function(loaded) {
    _loaded = loaded;
  },

  // Add change listener
  addChangeListener: function(callback) {
    this.on('change', callback);
  },

  // Emit Change event
  emitChange: function() {
    this.emit('change');
  },

  // Remove change listener
  removeChangeListener: function(callback) {
    this.removeListener('change', callback);
  }
});

// Register callback with AppDispatcher
AppDispatcher.register(function(payload) {
  var action = payload.action;
  var text;

  switch(action.actionType) {

    case SessionConstants.LOAD_SESSION_SUCCESS:
      loadSessionData(action.data);
      break;
    case SessionConstants.LOAD_SESSION:
      QuestionsStore.setLoaded(false);
      break;

    default:
      return true;
  }

  // If action was responded to, emit change event
  QuestionsStore.emitChange();

  return true;

});
module.exports = QuestionsStore
