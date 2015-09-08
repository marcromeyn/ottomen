import Ember from 'ember';
import ClientStorage from 'ember-frontend/utils/client-storage';
export default Ember.Controller.extend({
  queryParams: ['assignmentId', 'workerId', 'workerSubmitTo', 'hitId'],
  task_id: Ember.computed(function() {
    var task_id = this.get('assignmentId');
    var worker_id = this.get('workerId');
	  var hit_id = this.get('hitId');
    var worker_submit_to = this.get('workerSubmitTo') + '/mturk/externalSubmit';
    ClientStorage.set('worker_id', worker_id);
    ClientStorage.set('hit_id', hit_id);
    ClientStorage.set('worker_submit_to', worker_submit_to);
    if (task_id) {
      if ( task_id === "ASSIGNMENT_ID_NOT_AVAILABLE") {
        ClientStorage.set('task_id', null);
        return null;
      }
      else{
        ClientStorage.set('task_id', task_id);
        return task_id;
      }
    }
    ClientStorage.set('task_id', null);
    return null;
  }),
  has_task_id: Ember.computed(function() {
    var task_id = this.get('task_id');
    if(task_id){
      return true;
    }
    return false;
  }),
  has_session_id: Ember.computed(function() {
    var session_id = ClientStorage.get('session_id');
    if(session_id){
      return true;
    }
    return false;
  }),
  session_id: Ember.computed(function() {
    return ClientStorage.get('session_id');
  })

});
