var React = require('React');
var FluxApp = require('./components/FluxApp');
var Mocks = require('./Mocks');

// Load Mock Product Data into localStorage
Mocks.init();

React.render(
  <FluxApp />,
  document.getElementById('app')
);
