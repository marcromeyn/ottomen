var React = require('React');

module.exports = React.createClass({

  render: function() {
    return (
      <div id="container" className={this.props.hidden? "hidden": ""}>
        <div id="ad">
          <div className="row">
            <div className="col-xs-2">
            </div>
            <div className="col-xs-10">
              <h1>Thank you for accepting this HIT!</h1>
              <p>
                By clicking the following URL link, you will be taken to the experiment, including complete instructions.
              </p>
              <div className="alert alert-warning">
                <b>Warning</b>: In each HIT we incorporate some questions to which we already know the answer, so that we can evaluate the trustworthiness of every worker. After completing this set of questions we will evaluate your answers, if they dont meet our standards you will be banned from participating again and this hit will be rejected.
              </div>
              <div className="alert alert-danger">
                <strong>We are still in Beta so some errors could occur, if they do, please email us at ottomen.cleaning@gmail.com. We will do our best to accept all submissions made to our system.</strong>
              </div>
              <button type="button" className="btn btn-primary btn-lg" onClick={this.props.goToInstructions} > Instructions </button>
              <button type="button" className="btn btn-default btn-lg pull-right" onClick={this.props.goToQuestions} >
                Skip Instructions <span className="glyphicon glyphicon-arrow-right"></span>
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }
});
