import DS from 'ember-data';

export default DS.RESTSerializer.extend({
  isNewSerializerAPI: true,
  serialize(snapshot, options){
    var json = {};
    var record = snapshot.record;
    var self = this;
    json['task_id'] = record.get('task_id');
    json['worker_id'] = record.get('worker_id');
    json['hit_id'] = record.get('hit_id');
    if(options && options['embedded']){
      json = {session: json}
    }
    ['answers', 'questions'].forEach(function(key){
      var relation = [];
      var type;
      (snapshot.hasMany(key)||[]).forEach(function(o){
        var j = o.serialize();
        j['id'] = o.id;
        relation.push(j);
      });
      if(options && options['embedded']){
        json[key] = relation;
        json['session'][key] = snapshot.hasMany(key, { ids: true });
      }else{
        json[key] = relation;
      }
    });
    return json;
  },
  attrs: {
    answers: {embedded: 'always'}
  }
});
