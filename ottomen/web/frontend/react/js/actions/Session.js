var AppDispatcher = require('../dispatcher/AppDispatcher');
var SessionConstants = require('../constants/Session');
var config = require('../config');
var d = require('../utils/api/development/SessionApi');
var p = require('../utils/api/production/SessionApi');
require('../utils/api/production/SessionApi');
var SessionApi = require('../utils/api/' + config.env + '/SessionApi');
// Define actions object
module.exports = {
  // Request session data
  createSession: function(assignmentId, workerId) {
    AppDispatcher.handleAction({actionType: SessionConstants.LOAD_SESSION });
    SessionApi.createSession(assignmentId, workerId).then(function(data){
      AppDispatcher.handleAction({actionType: SessionConstants.LOAD_SESSION_SUCCESS, data: data.data });
    }, function(err){
      AppDispatcher.handleAction({actionType: SessionConstants.LOAD_SESSION_FAIL, data: err });
    })
  }
}
