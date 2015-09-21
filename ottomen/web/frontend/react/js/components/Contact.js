var React = require('react');
var Modal = require('react-bootstrap').Modal;
var Button = require('react-bootstrap').Button;

module.exports = React.createClass({

  getInitialState() {
    return { showModal: false };
  },

  close() {
    this.setState({ showModal: false });
  },

  open() {
    this.setState({ showModal: true });
  },

  render() {
    return (
      <div className="navbar-right" style={{paddingRight:'20px'}}>

        <Button
          bsStyle="default"
          onClick={this.open}
        >
          Help
        </Button>

        <Modal show={this.state.showModal} onHide={this.close}>
          <Modal.Header closeButton>
            <Modal.Title>Running into trouble?</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            Please contact: <strong>ottomen.cleaning@gmail.com</strong>
          </Modal.Body>
          <Modal.Footer>
            <Button onClick={this.close}>Close</Button>
          </Modal.Footer>
        </Modal>
      </div>
    );
  }
});
