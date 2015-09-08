import applicationRouter from './application';
import ClientStorage from 'ember-frontend/utils/client-storage';

export default applicationRouter.extend({
  setupController: function (controller, model) {
    var session_id = ClientStorage.get('session_id');
    ClientStorage.remove('session_' + session_id);
    ClientStorage.remove('session_id');
    ClientStorage.remove('key');
    ClientStorage.remove('answers');
    ClientStorage.remove('index');
    ClientStorage.remove('experiment_started');
    this._super(controller, model);
  }
});
