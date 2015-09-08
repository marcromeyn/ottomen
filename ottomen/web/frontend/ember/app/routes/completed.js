import Ember from 'ember';
import ClientStorage from 'ember-frontend/utils/client-storage';

export default Ember.Route.extend({
  setupController: function (controller, model) {
    var worker_submit_to = ClientStorage.get('worker_submit_to');
    var task_id = ClientStorage.get('task_id');
    var worker_id = ClientStorage.get('worker_id');
    controller.set('task_id', task_id);
    controller.set('worker_id', worker_id);
    controller.set('worker_submit_to', worker_submit_to);
  }
});
