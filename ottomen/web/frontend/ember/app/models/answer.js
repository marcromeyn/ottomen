import DS from 'ember-data';

export default DS.Model.extend({
    lables: DS.attr(),
    question_id: DS.attr()
});
