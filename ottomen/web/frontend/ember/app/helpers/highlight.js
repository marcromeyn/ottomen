import Ember from 'ember';

export function highlight(question) {
  question = question[0];
  var text = question.get('text');
  var answers = question.get('answers');
  answers.forEach(function(answer){
    text = text.replace(answer,  '<span class="highlight">' + answer + '</span>')
  });
  return new Ember.Handlebars.SafeString(text);
}

export default Ember.Helper.helper(highlight);
