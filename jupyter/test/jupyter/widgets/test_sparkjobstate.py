from unittest import TestCase
from unittest.mock import MagicMock
from iclientpy.jupyter import SparkJobStateWidgets
from iclientpy.rest.api.model import SparkRunState, SparkJobState


class SparkJobStateTest(TestCase):
    def test_update(self):
        widget = SparkJobStateWidgets()
        state = SparkJobState()
        state.runState = SparkRunState.RUNNING
        state.startTime = 1522217321932
        state.elapsedTime = 142259
        state.publisherelapsedTime = 7889
        state.endTime = 1522217473360
        widget.update(state)
        self.assertEqual(widget.runstate_widget.value, 'RUNNING')
        self.assertEqual(widget.start_time_widget.value, '2018-03-28 14:08:41')
        self.assertEqual(widget.duration_widget.value, '150s')
        self.assertEqual(widget.end_time_widget.value, '2018-03-28 14:11:13')

    def test_update_with_zero_value(self):
        widget = SparkJobStateWidgets()
        state = SparkJobState()
        state.runState = SparkRunState.RUNNING
        state.startTime = 1522217321932
        state.elapsedTime = 0
        state.publisherelapsedTime = 0
        state.endTime = 0
        widget.update(state)
        self.assertEqual(widget.runstate_widget.value, 'RUNNING')
        self.assertEqual(widget.start_time_widget.value, '2018-03-28 14:08:41')
        self.assertEqual(widget.duration_widget.value, '***')
        self.assertEqual(widget.end_time_widget.value, '***')

    def test_ipytion_display(self):
        widget = SparkJobStateWidgets()
        mock_method = MagicMock()
        widget.vbox._ipython_display_ = mock_method
        widget._ipython_display_()
        mock_method.assert_called_once()
