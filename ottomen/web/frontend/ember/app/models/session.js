import DS from 'ember-data';

export default DS.Model.extend({
  questions:    DS.hasMany('questions',{async: false}),
  answers:      DS.hasMany('answers'),
  task_id:      DS.attr("string"),
  worker_id:    DS.attr("string"),
  hit_id:       DS.attr("string"),
  completed:    DS.attr('boolean', {defaultValue: false}),
  banned:       DS.attr('boolean', {defaultValue: false}),
  no_questions: DS.attr('boolean', {defaultValue: false})
});
