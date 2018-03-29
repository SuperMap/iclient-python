from ipywidgets import DOMWidget, Label, VBox, Text
from IPython.display import display
from traitlets import Unicode
from iclientpy.rest.api.model import SparkJobState, SparkRunState
import time


class SparkJobStateWidgets(DOMWidget):
    runstate = Unicode('UNKNOWN').tag(sync=True)
    starttime = Unicode('0').tag(sync=True)
    elspsedtime = Unicode('0').tag(sync=True)
    publisherelapsed_time = Unicode('0').tag(sync=True)
    endtime = Unicode('0').tag(sync=True)

    runstate_widget = Text(value='0', description='任务状态：', disabled=True)
    start_time_widget = Text(value='0', description='开始时间：', disabled=True)
    elspsed_time_widget = Text(value='0', description='经过时间：', disabled=True)
    publisherelapsed_time_widget = Text(value='0', description='发布耗时：', disabled=True)
    end_time_time = Text(value='0', description='结束时间：', disabled=True)

    vbox = VBox([runstate_widget, start_time_widget, elspsed_time_widget, publisherelapsed_time_widget, end_time_time])

    def update(self, state: SparkJobState):
        self.runstate = state.runState.value
        self.starttime = str(state.startTime)
        self.elspsedtime = str(state.elapsedTime)
        self.publisherelapsed_time = str(state.publisherelapsedTime)
        self.endtime = str(state.endTime)

        self.runstate_widget.value = state.runState.value
        self.start_time_widget.value = str(state.startTime)
        self.elspsed_time_widget.value = str(state.elapsedTime)
        self.publisherelapsed_time_widget.value = str(state.publisherelapsedTime)
        self.end_time_time.value = str(state.endTime)

    def _ipython_display_(self, **kwargs):
        self.vbox._ipython_display_(**kwargs)
