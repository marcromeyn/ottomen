module.exports = function(app) {
  var express = require('express');
  var answersRouter = express.Router();

  answersRouter.get('/', function(req, res) {
    res.send({
      'answers': []
    });
  });

  answersRouter.post('/', function(req, res) {
    res.status(201).end();
  });

  answersRouter.get('/:id', function(req, res) {
    res.send({
      'answers': {
        id: req.params.id
      }
    });
  });

  answersRouter.put('/:id', function(req, res) {
    res.send({
      'answers': {
        id: req.params.id
      }
    });
  });

  answersRouter.delete('/:id', function(req, res) {
    res.status(204).end();
  });

  app.use('/api/answers', answersRouter);
};
