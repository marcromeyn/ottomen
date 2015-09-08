import Ember from 'ember';
import ClientStorage from 'ember-frontend/utils/client-storage';
export default Ember.Route.extend({
  afterModel(model, transition) {
    var store = this.store;
    if(ClientStorage.get('session_id')){
      var session = store.peekRecord('session', ClientStorage.get('session_id'));
      if(session && session.get('banned')){
        return this.transitionTo('banned');
      }
      if(session && session.get('completed')){
        return this.transitionTo('completed');
      }
      if(session && session.get('no_questions')){
        return this.transitionTo('no_questions');
      }
    }
  },
  setupController: function (controller, model) {
    // Call _super for default behavior
    this._super(controller, model);
    // Implement your custom setup after

    var store = this.store;

    var applicationController = this.controllerFor('application');
    var indexController = this.controllerFor('index');

    if(ClientStorage.get('session_id')){
      var session = store.peekRecord('session', ClientStorage.get('session_id'));
      if(session && session.get('banned')){
        return this.transitionTo('banned');
      }
      if(session && session.get('completed')){
        return this.transitionTo('completed');
      }
      if(session && session.get('no_questions')){
        return this.transitionTo('no_questions');
      }
    }

    if(applicationController.get('has_task_id')){
      indexController.set('task_id', applicationController.get('task_id'));
      controller.set('task_id', applicationController.get('task_id'));
    }
  }
});
