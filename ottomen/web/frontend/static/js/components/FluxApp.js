var React = require('React');
var Instructions = require('./Instructions');
var Questions = require('./Questions');
var Welcome = require('./Welcome');
var CallParticipants = require('./CallParticipants');

function getQueryStringValue (key) {
  return unescape(window.location.search.replace(new RegExp("^(?:.*[&\\?]" + escape(key).replace(/[\.\+\*]/g, "\\$&") + "(?:\\=([^&]*))?)?.*$", "i"), "$1"));
}

module.exports = React.createClass({
  // Get initial state from stores
  getInitialState: function() {
    var assignmentId = getQueryStringValue("assignmentId");
    if(assignmentId == "ASSIGNMENT_ID_NOT_AVAILABLE") assignmentId = null;
    var hideWelcome, hideCallParticipants;
    if(assignmentId){
      hideWelcome = false;
      hideCallParticipants = true;
    }else{
      hideWelcome = true;
      hideCallParticipants = false;
    }

    return {
      assignmentId: assignmentId,
      workerId: getQueryStringValue("workerId"),
      turkSubmitTo: getQueryStringValue("turkSubmitTo"),
      hideInstructions: true,
      hideQuestions: true,
      hideCallParticipants: hideCallParticipants,
      hideWelcome: hideWelcome
    }
  },
  goToInstructions: function(){
    this.setState({
      hideInstructions: false,
      hideQuestions: true,
      hideCallParticipants: true,
      hideWelcome: true});
  },
  goToQuestions: function(){
    this.setState({
      hideInstructions: true,
      hideQuestions: false,
      hideCallParticipants: true,
      hideWelcome: true});
  },
  render() {
    return (
      <div id="node">
        <Welcome hidden={this.state.hideWelcome} goToInstructions={this.goToInstructions} goToQuestions={this.goToQuestions}/>
        <CallParticipants hidden={this.state.hideCallParticipants}/>
        <Instructions hidden={this.state.hideInstructions} goToQuestions={this.goToQuestions}/>
        <Questions hidden={this.state.hideQuestions} assignmentId={this.state.assignmentId} workerId={this.state.workerId} turkSubmitTo={this.state.turkSubmitTo} />
      </div>
    );
  }
})
