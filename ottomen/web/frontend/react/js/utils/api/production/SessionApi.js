var Promise = require('promise');
var jQuery = require('jquery');

jQuery.ajaxSetup({
  contentType: "application/json"
});

function get(url) {
    return Promise.resolve(jQuery.getJSON(url));
};

function post(url, data) {
    return Promise.resolve(jQuery.post(url, JSON.stringify(data)));
};

function put(url, data) {
    return Promise.resolve(jQuery.ajax({
        url: url,
        type: 'PUT',
        data: JSON.stringify(data)
    }));
};

function del(url) {
    return Promise.resolve(jQuery.ajax({
        url: url,
        type: 'DELETE'
    }));
};

module.exports = {

  createSession: function(assignmentId, workerId) {
    return post('api/session',{session: {worker_id: workerId.toString(), task_id: assignmentId.toString()}})
  },

  postAnswers: function(session, answers) {
    var data = {
      session:{
        worker_id: session.worker_id.toString(),
        task_id: session.task_id.toString(),
        question_type: "string"
      },
      answers: answers.map(function(a){
        return {labels: a.labels.get(), question_id: a.questionId};
      })
    }
    return put('api/session/' + session.id, data)
  }

};
