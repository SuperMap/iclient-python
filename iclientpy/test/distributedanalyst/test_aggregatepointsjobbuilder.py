from unittest import TestCase
from unittest.mock import MagicMock
from iclientpy.codingui.distributedanalyst._aggregate import SummaryRegion, SummaryAnalystType, DistanceUnit, SummaryMesh


class AggregatePointsJobBuilderTest(TestCase):

    def test_summary_mesh(self):
        executor = MagicMock()
        builder = SummaryMesh('s_processing_newyorkPoint_P', ['medallion', 'hack_license', 'vecdor_id', 'rate_code', 'store_and_fwd_flag', 'pickup_datetime', 'dropoff_datetime', 'passenger_count', 'trip_time_in_secs', 'trip_distance', 'pickup_longitude', 'pickup_latitude', 'dropoff_longitude', 'dropoff_latitude'], executor)
        self.assertEqual(builder.job_setting.input.datasetName, 's_processing_newyorkPoint_P')

        builder.set_numeric_precision(2)
        self.assertEqual(builder.job_setting.analyst.mappingParameters.numericPrecision, 2)

        builder.available_mesh_sieze_units.Kilometer.select()
        self.assertEqual(builder.job_setting.type, SummaryAnalystType.SUMMARYMESH)
        self.assertEqual(builder.job_setting.analyst.meshSizeUnit, DistanceUnit.Kilometer)

        builder.set_bounds((-180, -90, 180, 90))
        self.assertEqual(builder.job_setting.analyst.query, '-180,-90,180,90')

        builder.set_mesh_hexagon()
        self.assertEqual(builder.job_setting.analyst.meshType, 1)

        builder.set_mesh_square()
        self.assertEqual(builder.job_setting.analyst.meshType, 0)

        builder.set_resolution(100)
        self.assertEqual(builder.job_setting.analyst.resolution, 100)

        self.assertEqual(builder.job_setting.type, SummaryAnalystType.SUMMARYMESH)

        builder.execute()
        executor.assert_called_once()

    def test_summary_region(self):
        executor = MagicMock()
        builder = SummaryRegion('s_processing_newyorkPoint_P', ['medallion', 'hack_license', 'vecdor_id', 'rate_code', 'store_and_fwd_flag', 'pickup_datetime', 'dropoff_datetime', 'passenger_count', 'trip_time_in_secs', 'trip_distance', 'pickup_longitude', 'pickup_latitude', 'dropoff_longitude', 'dropoff_latitude'], ['s_processing_newyorkZone_R', 's_processing_singleRegion_R'], executor)
        self.assertEqual(builder.job_setting.input.datasetName, 's_processing_newyorkPoint_P')

        builder.set_numeric_precision(2)
        self.assertEqual(builder.job_setting.analyst.mappingParameters.numericPrecision, 2)

        builder.available_region_datasets.s_processing_newyorkZone_R.select()
        self.assertEqual(builder.job_setting.analyst.regionDataset, 's_processing_newyorkZone_R')
        self.assertEqual(builder.job_setting.type, SummaryAnalystType.SUMMARYREGION)
        builder.execute()
        executor.assert_called_once()

