from ipywidgets import DOMWidget, VBox, Text
from iclientpy.rest.api.model import SparkJobState


class SparkJobStateWidgets(DOMWidget):

    runstate_widget = Text(value='0', description='任务状态：', disabled=True)
    start_time_widget = Text(value='0', description='开始时间：', disabled=True)
    elspsed_time_widget = Text(value='0', description='经过时间：', disabled=True)
    publisherelapsed_time_widget = Text(value='0', description='发布耗时：', disabled=True)
    end_time_widget = Text(value='0', description='结束时间：', disabled=True)

    vbox = VBox([runstate_widget, start_time_widget, elspsed_time_widget, publisherelapsed_time_widget, end_time_widget])

    def update(self, state: SparkJobState):
        self.runstate_widget.value = state.runState.value
        self.start_time_widget.value = str(state.startTime)
        self.elspsed_time_widget.value = str(state.elapsedTime)
        self.publisherelapsed_time_widget.value = str(state.publisherelapsedTime)
        self.end_time_widget.value = str(state.endTime)

    def _ipython_display_(self, **kwargs):
        self.vbox._ipython_display_(**kwargs)


