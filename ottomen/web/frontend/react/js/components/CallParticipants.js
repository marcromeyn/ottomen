const React = require('React');

module.exports = React.createClass({
  render: function() {
    return (
      <div id="container" className={this.props.hidden? "hidden": ""}>
        <div id="ad">
          <div className="row">
            <div className="col-xs-2">
            </div>
            <div className="col-xs-10">
              <h1>Call for participants</h1>
              <p>
                We are looking for online participants for a brief data classification experiment. The only requirements are that you are a fluent English speaker. The task should take around 10 minutes.
              </p>
              <div className="alert alert-danger">
                <strong>If your test scores are low you could be banned from trying this task again</strong>
              </div>
              <p>
                Please click the "Accept HIT" button on the Amazon site above to begin the task.
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }
});
