var React = require('react');
var Contact = require('./Contact');

module.exports = React.createClass({
  render: function(){
    return (
      <div className={this.props.hidden? "hidden": ""} id="container">
      	<div className="nav">
          <h1 className="nav navbar-nav navbar-left">You are Banned</h1>
      		<Contact />
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
