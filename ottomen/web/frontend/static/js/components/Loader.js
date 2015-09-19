var React = require('react');

module.exports = React.createClass({
  render: function(){
    return (
      <div className={"absolute-Center loader " + (this.props.loaded ? "hidden" : "")}>
        <img src="static/assets/loader.svg" />
      </div>
    )
  }
});
