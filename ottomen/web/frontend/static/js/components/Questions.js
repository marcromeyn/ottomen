var React = require('React');
var Questions = require('./Questions');
var Loader = require('./Loader');
var SessionStore = require('../stores/Session');

function getSessionState(){
  return {
    session: SessionStore.getSession(),
    loaded: SessionStore.getLoaded()
  }
}
module.exports = React.createClass({
  getInitialState: function() {
    return getSessionState()
  },
  // Add change listeners to stores
  componentDidMount: function() {
    SessionStore.actions.createSession(this.props.assignmentId, this.props.workerId)
    SessionStore.addChangeListener(this._onChange);
  },

  // Remove change listers from stores
  componentWillUnmount: function() {
    SessionStore.removeChangeListener(this._onChange);
  },

  next: function(){
  },
  render: function() {
    return (
      <div id="container-instructions">
        <div className="instructions well" style={{height:'200px'}}>
          <Loader paging={this.state.loaded}/>
          <div id="highlighter-question">
    				<div id="text">{this.state.session.id}</div>
    			</div>
        </div>
      </div>
    );
  },
  // Method to setState based upon Store changes
  _onChange: function() {
    this.setState(getSessionState());
  }
});
