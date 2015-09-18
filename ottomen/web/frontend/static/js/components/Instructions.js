var React = require('React');
var Questions = require('./Questions');

module.exports = React.createClass({

  goToQuestions: function(){
    React.render(<Questions assignmentId={this.props.assignmentId} workerId={this.props.workerId} turkSubmitTo={this.props.turkSubmitTo} />, document.getElementById('app'));
  },
  render: function() {
    return (
      <div id="container-instructions">
      	<div className="nav">
      		<h1 className="nav navbar-nav navbar-left">Instructions</h1>
      		<div className="navbar-right" style={{paddingRight:'20px'}}>
            <button type="button" className="btn btn-default" data-container="body" data-toggle="popover" data-placement="bottom" data-content="<p>Running into trouble?</p> <p>Please contact: <strong>ottomen.cleaning@gmail.com</strong></p>" data-html="true">
              Help
            </button>
      		</div>
      	</div>
      	<hr></hr>
      	<div className="instructions well">
      	    <p>
      		    You will be supplied with a set a phrases, in them there could be a word or a combination of words that describe a
      				<a href="https://en.wikipedia.org/wiki/Malware" target="_blank" >Malware</a> like(Spyware, Adware, etc)
      				<blockquote>
      					<p>Malware, short for malicious software, is any software used to disrupt computer operation, gather sensitive information, or gain access to private computer systems. Malware is defined by its malicious intent, acting against the requirements of the computer user, and does not include software that causes unintentional harm due to some deficiency.</p>
      				</blockquote>
      				If you identify one of them in the phrase add it to the field below.
            	If you identify more than one click on the + button and a new field will appear where you can add it.
      				If you leave an input box empy it wont be submitted.
            </p>
      			<h3>Examples:</h3>
      			<blockquote>
        			<p>Of course, we cannot say that you will definitely be taken to corrupted websites after clicking on any of them; however, it is still very risky to keep <mark>Omiga</mark> virus on the system.</p>
      			</blockquote>
      			<strong>Explanation:</strong>
      			<p>If we search in <strong>Google</strong> we can see the following statement: </p>
      			<p>Omiga virus is a browser hijacker that can be installed on random computers through free software from the Internet. The program can hijack Internet Explorer, Mozilla Firefox and Google Chrome. It is an application that can change your homepage and default search provider without your consent. No matter which side you were using before, when it hijacks your browser, it will be replaced with Isearch.omiga-plus.com.</p>
      			<blockquote>
              <p>I have somehow managed to download the <mark>Window Shopper</mark> virus</p>
      			</blockquote>
      			<strong>Explanation:</strong>
      			<p>If we search in <strong>Google</strong> we can see the following statement: </p>
      			<p>Window Shopper virus is malware categorized as combo adware and browser hijacker discovered by botcrawl.com that may change internet browser settings by targeting and entrapping unsuspecting victims to unethical terms, including third-party terms the internet user may not be aware of.</p>
      			<blockquote>
        			<p>Boko Haram attack travelers, kill many, others missing: some Cameroonian travelers were killed</p>
      			</blockquote>
      			<strong>Explanation:</strong>
      			<p>This phrase has no malware so none is selected it should be submited empty.</p>
      	</div>
      	<hr></hr>
        <div className="instructionsnav">
            <div className="row">
                <div className="col-xs-2">
                </div>
                <div className="col-xs-7">
                </div>
                <div className="col-xs-2">
                  <button type="button" className="btn btn-primary btn-lg" onClick={this.goToQuestions} >
                    Begin experiment <span className="glyphicon glyphicon-arrow-right"></span>
                  </button>
                </div>
            </div>
        </div>
      </div>
    );
  }
});
