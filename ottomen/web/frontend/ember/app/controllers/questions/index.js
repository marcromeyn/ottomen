import Ember from 'ember';
import ClientStorage from 'ember-frontend/utils/client-storage';

export default Ember.Controller.extend({
  question: Ember.computed(function() {
    var index = ClientStorage.get('index') || 0;
    var question;
    var questions = this.model.get('questions');
    if(questions.get('length') > index){
        question = questions.objectAt(index);
    }

    ClientStorage.set('index', index);
    return question;
  })
});
