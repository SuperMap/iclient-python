var leaflet = require('jupyter-leaflet')
var widgets = require('@jupyter-widgets/base');
var _ = require('underscore')
var L = require('./SuperMap')

var SuperMapCloudTileLayerView = leaflet.LeafletTileLayerView.extend({

    create_obj: function () {
        var url = this.model.get('url');
        var options = this.get_options();
        if (!options.attribution) {
            delete options.attribution;
        }
        this.obj = L.supermap.cloudTileLayer(url, options);
    },

})

var SuperMapMapView = leaflet.LeafletMapView.extend({
})


var SuperMapCloudTileLayerModel = leaflet.LeafletTileLayerModel.extend({
    defaults: _.extend({}, leaflet.LeafletTileLayerModel.prototype.defaults, {
        _view_name: 'SuperMapCloudLayerView',
        _model_name: 'SuperMapCloudTileLayerModel',
        _view_module: 'iclientpy',
        _model_module: 'iclientpy',
        mapName: '',
        type: ''
    })
})

var SuperMapMapModel = leaflet.LeafletMapModel.extend({
    defaults: _.extend({}, leaflet.LeafletMapModel.prototype.defaults, {
        _view_name: 'SuperMapMapView',
        _model_name: 'SuperMapMapModel',
        _view_module: 'iclientpy',
        _model_module: 'iclientpy',
    })
})

module.exports = _.extend({}, leaflet, {
    SuperMapCloudTileLayerView: SuperMapCloudTileLayerView,
    SuperMapMapView: SuperMapMapView,

    SuperMapCloudTileLayerModel: SuperMapCloudTileLayerModel,
    SuperMapMapModel: SuperMapMapModel
})



