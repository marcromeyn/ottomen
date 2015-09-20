var AppDispatcher = require('../dispatcher/AppDispatcher');
var EventEmitter = require('events').EventEmitter;
var AnswerConstants = require('../constants/Answer');
var AnswerActions = require('../actions/Answer');
var _ = require('underscore');

// Define initial data points
var _answers = [], _loaded = false;

var addAnswer = function(answer){
  _answers.push(answer);
}
// Extend AnswersStore with EventEmitter to add eventing capabilities
var AnswersStore = _.extend({}, EventEmitter.prototype, {
  // Return Answers data
  getAnswers: function() {
    return _answers;
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
  actions: AnswerActions,

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
    case AnswerConstants.ADD_ANSWER:
      addAnswer(action.data);
      break;

    default:
      return true;
  }

  // If action was responded to, emit change event
  AnswersStore.emitChange();

  return true;

});
module.exports = AnswersStore
