var leaflet = require('jupyter-leaflet')
var _ = require('underscore')
var version = require('../package.json').version
import { CRS, map, latLng } from 'leaflet'
import { cloudTileLayer, rankSymbolThemeLayer, tiledMapLayer, SuperMap, themeFeature } from '@supermap/iclient-leaflet'


var SuperMapCloudTileLayerView = leaflet.LeafletTileLayerView.extend({

    create_obj: function () {
        var url = this.model.get('url');
        var options = this.get_options();
        if (!options.attribution) {
            delete options.attribution;
        }
        this.obj = cloudTileLayer(url, options);
    },

})

var SuperMapTileMapLayerView = leaflet.LeafletTileLayerView.extend({
    create_obj: function () {
        var url = this.model.get('url')
        this.obj = tiledMapLayer(url)
    },
})

var SuperMapRankSymbolThemeLayerView = leaflet.LeafletLayerView.extend({
    create_obj: function () {
        var name = this.model.get('name');
        var symbolType = this.model.get('symbolType')

        var options = this.get_options();
        if (!options.attribution) {
            delete options.attribution;
        }

        this.obj = rankSymbolThemeLayer(name, SuperMap.ChartType[symbolType], options);
        this.obj.addTo(this.map_view.obj);
        this.add_fetures()
    },

    add_fetures: function () {
        var symbolSetting = this.model.get('symbolSetting');
        var themeField = this.model.get('themeField');
        this.obj.themeField = themeField;
        this.obj.symbolSetting = symbolSetting;
        this.obj.symbolSetting.codomain = this.model.get('codomain');
        var rrange = this.model.get('rrange');
        this.obj.symbolSetting.minR = rrange[0]
        this.obj.symbolSetting.maxR = rrange[1]
        this.obj.symbolSetting.fillColor = this.model.get('color')
        this.obj.clear();
        var data = this.model.get('data');
        var address_key = 0;
        var value_key = 1;
        var lng_key = 2;
        var lat_key = 3;
        var features = [];
        for (var i = 0, len = data.length; i < len; i++) {
            var geo = this.map_view.obj.options.crs.project(latLng(data[i][lat_key], data[i][lng_key]));
            var attrs = { NAME: data[i][address_key] };
            attrs[themeField] = data[i][value_key]
            var feature = themeFeature(geo, attrs);
            features.push(feature);
        }
        this.obj.addFeatures(features);
    },

    model_events: function () {
        this.listenTo(this.model, 'change:codomain', function () {
            this.add_fetures();
        }, this);
        this.listenTo(this.model, 'change:rrange', function () {
            this.add_fetures();
        }, this);
        this.listenTo(this.model, 'change:color', function () {
            this.add_fetures();
        }, this);
    }
})

var SuperMapMapView = leaflet.LeafletMapView.extend({
    create_obj: function () {
        var that = this;
        var options = this.get_options();
        options.crs = CRS[options.crs]
        that.obj = map(this.el, options);
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



