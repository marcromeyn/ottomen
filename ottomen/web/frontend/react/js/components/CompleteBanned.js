var React = require('react');

module.exports = React.createClass({
  render: function(){
    return (
      <div className={this.props.hidden? "hidden": ""} id="container-instructions">
      	<div className="nav">
          <h1 classFor="nav navbar-nav navbar-left">You are done</h1>,
      		<div className="navbar-right" style={{paddingRight: "20px"}}>
      			<button type="button" className="btn btn-default" data-container="body" data-toggle="popover" data-placement="bottom" data-content="<p>Running into trouble?</p> <p>Please contact: <strong>ottomen.cleaning@gmail.com</strong></p>" data-html="true">
        			Help
      			</button>
      		</div>
      	</div>
      	<hr></hr>
      	<div className="instructions well">
          <p>You have finished the task but sadly you wont be able to try again.</p>
          <p>Click on submit to finilize the experiment</p>
          </div>
      	<hr></hr>
        <div className="instructionsnav" id="instructionsnav">
          <div classFor="row">
              <div classFor="col-xs-2">
              </div>
              <div classFor="col-xs-8">
              </div>
              <div classFor="col-xs-2">
                <form action={this.props.turkSubmitTo}>
                  <input type="hidden" name="assignmentId" value={this.props.assignmentId} />
                  <input type="hidden" name="workerid" value={this.props.workerId} />
                  <input type="submit" value="Submit" classFor="btn btn-primary btn-lg" />
                </form>
              </div>
          </div>
        </div>
      </div>
    )
  }
});
