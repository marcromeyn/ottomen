var AppDispatcher = require('../dispatcher/AppDispatcher');
var EventEmitter = require('events').EventEmitter;
var SessionConstants = require('../constants/Session');
var SessionActions = require('../actions/Session');
var AnswerConstants = require('../constants/Answer');
var _ = require('underscore');

// Define initial data points
var _session = {}, _loaded = false;

// Method to load session data from API
function loadData(data) {
  _session = data.session;
  _loaded = true;
}

// Extend SessionStore with EventEmitter to add eventing capabilities
var SessionStore = _.extend({}, EventEmitter.prototype, {
  // Return Session data
  getSession: function() {
    return _session;
  },

  // Return loaded
  getLoaded: function() {
    return _loaded;
  },

  // Set loaded
  setLoaded: function(loaded) {
    _loaded = loaded;
  },

  // Store actions
  actions: SessionActions,

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

    // Respond to SELECT_PRODUCT action
    case SessionConstants.LOAD_SESSION_SUCCESS:
      loadData(action.data);
      break;
    case SessionConstants.LOAD_SESSION_FAIL:
      return true; //Implement FAIL !!!!
      break;
    case SessionConstants.LOAD_SESSION:
      SessionStore.setLoaded(false);
      break;
    case AnswerConstants.POST_ANSWERS_SUCCESS:
      loadData(action.data);
      break;
    default:
      return true;
  }

  // If action was responded to, emit change event
  SessionStore.emitChange();

  return true;

});
module.exports = SessionStore
