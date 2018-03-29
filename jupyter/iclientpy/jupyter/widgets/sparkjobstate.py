from ipywidgets import DOMWidget, VBox, Text
import datetime as dt
from iclientpy.rest.api.model import SparkJobState


class SparkJobStateWidgets(DOMWidget):
    runstate_widget = Text(value='0', description='任务状态：', disabled=True)
    start_time_widget = Text(value='0', description='开始时间：', disabled=True)
    elspsed_time_widget = Text(value='0', description='持续时间(s)：', disabled=True)
    publisherelapsed_time_widget = Text(value='0', description='发布耗时(s)：', disabled=True)
    end_time_widget = Text(value='0', description='结束时间：', disabled=True)

    vbox = VBox(
        [runstate_widget, start_time_widget, elspsed_time_widget, publisherelapsed_time_widget, end_time_widget])

    def update(self, state: SparkJobState):
        self.runstate_widget.value = state.runState.value
        self.start_time_widget.value = dt.datetime.fromtimestamp(int(state.startTime / 1000)).strftime(
            '%Y-%m-%d %H:%M:%S')
        self.elspsed_time_widget.value = str(int(state.elapsedTime / 1000))
        self.publisherelapsed_time_widget.value = str(int(state.publisherelapsedTime / 1000))
        self.end_time_widget.value = dt.datetime.fromtimestamp(int(state.endTime / 1000)).strftime('%Y-%m-%d %H:%M:%S')

    def _ipython_display_(self, **kwargs):
        self.vbox._ipython_display_(**kwargs)
