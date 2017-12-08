var leaflet = require('jupyter-leaflet')
var _ = require('underscore')
var version = require('../package.json').version
import L from 'leaflet'
require('leaflet.heat')
require('@supermap/iclient-leaflet')
var mapv = require('mapv')

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
        var symbolType = this.model.get('symbol_type')

        var options = this.get_options();
        if (!options.attribution) {
            delete options.attribution;
        }
        this.obj = L.supermap.rankSymbolThemeLayer(name, SuperMap.ChartType[symbolType], options);
        this.obj.addTo(this.map_view.obj);
        this.add_fetures()
    },

    add_fetures: function () {
        var symbolSetting = this.model.get('symbol_setting');
        var themeField = this.model.get('theme_field');
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
            var geo = this.map_view.obj.options.crs.project(L.latLng(data[i][lat_key], data[i][lng_key]));
            var attrs = { NAME: data[i][address_key] };
            attrs[themeField] = data[i][value_key]
            var feature = L.supermap.themeFeature(geo, attrs);
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

var SuperMapHeatLayerView = leaflet.LeafletLayerView.extend({
    create_obj: function () {
        var heatPoints = this.model.get('heat_points');
        var options = this.get_options();
        if (!options.gradient || this.isNull(options.gradient)) {
            delete options.gradient;
        }
        this.obj = L.heatLayer(heatPoints, options)
    },

    isNull: function (obj) {
        for (var name in obj) {
            return false;
        }
        return true;
    },

    refresh: function () {
        var options = this.get_options();
        if (!options.gradient || this.isNull(options.gradient)) {
            delete options.gradient;
        }
        this.obj.setOptions(options);
        this.obj.redraw();
    },

    model_events: function () {
        this.listenTo(this.model, 'change:radius', function () {
            this.refresh();
        }, this);
        this.listenTo(this.model, 'change:min_opacity', function () {
            this.refresh();
        }, this);
        this.listenTo(this.model, 'change:blur', function () {
            this.refresh();
        }, this);
        this.listenTo(this.model, 'change:max', function () {
            this.refresh();
        }, this);
    }
})

var SuperMapMapVLayerView = leaflet.LeafletLayerView.extend({
    create_obj: function () {
        var dataSet = this.model.get('data_set');
        var options = this.get_options();
        if (!options.gradient || this.isNull(options.gradient)) {
            delete options.gradient;
        }
        var mapvDataSet = new mapv.DataSet(dataSet);
        this.obj = L.supermap.mapVLayer(mapvDataSet, options)
    },

    isNull: function (obj) {
        for (var name in obj) {
            return false;
        }
        return true;
    },
})

var SuperMapMapView = leaflet.LeafletMapView.extend({
    create_obj: function () {
        var that = this;
        var options = this.get_options();
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
        map_name: '',
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
        theme_field: '',
        symbol_type: '',
        symbol_setting: {}
    })
})

var SuperMapMapVLayerModel = leaflet.LeafletLayerModel.extend({
    defaults: _.extend({}, leaflet.LeafletLayerModel.defaults, {
        _view_name: "SuperMapMapVLayerView",
        _model_name: "SuperMapMapVLayerModel",
        _view_module: 'iclientpy',
        _model_module: 'iclientpy',
        _view_module_version: version,
        _model_module_version: version,


        data_set: [],
        fill_style: '',
        shadow_color: '',
        shadow_blur: 0,
        max: 1,
        size: 1,
        label: {},
        global_alpha: 0.0,
        gradient: {},
        draw: ''
    })
})

var SuperMapHeatLayerModel = leaflet.LeafletLayerModel.extend({
    defaults: _.extend({}, leaflet.LeafletLayerModel.defaults, {
        _view_name: "SuperMapHeatLayerView",
        _model_name: "SuperMapHeatLayerModel",
        _view_module: 'iclientpy',
        _model_module: 'iclientpy',
        _view_module_version: version,
        _model_module_version: version,

        radius: 0,
        min_opacity: 0.5,
        heat_points: []
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
    SuperMapHeatLayerView: SuperMapHeatLayerView,
    SuperMapMapVLayerView: SuperMapMapVLayerView,
    SuperMapMapView: SuperMapMapView,

    SuperMapRankSymbolThemeLayerModel: SuperMapRankSymbolThemeLayerModel,
    SuperMapCloudTileLayerModel: SuperMapCloudTileLayerModel,
    SuperMapTileMapLayerModel: SuperMapTileMapLayerModel,
    SuperMapHeatLayerModel: SuperMapHeatLayerModel,
    SuperMapMapVLayerModel: SuperMapMapVLayerModel,
    SuperMapMapModel: SuperMapMapModel
})



