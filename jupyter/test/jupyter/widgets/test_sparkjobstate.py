from unittest import TestCase
from unittest.mock import MagicMock
from iclientpy.jupyter import SparkJobStateWidgets
from iclientpy.rest.api.model import SparkRunState, SparkJobState


class SparkJobStateTest(TestCase):
    def test_update(self):
        widget = SparkJobStateWidgets()
        state = SparkJobState()
        state.runState = SparkRunState.RUNNING
        state.startTime = 1
        state.elapsedTime = 10
        state.publisherelapsedTime = 3
        state.endTime = 11
        widget.update(state)
        self.assertEqual(widget.runstate_widget.value, 'RUNNING')
        self.assertEqual(widget.start_time_widget.value, '1')
        self.assertEqual(widget.elspsed_time_widget.value, '10')
        self.assertEqual(widget.publisherelapsed_time_widget.value, '3')
        self.assertEqual(widget.end_time_widget.value, '11')

    def test_ipytion_display(self):
        widget = SparkJobStateWidgets()
        mock_method = MagicMock()
        widget.vbox._ipython_display_ = mock_method
        widget._ipython_display_()
        mock_method.assert_called_once()
