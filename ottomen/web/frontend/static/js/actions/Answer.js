var AppDispatcher = require('../dispatcher/AppDispatcher');
var AnswerConstants = require('../constants/Answer');
var SessionApi = require('../utils/SessionApi');
// Define actions object
module.exports = {
  // Request session data
  addAnswer: function(lables, question) {
    var answer = {lables: lables, questionId: question.id}
    AppDispatcher.handleAction({actionType: AnswerConstants.ADD_ANSWER, data: answer });
  }
}
