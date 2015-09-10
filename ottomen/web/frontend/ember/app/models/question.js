import DS from 'ember-data';

export default DS.Model.extend({
  text: DS.attr("string"),
  answers: DS.attr(),
  session: DS.belongsTo('session'),

  is_boolean: function() {
    return this.get('session').get("questions_type") == "boolean";
  }.property('session'),

  is_string: function() {
    return this.get('session').get("questions_type") == "string";
  }.property('session'),

  stringAnswers: function() {
    return this.get('answers').join(' ');
  }.property('answers')
});
