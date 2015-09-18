var AppDispatcher = require('../dispatcher/AppDispatcher');
var SessionConstants = require('../constants/Session');
var SessionApi = require('../utils/SessionApi');
// Define actions object
module.exports = {
  // Request session data
  createSession: function(assignmentId, workerId) {
    AppDispatcher.handleAction({actionType: SessionConstants.LOAD_SESSION });
    SessionApi.createSession(assignmentId, workerId).then(function(data){
      session = data.session;
      AppDispatcher.handleAction({actionType: SessionConstants.LOAD_SESSION_SUCCESS, data: session });
    }, function(err){
      AppDispatcher.handleAction({actionType: SessionConstants.LOAD_SESSION_FAIL, data: err });
    })
  }
}
