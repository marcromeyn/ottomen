var React = require('React');
var Instructions = require('./Instructions');
var Questions = require('./Questions');
var Welcome = require('./Welcome');
var CallParticipants = require('./CallParticipants');
var SessionStore = require('../stores/Session');

function getQueryStringValue (key) {
  return unescape(window.location.search.replace(new RegExp("^(?:.*[&\\?]" + escape(key).replace(/[\.\+\*]/g, "\\$&") + "(?:\\=([^&]*))?)?.*$", "i"), "$1"));
}

module.exports = React.createClass({
  // Get initial state from stores
  getInitialState: function() {
    var assignmentId = getQueryStringValue("assignmentId");
    var workerId = getQueryStringValue("workerId");
    var turkSubmitTo = getQueryStringValue("turkSubmitTo");
    if(assignmentId == "ASSIGNMENT_ID_NOT_AVAILABLE" || !workerId || !turkSubmitTo) assignmentId = null;
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
      workerId: workerId,
      turkSubmitTo: turkSubmitTo,
      hideInstructions: true,
      hideQuestions: true,
      hideCallParticipants: hideCallParticipants,
      hideWelcome: hideWelcome
    }
  },
  componentDidMount: function() {
    SessionStore.addChangeListener(this._onChange);
  },

  // Remove change listers from stores
  componentWillUnmount: function() {
    SessionStore.removeChangeListener(this._onChange);
  },

  _onChange: function() {
    var session = SessionStore.getSession()
    if(session){
      if(session.banned){
        console.log("banned")
      }
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
