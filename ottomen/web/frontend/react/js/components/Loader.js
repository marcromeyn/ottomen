var React = require('react');

module.exports = React.createClass({
  render: function(){
    return (
      <div className={this.props.loaded ? "hidden" : ""}>
        Your question is loading...
      </div>
    )
  }
});
