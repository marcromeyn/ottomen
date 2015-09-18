var React = require('React');
var Welcome = require('./Welcome');
var CallParticipants = require('./CallParticipants');

function getQueryStringValue (key) {
  return unescape(window.location.search.replace(new RegExp("^(?:.*[&\\?]" + escape(key).replace(/[\.\+\*]/g, "\\$&") + "(?:\\=([^&]*))?)?.*$", "i"), "$1"));
}

module.exports = React.createClass({
  // Get initial state from stores
  getInitialState: function() {
    return {
      assignmentId: getQueryStringValue("assignmentId"),
      workerId: getQueryStringValue("workerId"),
      turkSubmitTo: getQueryStringValue("turkSubmitTo")
    }
  },

  render() {
    var assignmentId = this.state.assignmentId;
    var tag;
    if(assignmentId){
      tag = <Welcome assignmentId={this.state.assignmentId} workerId={this.state.workerId} turkSubmitTo={this.state.turkSubmitTo} />;
    }else{
      tag = <CallParticipants />;
    }
    return (
      <div id="node">
        {tag}
      </div>
    );
  }
});
