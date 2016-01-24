var React = require('react');

module.exports = React.createClass({
  render: function(){
    return (
      <div className={this.props.hidden? "hidden": ""} id="container">
      	<h1>You are done</h1>
      	<hr></hr>
      	<div className="instructions well">
          You have finished the current question decks, right now we have no more for you please try again later.
      	</div>
      	<hr></hr>
      </div>
    )
  }
});
