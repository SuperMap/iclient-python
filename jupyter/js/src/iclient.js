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
        var address_field_index = this.model.get('address_field_index');
        var value_field_index = this.model.get('value_field_index');
        var lng_filed_index = this.model.get('lng_filed_index');
        var lat_filed_index = this.model.get('lat_filed_index');
        var options = this.get_options();
        if (!options.attribution) {
            delete options.attribution;
        }

        this.obj = L.supermap.rankSymbolThemeLayer(name, SuperMap.ChartType.CIRCLE, options);

        // 指定用于专题图制作的属性字段  详看下面 addThemeLayer（）中的feature.attrs.CON2009
        this.obj.themeField = "CON2009";

        // 配置图表参数
        this.obj.symbolSetting = {
            //允许图形展示的值域范围，此范围外的数据将不制作图图形,必设参数
            codomain: [0, 40000],
            //圆最大半径 默认100
            maxR: 100,
            //圆最小半径 默认0
            minR: 0,
            // 圆形样式
            circleStyle: { fillOpacity: 0.8 },
            // 符号专题图填充颜色
            fillColor: "#FFA500",
            // 专题图hover 样式
            circleHoverStyle: { fillOpacity: 1 }
        };
        this.obj.addTo(this.map_view.obj);
        // 注册专题图 mousemove, mouseout事件(注意：专题图图层对象自带 on 函数，没有 events 对象)
        // themeLayer.on("mousemove", showInfoWin);
        // themeLayer.on("mouseout", closeInfoWin);
        this.obj.clear();
        var features = [];
        for (var i = 0, len = data.length; i < len; i++) {
            var geo = this.map_view.obj.options.crs.project(L.latLng(data[i][lat_filed_index], data[i][lng_filed_index]));
            // var geo = L.point(data[i][lng_filed_index], data[i][lat_filed_index])
            var attrs = { NAME: data[i][address_field_index], CON2009: data[i][value_field_index] };
            var feature = L.supermap.themeFeature(geo, attrs);
            features.push(feature);
        }
        this.obj.addFeatures(features);
        // this.obj.redrawThematicFeatures();
    },
})

var SuperMapMapView = leaflet.LeafletMapView.extend({
    create_obj: function () {
        options = this.get_options()
        // options.crs = L.CRS.EPSG4326;
        this.obj = L.map(this.el, options);
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
        address_field_index: 0,
        value_field_index: 1,
        lng_filed_index: 2,
        lat_filed_index: 3,


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



