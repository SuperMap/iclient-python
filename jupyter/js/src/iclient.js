var leaflet = require('jupyter-leaflet')
var widgets = require('@jupyter-widgets/base')
var _ = require('underscore')
var L = require('./SuperMap')
var version = require('../package.json').version


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

var SuperMapTileMapLayerView = leaflet.LeafletTileLayerView.extend({
    create_obj: function () {
        var url = this.model.get('url')
        this.obj = L.supermap.tiledMapLayer(url)
    },
})

var SuperMapRankSymbolThemeLayerView = leaflet.LeafletLayerView.extend({
    create_obj: function () {
        var name = this.model.get('name');
        var data = this.model.get('data');
        var symbolType = this.model.get('symbolType')
        var symbolSetting = this.model.get('symbolSetting');
        var themeField = this.model.get('themeField');
        // var address_key = this.model.get('address_key');
        // var value_key = this.model.get('value_key');
        // var lng_key = this.model.get('lng_key');
        // var lat_key = this.model.get('lat_key');

        var address_key = 0;
        var value_key = 1;
        var lng_key = 2;
        var lat_key = 3;
        var options = this.get_options();
        if (!options.attribution) {
            delete options.attribution;
        }

        this.obj = L.supermap.rankSymbolThemeLayer(name, SuperMap.ChartType[symbolType], options);
        this.obj.themeField = themeField;
        this.obj.symbolSetting = symbolSetting;
        this.obj.addTo(this.map_view.obj);
        this.obj.clear();
        var features = [];
        for (var i = 0, len = data.length; i < len; i++) {
            var geo = this.map_view.obj.options.crs.project(L.latLng(data[i][lat_key], data[i][lng_key]));
            var attrs = { NAME: data[i][address_key] };
            attrs[themeField] = data[i][value_key]
            var feature = L.supermap.themeFeature(geo, attrs);
            features.push(feature);
        }
        this.obj.addFeatures(features);
    },
})

var SuperMapMapView = leaflet.LeafletMapView.extend({
    create_obj: function () {
        var that = this;
        options = this.get_options();
        options.crs = L.CRS[options.crs]
        that.obj = L.map(this.el, options);
    }
})


var SuperMapCloudTileLayerModel = leaflet.LeafletTileLayerModel.extend({
    defaults: _.extend({}, leaflet.LeafletTileLayerModel.prototype.defaults, {
        _view_name: 'SuperMapCloudTileLayerView',
        _model_name: 'SuperMapCloudTileLayerModel',
        _view_module: 'iclientpy',
        _model_module: 'iclientpy',
        mapName: '',
        type: ''
    })
})

var SuperMapTileMapLayerModel = leaflet.LeafletTileLayerModel.extend({
    defaults: _.extend({}, leaflet.LeafletTileLayerModel.defaults, {
        _view_name: 'SuperMapTileMapLayerView',
        _model_name: 'SuperMapTileMapLayerModel',
        _view_module: 'iclientpy',
        _model_module: 'iclientpy',
    })
})

var SuperMapRankSymbolThemeLayerModel = leaflet.LeafletLayerModel.extend({
    defaults: _.extend({}, leaflet.LeafletLayerModel.defaults, {
        _view_name: "SuperMapRankSymbolThemeLayerView",
        _model_name: "SuperMapRankSymbolThemeLayerModel",
        _view_module: 'iclientpy',
        _model_module: 'iclientpy',
        _view_module_version: version,
        _model_module_version: version,


        name: '',
        data: [],
        // address_key: '0',
        // value_key: '1',
        // lng_key: '2',
        // lat_key: '3',
        themeField: '',
        symbolType: '',
        symbolSetting: {}
    })
})

var SuperMapMapModel = leaflet.LeafletMapModel.extend({
    defaults: _.extend({}, leaflet.LeafletMapModel.prototype.defaults, {
        _view_name: 'SuperMapMapView',
        _model_name: 'SuperMapMapModel',
        _view_module: 'iclientpy',
        _model_module: 'iclientpy',
        _view_module_version: version,
        _model_module_version: version,
        crs: ''
    })
})

module.exports = _.extend({}, leaflet, {
    SuperMapRankSymbolThemeLayerView: SuperMapRankSymbolThemeLayerView,
    SuperMapCloudTileLayerView: SuperMapCloudTileLayerView,
    SuperMapTileMapLayerView: SuperMapTileMapLayerView,
    SuperMapMapView: SuperMapMapView,

    SuperMapRankSymbolThemeLayerModel: SuperMapRankSymbolThemeLayerModel,
    SuperMapCloudTileLayerModel: SuperMapCloudTileLayerModel,
    SuperMapTileMapLayerModel: SuperMapTileMapLayerModel,
    SuperMapMapModel: SuperMapMapModel
})



