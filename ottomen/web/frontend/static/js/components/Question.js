var React = require('React');
var $ = require('jquery');
var highlighter = require('../utils/highlighter');

module.exports = React.createClass({
  getInitialState: function() {
    return {
      loaded: false
    }
  },
  componentWillReceiveProps: function(nextProps) {
    if(!this.state.loaded && nextProps.question.id){
      highlighter("#highlighter-question");
      this.setState({loaded: true});
    }
  },

  render: function() {
    return (<div id="text">{this.props.question ? this.props.question.text : ""}</div>)
  }
});
