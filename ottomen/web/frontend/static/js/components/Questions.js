var React = require('React');
var Question = require('./Question');
var Loader = require('./Loader');
var SessionStore = require('../stores/Session');
var QuestionsStore = require('../stores/Questions');

function getSessionState(){
  return {
    questions: QuestionsStore.getQuestions(),
    loaded: QuestionsStore.getLoaded(),
    index: 0
  }
}
module.exports = React.createClass({
  getInitialState: function() {
    return getSessionState()
  },
  // Add change listeners to stores
  componentDidMount: function() {
    if(this.props.assignmentId){
      SessionStore.actions.createSession(this.props.assignmentId, this.props.workerId);
    }
    SessionStore.addChangeListener(this._onChange);
    QuestionsStore.addChangeListener(this._onChange);
  },

  // Remove change listers from stores
  componentWillUnmount: function() {
    SessionStore.removeChangeListener(this._onChange);
    QuestionsStore.removeChangeListener(this._onChange);
  },

  next: function(){
  },

  // Method to setState based upon Store changes
  _onChange: function() {
    this.setState(getSessionState());
  },

  render: function() {
    return (
      <div id="container-instructions" className={this.props.hidden ? "hidden": ""}>
      	<div className="nav">
      		<div className="nav navbar-nav navbar-left">
      			<h1 >Classify the Malwares</h1>
      			<h4>This questions are highlight questions, please highlight any malware you find on the text.</h4>
      		</div>
      		<div className="navbar-right" style={{paddingRight:'20px'}} >
      			<button type="button" className="btn btn-default" data-container="body" data-toggle="popover" data-placement="bottom" data-content="<p>Running into trouble?</p> <p>Please contact: <strong>ottomen.cleaning@gmail.com</strong></p>" data-html="true">
        			Help
      			</button>
      		</div>
      	</div>
      	<hr></hr>
      	<div className="instructions well" style={{height:'200px'}}>
          <Loader loaded={this.state.loaded}/>
      		<div id="highlighter-question">
            <Question question={this.state.loaded ? this.state.questions[this.state.index]: {}}/>
      		</div>
      	</div>
      	<hr></hr>
        <div className="instructionsnav">
          <div className="row">
            <div className="col-xs-8"></div>
      			<div className="col-xs-2">
      				<button type="button" id="next" value="next" className="btn btn-primary btn-lg continue" >
      						Next <span className="glyphicon glyphicon-arrow-right"></span>
      				</button>
      			</div>
          </div>
        </div>
      </div>
    );
  }
});
