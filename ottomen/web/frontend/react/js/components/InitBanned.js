var React = require('react');

module.exports = React.createClass({
  render: function(){
    return (
      <div className={this.props.hidden? "hidden": ""} id="container-instructions">
      	<div className="nav">
          <h1 className="nav navbar-nav navbar-left">You are Banned</h1>
      		<div className="navbar-right" style={{paddingRight: "20px"}}>
      			<button type="button" className="btn btn-default" data-container="body" data-toggle="popover" data-placement="bottom" data-content="<p>Running into trouble?</p> <p>Please contact: <strong>ottomen.cleaning@gmail.com</strong></p>" data-html="true">
        			Help
      			</button>
      		</div>
      	</div>
      	<hr></hr>
      	<div className="instructions well">
          <div>
            <p>Your passed scores where not high enough to allow you to continue with this experiment</p>
          </div>
      	</div>
      	<hr></hr>
      </div>
    )
  }
});
