from ipyleaflet import Layer
from ipywidgets import IntSlider, FloatSlider, VBox, Layout, ColorPicker
from traitlets import Unicode, List, Int, Float, Dict, Bool, validate, link, default, CaselessStrEnum, Any
from iclientpy._version import EXTENSION_VERSION
from .basesetting import BaseSetting


class MapvOptions(BaseSetting):
    fill_style = Unicode(allow_none=True).tag(settings=True)
    shadow_color = Unicode(allow_none=True).tag(settings=True)
    shadow_blur = Int(35).tag(settings=True)
    size = Int(5).tag(settings=True)

    label_show = Bool(True).tag(label=True)
    label_fill_style = Unicode('True').tag(label=True)
    label = Any({}, allow_none=True).tag(settings=True)

    @default('label')
    def _default_label(self):
        tmp_label = {}
        for name in self.traits(label=True):
            v = getattr(self, name)
            if not v:
                continue
            tmp_label[name.lstrip("label_")] = v
        return tmp_label

    global_alpha = Float(1).tag(settings=True)

    @validate('global_alpha')
    def _validate_global_alpha(self, proposal):
        if (proposal['value'] > 1 or proposal['value'] < 0):
            raise Exception("透明度范围是0-1之间")
        return proposal['value']

    gradient = Dict(allow_none=True).tag(settings=True)
    draw = CaselessStrEnum(
        ["simple", "time", "heatmap", "grid", "honeycomb", "bubble", "intensity", "category", "choropleth", "text",
         "icon"], default_value="honeycomb").tag(settings=True)


class MapVLayer(Layer):
    _view_name = Unicode("SuperMapMapVLayerView").tag(sync=True)
    _model_name = Unicode("SuperMapMapVLayerModel").tag(sync=True)
    _view_module = Unicode("iclientpy").tag(sync=True)
    _model_module = Unicode("iclientpy").tag(sync=True)
    _view_module_version = Unicode(EXTENSION_VERSION).tag(sync=True)
    _model_module_version = Unicode(EXTENSION_VERSION).tag(sync=True)

    data_set = List([]).tag(sync=True)
    map_v_options = Any().tag(sync=True)

    @validate('map_v_options')
    def _validate_map_v_options(self, proposal):

        if isinstance(proposal['value'], MapvOptions):
            tmp_options = proposal['value'].get_settings()
        else:
            tmp_options = proposal['value']
        self.size = tmp_options['size'] if 'size' in tmp_options else 5
        self.global_alpha = tmp_options['globalAlpha'] if 'globalAlpha' in tmp_options else 1
        self.fill_style = tmp_options['fillStyle'] if 'fillStyle' in tmp_options else'#3732FA'
        self.shadow_color = tmp_options['shadowColor'] if 'shadowColor' in tmp_options else'#FFFA32'
        self.shadow_blur = tmp_options['shadowBlur'] if 'shadowBlur' in tmp_options else 35
        return tmp_options

    size = Int().tag(sync=True)
    global_alpha = Float().tag(sync=True)
    fill_style = Unicode('').tag(sync=True)
    shadow_color = Unicode('').tag(sync=True)
    shadow_blur = Int().tag(sync=True)

    def interact(self):
        sizeslider = IntSlider(value=self.size,
                               min=0,
                               max=100,
                               step=1,
                               description='大小:',
                               disabled=False,
                               continuous_update=False,
                               orientation='horizontal',
                               readout=True,
                               readout_format='d',
                               layout=Layout(width="350px"))
        link((sizeslider, 'value'), (self, 'size'))
        global_alpha_slider = FloatSlider(value=self.global_alpha,
                                          min=0,
                                          max=1.0,
                                          step=0.1,
                                          description='透明度:',
                                          disabled=False,
                                          continuous_update=False,
                                          orientation='horizontal',
                                          readout=True,
                                          readout_format='.1f',
                                          layout=Layout(width="350px"))
        link((global_alpha_slider, 'value'), (self, 'global_alpha'))
        fill_style_color = ColorPicker(concise=False,
                                       description='填充颜色：',
                                       value=self.fill_style,
                                       disabled=False,
                                       layout=Layout(width="350px"))
        link((fill_style_color, 'value'), (self, 'fill_style'))
        shadow_color_color = ColorPicker(concise=False,
                                         description='描边颜色：',
                                         value=self.shadow_color,
                                         disabled=False,
                                         layout=Layout(width="350px"))
        link((shadow_color_color, 'value'), (self, 'shadow_color'))
        shadow_blur_slider = IntSlider(value=self.shadow_blur,
                                       min=0,
                                       max=100,
                                       step=1,
                                       description='投影模糊级数:',
                                       disabled=False,
                                       continuous_update=False,
                                       orientation='horizontal',
                                       readout=True,
                                       readout_format='d',
                                       layout=Layout(width="350px"))
        link((shadow_blur_slider, 'value'), (self, 'shadow_blur'))

        return VBox([sizeslider, global_alpha_slider, shadow_color_color, fill_style_color, shadow_blur_slider])
