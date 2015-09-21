var React = require('React');
var FluxApp = require('./components/FluxApp');
var Mocks = require('./Mocks');
require('./utils/api/development/*.js', { glob: true })

// Load Mock Product Data into localStorage
Mocks.init();
React.render(
  <FluxApp />,
  document.getElementById('app')
);
