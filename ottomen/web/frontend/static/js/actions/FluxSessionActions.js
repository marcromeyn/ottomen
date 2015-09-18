var AppDispatcher = require('../dispatcher/AppDispatcher');
var FluxSessionConstants = require('../constants/FluxSessionConstants');
var SessionApi = require('../utils/SessionApi');
// Define actions object
module.exports = {
  // Request session data
  loadSession: function(assignmentId, workerId) {
    AppDispatcher.handleAction({actionType: FluxSessionConstants.LOAD_SESSION });
    SessionApi.createSession(assignmentId, workerId).then(function(session){
      AppDispatcher.handleAction({actionType: FluxSessionConstants.LOAD_SESSION_SUCCESS, data: session });
    }, function(err){
      AppDispatcher.handleAction({actionType: FluxSessionConstants.LOAD_SESSION_FAIL, data: err });
    })
  }
}
