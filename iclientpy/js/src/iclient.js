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
            var showinfowinbind = _.bind(this.showInfoWin, this)
            var closeinfowinbind = _.bind(this.closeInfoWin, this)
            this.obj.on("mousemove", showinfowinbind);
            this.obj.on("mouseout", closeinfowinbind);
            var mouseoverbind = _.bind(this.mouseover, this)
            this.map_view.obj.on("mousemove", mouseoverbind);
            this.add_fetures()
        },

        mouseover: function (e) {
            this.infowinPosition = e.layerPoint;
        },


        showInfoWin: function (e) {
            if (e.target && e.target.refDataID && e.target.dataInfo) {
                this.closeInfoWin()
                // 获取图形对应的数据 (feature)
                var fea = this.obj.getFeatureById(e.target.refDataID);
                if (!fea) {
                    return;
                }
                var info = e.target.dataInfo;
                // 弹窗内容
                var contentHTML = "<div style='color: #000; background-color: #fff'>";
                contentHTML += "<br><strong>" + fea.attributes.NAME + "</strong>";
                contentHTML += "<hr style='margin: 3px'>";
                switch (info.field) {
                    case this.model.get('theme_field'):
                        contentHTML += "<br/><strong>" + info.value + "</strong>";
                        break;
                    default:
                        contentHTML += "No Data";
                }
                contentHTML += "</div>";

                var latLng = this.map_view.obj.layerPointToLatLng(this.infowinPosition);
                if (!this.infowin) {
                    this.infowin = L.popup();
                }
                this.infowin.setLatLng(latLng);
                this.infowin.setContent(contentHTML);
                this.infowin.openOn(this.map_view.obj);


            }
        },

        closeInfoWin: function () {
            if (this.infowin) {
                try {
                    this.infowin.remove();
                } catch (e) {
                }
            }
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
                var attrs = {NAME: data[i][address_key]};
                attrs[themeField] = data[i][value_key]
                var feature = L.supermap.themeFeature(geo, attrs);
                features.push(feature);
            }
            this.obj.addFeatures(features);
        }
        ,

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
    }
)

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
        var mapvOptions = this.model.get('map_v_options')
        var mapvDataSet = new mapv.DataSet(dataSet);
        this.obj = L.supermap.mapVLayer(mapvDataSet, mapvOptions, options)
    },

    refresh: function () {
        var mapvOptions = this.model.get('map_v_options')
        mapvOptions.size = this.model.get('size');
        mapvOptions.globalAlpha = this.model.get('global_alpha');
        mapvOptions.fillStyle = this.model.get('fill_style');
        mapvOptions.shadowColor = this.model.get('shadow_color');
        mapvOptions.shadowBlur = this.model.get('shadow_blur');
        // mapvOptions.lineWidth = this.model.get('line_width');
        var dataSet = this.model.get('data_set');
        var mapvDataSet = new mapv.DataSet(dataSet);
        this.obj.update({data: mapvDataSet, options: mapvOptions})
    },

    model_events: function () {
        this.listenTo(this.model, 'change:size', function () {
            this.refresh();
        }, this);
        this.listenTo(this.model, 'change:global_alpha', function () {
            this.refresh();
        }, this);
        this.listenTo(this.model, 'change:fill_style', function () {
            this.refresh();
        }, this);
        this.listenTo(this.model, 'change:shadow_color', function () {
            this.refresh();
        }, this);
        this.listenTo(this.model, 'change:shadow_blur', function () {
            this.refresh();
        }, this);
        // this.listenTo(this.model, 'change:line_width', function () {
        //     this.refresh();
        // }, this);
    },

})

var SuperMapEchartsLayerView = leaflet.LeafletLayerView.extend({
    create_obj: function () {
        var options = this.model.get('option');
        this.obj = L.supermap.echartsLayer(options);
    }
})

var SuperMapMapView = leaflet.LeafletMapView.extend({
    create_obj: function () {
        var that = this;
        var options = this.get_options();
        options.crs = L.CRS[options.crs]
        that.obj = L.map(this.el, options);
        var fit_bounds = that.model.get('fit_bounds')
        if (fit_bounds.length === 2) {
            that.obj.fitBounds(fit_bounds);
            that.update_bounds();
            this.model.set('zoom', that.obj.getZoom());
        }
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
        size: 1,
        global_alpha: 0.0,
        fill_style: '',
        shadow_color: '',
        shadow_blur: 0,
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

var SuperMapEchartsLayerModel = leaflet.LeafletLayerModel.extend({
    defaults: _.extend({}, leaflet.LeafletLayerModel.prototype.defaults, {
        _view_name: 'SuperMapEchartsLayerView',
        _model_name: 'SuperMapEchartsLayerModel',
        _view_module: 'iclientpy',
        _model_module: 'iclientpy',
        _view_module_version: version,
        _model_module_version: version,
        option: {}
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
    SuperMapEchartsLayerView: SuperMapEchartsLayerView,
    SuperMapMapView: SuperMapMapView,

    SuperMapRankSymbolThemeLayerModel: SuperMapRankSymbolThemeLayerModel,
    SuperMapCloudTileLayerModel: SuperMapCloudTileLayerModel,
    SuperMapTileMapLayerModel: SuperMapTileMapLayerModel,
    SuperMapHeatLayerModel: SuperMapHeatLayerModel,
    SuperMapMapVLayerModel: SuperMapMapVLayerModel,
    SuperMapEchartsLayerModel: SuperMapEchartsLayerModel,
    SuperMapMapModel: SuperMapMapModel
})



