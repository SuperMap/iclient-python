import math
from ipyleaflet import Layer
from ipywidgets import IntSlider, FloatSlider, VBox, Layout
from traitlets import Unicode, List, Int, Float, Dict, validate, link
from iclientpy._version import EXTENSION_VERSION


class HeatLayer(Layer):
    """
    热力图图层
    """
    _view_name = Unicode("SuperMapHeatLayerView").tag(sync=True)
    _model_name = Unicode("SuperMapHeatLayerModel").tag(sync=True)
    _view_module = Unicode("iclientpy").tag(sync=True)
    _model_module = Unicode("iclientpy").tag(sync=True)
    _view_module_version = Unicode(EXTENSION_VERSION).tag(sync=True)
    _model_module_version = Unicode(EXTENSION_VERSION).tag(sync=True)

    heat_points = List([]).tag(sync=True)  #:热力点数据

    @validate('heat_points')
    def _validate_heat_points(self, proposal):
        if (proposal['value'] is None):
            raise Exception("error data")
        self.max = max(dt[2] for dt in self.heat_points)
        return proposal['value']

    radius = Int(25).tag(sync=True, o=True)  #:半径
    min_opacity = Float(0.05).tag(sync=True, o=True)  #:最小透明度
    max_zoom = Int().tag(sync=True, o=True)  #:最大缩放程度
    max = Float(1.0).tag(sync=True, o=True)  #:最大值
    blur = Int(15).tag(sync=True, o=True)  #:模糊度
    gradient = Dict().tag(sync=True, o=True)  #:级别

    def interact(self):
        """
        获取交互式控制专题图样式部件
        """
        radiusintslider = IntSlider(value=self.radius,
                                    min=1,
                                    max=100,
                                    step=1,
                                    description='半径:',
                                    disabled=False,
                                    continuous_update=False,
                                    orientation='horizontal',
                                    readout=True,
                                    readout_format='d',
                                    layout=Layout(width="350px"))
        link((radiusintslider, 'value'), (self, 'radius'))
        minopacityslider = FloatSlider(value=self.min_opacity,
                                       min=0,
                                       max=1.0,
                                       step=0.05,
                                       description='透明度:',
                                       disabled=False,
                                       continuous_update=False,
                                       orientation='horizontal',
                                       readout=True,
                                       readout_format='.1f',
                                       layout=Layout(width="350px"))
        link((minopacityslider, 'value'), (self, 'min_opacity'))
        blurintslider = IntSlider(value=self.blur,
                                  min=1,
                                  max=100,
                                  step=1,
                                  description='模糊:',
                                  disabled=False,
                                  continuous_update=False,
                                  orientation='horizontal',
                                  readout=True,
                                  readout_format='d',
                                  layout=Layout(width="350px"))
        link((blurintslider, 'value'), (self, 'blur'))
        maxslider = IntSlider(value=1,
                              min=0,
                              max=math.ceil(self.max),
                              step=1,
                              description='max:',
                              disabled=False,
                              continuous_update=False,
                              orientation='horizontal',
                              readout=True,
                              readout_format='d',
                              layout=Layout(width="350px"))
        link((maxslider, 'value'), (self, 'max'))
        return VBox([radiusintslider, minopacityslider, blurintslider, maxslider])
