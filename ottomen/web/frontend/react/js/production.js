var React = require('React');
var FluxApp = require('./components/FluxApp');
require('./utils/api/production/*.js', { glob: true })
React.render(
  <FluxApp />,
  document.getElementById('app')
);
