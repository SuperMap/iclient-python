import ipywidgets as widgets
# from ipywidgets import register
from ipywidgets import Layout
from ipywidgets import DOMWidget
from ipywidgets import Widget
from ipywidgets import widget_serialization
# from ipywidgets import interactive
# from ipywidgets import Box
from traitlets import Unicode
from traitlets import default
from traitlets import Bool
from traitlets import List
from traitlets import observe
from traitlets import Tuple
from traitlets import Instance
from traitlets import validate
from traitlets import Float
from traitlets import Type
from traitlets import link


# from traitlets import Integer


# class InteractMixin(object):
#     def interact(self, **kwargs):
#         c = []
#         for name, abbrev in kwargs.items():
#             default = getattr(self, name)
#             widget = interactive.widget_from_abbrev(abbrev, default)
#             if not widget.description:
#                 widget.description = name
#             widget.link = link((widget, 'value'), (self, name))
#             c.append(widget)
#         cont = Box(children=c)
#         return cont


class Layer(Widget):
    """
    :type _map: Map
    """
    _view_name = Unicode("SuperMapLayerView").tag(sync=True)
    _model_name = Unicode("SuperMapLayerModel").tag(sync=True)
    _view_module = Unicode("iclientpy").tag(sync=True)
    _model_module = Unicode("iclientpy").tag(sync=True)
    _view_module_version = Unicode('^0.1.0').tag(sync=True)
    _model_module_version = Unicode('^0.1.0').tag(sync=True)

    _map = None
    options = List(trait=Unicode).tag(sync=True)

    @default("options")
    def _default_options(self):
        return [name for name in self.traits(o=True)]

    visibility = Bool(False).tag(sync=True)

    @observe('visibility')
    def _update_visibility(self, change):
        old = change['old']
        new = change['new']
        if self._map is None:
            raise Exception("no map")
        else:
            if not old and new:
                if self.model_id not in self._map.layer_ids:
                    self._map.add_layer(self)
            elif old and not new:
                if self.model_id in self._map.layer_ids:
                    self._map.remove_layer(self)


class Icon(Widget):
    _view_name = Unicode("SuperMapIconView").tag(sync=True)
    _model_name = Unicode("SuperMapIconModel").tag(sync=True)
    _view_module = Unicode("iclientpy").tag(sync=True)
    _model_module = Unicode("iclientpy").tag(sync=True)
    _view_module_version = Unicode('^0.1.0').tag(sync=True)
    _model_module_version = Unicode('^0.1.0').tag(sync=True)
    url = Unicode("").tag(sync=True)
    size = Tuple(trait=Float).tag(sync=True)
    offset = Tuple(trait=Float).tag(sync=True)


class Marker(Widget):
    _view_name = Unicode("SuperMapMarkerView").tag(sync=True)
    _model_name = Unicode("SuperMapMarkerModel").tag(sync=True)
    _view_module = Unicode("iclientpy").tag(sync=True)
    _model_module = Unicode("iclientpy").tag(sync=True)
    _view_module_version = Unicode('^0.1.0').tag(sync=True)
    _model_module_version = Unicode('^0.1.0').tag(sync=True)

    lonlat = Tuple(trait=Float).tag(sync=True)
    icon = Instance(klass=Icon).tag(sync=True, **widget_serialization)

    @default("icon")
    def _default_keys(self):
        return Icon()


class Markers(Layer):
    _view_name = Unicode("SuperMapMarkersView").tag(sync=True)
    _model_name = Unicode("SuperMapMarkersModel").tag(sync=True)

    is_base_layer = Bool(False).tag(sync=True)
    opacity = Float(default_value=1).tag(sync=True)

    @validate("opacity")
    def _validate_opacity(self, proposal):
        return proposal['value']

    markers = Tuple(trait=Instance(Marker)).tag(sync=True, **widget_serialization)
    marker_ids = List()

    @validate('markers')
    def _validate_markers(self, proposal):
        self.marker_ids = [m.model_id for m in proposal['value']]
        # if (len(set(self.marker_ids)) != len(self.marker_ids)):
        #     raise Exception("duplicate marker detected ")
        return proposal['value']

    def add_marker(self, marker):
        """
        :param marker:
        :return:
        :type marker:Marker
        """
        if (marker.model_id in self.marker_ids):
            raise Exception('marker exist')
        self.markers = tuple([m for m in self.markers] + [marker])

    def remove_marker(self, marker):
        """
        :param marker:
        :return:
        :type marker:Marker
        """
        if (marker.model_id not in self.marker_ids):
            raise Exception('marker not exist')
        self.markers = tuple([m for m in self.markers if marker.model_id != m.model_id])

    def remove_markers(self):
        self.markers = ()


# @register
class Map(DOMWidget):
    @default('layout')
    def _default_layout(self):
        return Layout(height='400px', align_self='stretch')

    _view_name = Unicode('SuperMapMapView').tag(sync=True)
    _model_name = Unicode('SuperMapMapModel').tag(sync=True)
    _view_module = Unicode('iclientpy').tag(sync=True)
    _model_module = Unicode('iclientpy').tag(sync=True)
    _view_module_version = Unicode('^0.1.0').tag(sync=True)
    _model_module_version = Unicode('^0.1.0').tag(sync=True)

    # center = List(trait=Float).tag(sync=True)

    layers = Tuple(trait=Instance(Layer)).tag(sync=True, **widget_serialization)
    layer_ids = List()

    @validate('layers')
    def _validate_layers(self, proposal):
        self.layer_ids = [l.model_id for l in proposal['value']]
        # if len(set(self.layer_ids) != len(self.layer_ids)):
        #     raise Exception('duplicate layer detected')
        return proposal['value']

    def add_layer(self, layer):
        """
        :param layer:
        :return:
        :type layer:Layer
        """
        if layer.model_id in self.layer_ids:
            raise Exception("layer exist")
        layer._map = self
        self.layers = tuple([l for l in self.layers] + [layer])
        layer.visibility = True

    def remove_layer(self, layer):
        """
        :param layer:
        :return:
        :type layer:Layer
        """
        if layer.model_id not in self.layer_ids:
            raise Exception("layer not exist")
        self.layers = tuple([l for l in self.layers if l.model_id != layer.model_id])
        layer.visibility = False

    def clear_layers(self):
        self.layers = ()

    def __iadd__(self, other):
        if isinstance(other, Layer):
            self.add_layer(other)

    def __add__(self, other):
        if isinstance(other, Layer):
            self.add_layer(other)

    def __isub__(self, other):
        if isinstance(other, Layer):
            self.add_layer(other)
