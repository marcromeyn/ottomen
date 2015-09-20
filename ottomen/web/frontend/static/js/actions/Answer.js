var AppDispatcher = require('../dispatcher/AppDispatcher');
var AnswerConstants = require('../constants/Answer');
var SessionApi = require('../utils/SessionApi');
var SessionStore = require('../stores/Session');

// Define actions object
module.exports = {
  // Request session data
  addAnswer: function(lables, question) {
    var answer = {lables: lables, questionId: question.id}
    AppDispatcher.handleAction({actionType: AnswerConstants.ADD_ANSWER, data: answer });
  },
  postAnswers: function(answers){
    setTimeout(function(){
      AppDispatcher.handleAction({actionType: AnswerConstants.POST_ANSWERS });
      var session = SessionStore.getSession();
      SessionApi.postAnswers(session, answers).then(function(data){
        AppDispatcher.handleAction({actionType: AnswerConstants.POST_ANSWERS_SUCCESS, data: data });
      }, function(err){
        AppDispatcher.handleAction({actionType: AnswerConstants.POST_ANSWERS_FAIL, data: err });
      });
    }, 100);
  }
}
