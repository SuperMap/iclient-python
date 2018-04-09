from ipywidgets import DOMWidget, VBox, Text, Layout
import datetime as dt
from iclientpy.rest.api.model import SparkJobState


class SparkJobStateWidgets(DOMWidget):
    runstate_widget = Text(value='0', description='任务状态：', disabled=True)
    start_time_widget = Text(value='0', description='开始时间：', disabled=True)
    duration_widget = Text(value='0', description='持续时间：', disabled=True)
    end_time_widget = Text(value='0', description='结束时间：', disabled=True)

    vbox = VBox(
        [runstate_widget, start_time_widget, duration_widget, end_time_widget])

    def update(self, state: SparkJobState):
        self.runstate_widget.value = state.runState.value
        self.start_time_widget.value = dt.datetime.fromtimestamp(int(state.startTime / 1000)).strftime(
            '%Y-%m-%d %H:%M:%S') if state.startTime != 0 else '***'
        self.duration_widget.value = str(
            int((state.elapsedTime + state.publisherelapsedTime) / 1000)) + 's' if state.elapsedTime != 0 else '***'
        self.end_time_widget.value = dt.datetime.fromtimestamp(int(state.endTime / 1000)).strftime(
            '%Y-%m-%d %H:%M:%S') if state.endTime != 0 else '***'

    def _ipython_display_(self, **kwargs):
        self.vbox._ipython_display_(**kwargs)
