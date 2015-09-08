import applicationRouter from './../application';
import ClientStorage from 'ember-frontend/utils/client-storage';

export default applicationRouter.extend({
  model: function(params) {
    var applicationController = this.controllerFor('application');
    var session;
    var store = this.store;
    if(applicationController.get('has_session_id')){
      // session = ClientStorage.get('session_' + ClientStorage.get('session_id'));
      // session['id'] = ClientStorage.get('session_id');
      // return store.push('session', session);
      return this.store.find('session', ClientStorage.get('session_id'));
    }else{
      session = store.createRecord('session', {
        worker_id: ClientStorage.get('worker_id'),
        task_id: ClientStorage.get('task_id'),
        hit_id:  ClientStorage.get('hit_id')
      }).save();
      return session;
    }
  },
  afterModel(session, transition) {
    ClientStorage.set('session_' + session.get('id'), session.serialize({embedded: true}));
    ClientStorage.set('session_id', session.get('id'));
    this._super(session, transition);
  },
  setupController: function (controller, model) {
    // Call _super for default behavior
    this._super(controller, model);
    // Implement your custom setup after
    ClientStorage.set('experiment_started', true);
    var task_id = ClientStorage.get('assignmentid');
    if(task_id){
      controller.set('assignmentid', task_id);
    }
  },
  actions:{
    next(answer) {
      var index = ClientStorage.get('index') + 1;
      var question;
      var controller = this.get('controller');
      var model = controller.get('model');
      var questions = model.get('questions');
      var route = this;
      if(questions.get('length') > index){
          question = questions.objectAt(index);
      }
      var answers = ClientStorage.get('answers') || [];

      ClientStorage.set('index', index);
      answers.push({id: controller.get('question').get('id'), answers: answer});
      ClientStorage.set('answers', answers);

      if(question){
        controller.set('question', question);
      }else{
          ClientStorage.set('index', 0);
          var answ = answers.map(function(ans){
            return route.store.createRecord('answer',{
              question_id: ans.id,
              malwares: $.makeArray(ans.answers)
            });
          });
          model.set('answers', answ);
          model.save().then(function(session){
            controller.set('model', session);
            question = session.get('questions').objectAt(0);
            controller.set('question', question);
            if(session && session.get('completed')){
              return route.transitionTo('completed');
            }
            if(session && session.get('banned')){
              return route.transitionTo('banned');
            }
            if(session && session.get('no_questions')){
              return route.transitionTo('no_questions');
            }
          });
          // Send answers
          ClientStorage.set('answers', null);
      }
    }
  }
});
