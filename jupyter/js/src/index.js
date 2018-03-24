// Entry point for the notebook bundle containing custom model definitions.
//
// Setup notebook base URL
//
// Some static assets may be required by the custom widget javascript. The base
// url for the notebook is not known at build time and is therefore computed
// dynamically.
var __webpack_public_path__ = document.querySelector('body').getAttribute('data-base-url') + 'nbextensions/iclientpy/';


// Load css
require('leaflet/dist/leaflet.css');
require('leaflet-draw/dist/leaflet.draw.css');

// Forcibly load the marker icon images to be in the bundle.
require('leaflet/dist/images/marker-shadow.png');
require('leaflet/dist/images/marker-icon.png');
require('leaflet/dist/images/marker-icon-2x.png');

// Export widget models and views, and the npm package version number.
module.exports = require('./iclient.js');
module.exports['version'] = require('../package.json').version;
