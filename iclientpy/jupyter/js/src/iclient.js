var widgets = require('@jupyter-widgets/base');
var _ = require('lodash');
var SuperMap = require('./SuperMap')

function camel_case(input) {
    // Convert from foo_bar to fooBar
    return input.toLowerCase().replace(/_(.)/g, function (match, group1) {
        return group1.toUpperCase();
    });
}

var SuperMapIconView = widgets.WidgetView.extend({

    initialize: function (parameters) {
        SuperMapIconView.__super__.initialize.apply(this, arguments);
    },

    render: function () {
        this.create_obj();
    },

    create_obj: function () {
        var url = this.model.get("url")
        var size = SuperMap.Size(44, 33);
        var offset = new SuperMap.Pixel(-(size.w / 2), -size.h);
        this.obj = new SuperMap.Icon(url, size, offset);
    }


})

var SuperMapIconModel = widgets.WidgetModel.extend({
    defaults: _.extend({}, widgets.WidgetModel.prototype.defaults, {
        _view_name: 'SuperMapIconView',
        _model_name: 'SuperMapIconModel',
        _view_module: 'iclientpy',
        _model_module: 'iclientpy',
        url: '',
        size: [0.0, 0.0],
        offset: [0.0, 0.0]
    })
})

var SuperMapLayerView = widgets.WidgetView.extend({
    initialize: function (parameters) {
        SuperMapLayerView.__super__.initialize.apply(this, arguments);
        this.map_view = this.options.map_view;
    },

    render: function () {
        this.create_obj()
    },

    get_options: function () {
        var o = this.model.get('options');
        var options = {};
        var key;
        for (var i = 0; i < o.length; i++) {
            key = o[i];
            options[camel_case(key)] = this.model.get(key);
        }
        return options;
    }
})

var SuperMapLayerModel = widgets.WidgetModel.extend({
    defaults: _.extend({}, widgets.WidgetModel.prototype.defaults, {
        _view_name: 'SuperMapLayerView',
        _model_name: 'SuperMapLayerModel',
        _view_module: 'iclientpy',
        _model_module: 'iclientpy',
        options: []
    })
})


var SuperMapIconView = widgets.WidgetView.extend({
    initialize: function (parameters) {
        SuperMapLayerView.__super__.initialize.apply(this, arguments);
    },

    render: function () {
        this.create_obj()
    },

    create_obj: function () {
        var url = this.model.get('url');
        var size = this.model.get('size');
        var offset = this.model.get('offset');
        var sSize = new SuperMap.Size(size[0], size[1]);
        var sPixel = new SuperMap.Pixel(-(sSize.w / 2), -sSize.h);
        this.obj = new SuperMap.Icon(url, sSize, sPixel);
    }

})

SuperMapIconModel = widgets.WidgetModel.extend({
    defaults: _.extend({}, widgets.WidgetModel.prototype.defaults, {
        _view_name: 'SuperMapIconView',
        _model_name: 'SuperMapIconModel',
        _view_module: 'iclientpy',
        _model_module: 'iclientpy',
        url: '',
        size: [],
        offset: []
    })
})

var SuperMapMarkerView = widgets.WidgetView.extend({
    initialize: function (parameters) {
        SuperMapMarkerView.__super__.initialize.apply(this, arguments);
    },

    render: function () {
        this.create_obj()
    },

    create_obj: function () {
        var icon = this.model.get('icon');
        var lonlat = this.model.get('lonlat');
        this.obj = new SuperMap.Marker(new SuperMap.LonLat(lonlat[0], lonlat[1]), icon.obj)
    }

}, {
    serializers: _.extend({
        icon: {deserialize: widgets.unpack_models}
    }, widgets.DOMWidgetModel.serializers)
})

var SuperMapMarkerModel = widgets.WidgetModel.extend({
    defaults: _.extend({}, widgets.WidgetModel.prototype.defaults, {
        _view_name: 'SuperMapMarkerView',
        _model_name: 'SuperMapMarkerModel',
        _view_module: 'iclientpy',
        _model_module: 'iclientpy',
        lonlat: [],
        icon: {}
    })
})


var SuperMapMarkersView = SuperMapLayerView.extend({

    remove_marker_view: function (child_view) {
        this.obj.removeMarker(child_view.obj);
        child_view.remove();
    },

    add_marker_model: function (child_model) {
        var that = this;
        return this.create_child_view(child_model, {
            marker_view: this
        }).then(function (child_view) {
            that.obj.addMarker(child_view.obj);
            return child_view;
        });
    },

    render: function () {
        this.marker_views = new widgets.ViewList(this.add_marker_model, this.remove_marker_view, this);
        this.render_markers();
    },

    render_markers: function () {
        this.create_obj();
        this.marker_views.update(this.model.get('markers'));
    },

    create_obj: function () {
        this.obj = new SuperMap.Layer.Markers("Markers", this.get_options());
    }
}, {
    serializers: _.extend({
        markers: {deserialize: widgets.unpack_models}
    }, widgets.DOMWidgetModel.serializers)
})

var SuperMapMarkersModel = SuperMapLayerModel.extend({
    defaults: _.extend({}, SuperMapLayerModel.prototype.defaults, {
        _view_name: 'SuperMapMarkersView',
        _model_name: 'SuperMapMarkersModel',
        markers: [],
        is_base_layer: false,
        opacity: 1
    })
}, {
    serializers: _.extend({
        markers: {deserialize: widgets.unpack_models}
    }, widgets.DOMWidgetModel.serializers)
})

var SuperMapMapView = widgets.DOMWidgetView.extend({
    initialize: function (parameters) {
        SuperMapMapView.__super__.initialize.apply(this, arguments);
    },

    remove_layer_view: function (child_view) {
        this.obj.removeLayer(child_view.obj);
        child_view.remove();
    },

    add_layer_model: function (child_model) {
        var that = this;
        return this.create_child_view(child_model, {
            map_view: this
        }).then(function (child_view) {
            that.obj.addLayer(child_view.obj);
            return child_view;
        });
    },

    render: function () {
        this.el.style['width'] = this.model.get('width');
        this.el.style['height'] = this.model.get('height');
        this.layer_views = new widgets.ViewList(this.add_layer_model, this.remove_layer_view, this);
        this.displayed.then(_.bind(this.render_map, this));
    },

    render_map: function () {
        this.obj = new SuperMap.Map(this.el, {
            controls: [
                new SuperMap.Control.ScaleLine(),
                new SuperMap.Control.LayerSwitcher(),
                new SuperMap.Control.Zoom(),
                new SuperMap.Control.Navigation({
                    dragPanOptions: {
                        enableKinetic: true
                    }
                })
            ]
        });

        var layer = new SuperMap.Layer.CloudLayer();

        this.obj.addLayers([layer]);

        this.obj.setCenter(new SuperMap.LonLat(11339634.286396, 4588716.5813769), 4);

        this.layer_views.update(this.model.get('layers'))
    }
})


var SuperMapMapModel = widgets.DOMWidgetModel.extend({
    defaults: _.extend({}, widgets.DOMWidgetModel.prototype.defaults, {
        _view_name: "SuperMapMapView",
        _model_name: "SuperMapMapModel",
        _view_module: "iclientpy",
        _model_module: "iclientpy",

        width: "600px",
        height: "400px",
        // center: [0.0, 0.0],
        layers: []
    })
}, {
    serializers: _.extend({
        layers: {deserialize: widgets.unpack_models}
    }, widgets.DOMWidgetModel.serializers)
})

module.exports = {
    SuperMapIconView: SuperMapIconView,
    SuperMapIconModel: SuperMapIconModel,
    SuperMapMarkerView: SuperMapMarkerView,
    SuperMapMarkerModel: SuperMapMarkerModel,
    SuperMapLayerView: SuperMapLayerView,
    SuperMapLayerModel: SuperMapLayerModel,
    SuperMapMarkersView: SuperMapMarkersView,
    SuperMapMarkersModel: SuperMapMarkersModel,
    SuperMapMapView: SuperMapMapView,
    SuperMapMapModel: SuperMapMapModel,
};