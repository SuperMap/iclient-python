from unittest import TestCase
from iclientpy.codingui.distributedanalyst._aggregate import PreparingAggregate, SummaryAnalystType, DistanceUnit
from iclientpy.rest.api.distributedanalyst import DistributedAnalyst

class AggregatePointsJobBuilderTest(TestCase):
    def test(self):
        distributedanalyst = DistributedAnalyst()
        builder = PreparingAggregate('s_processing_newyorkPoint_P', ['medallion', 'hack_license', 'vecdor_id', 'rate_code', 'store_and_fwd_flag', 'pickup_datetime', 'dropoff_datetime', 'passenger_count', 'trip_time_in_secs', 'trip_distance', 'pickup_longitude', 'pickup_latitude', 'dropoff_longitude', 'dropoff_latitude'], ['s_processing_newyorkZone_R', 's_processing_singleRegion_R'], distributedanalyst)
        self.assertEqual(builder.job_setting.input.datasetName, 's_processing_newyorkPoint_P')

        builder.set_numeric_precision(2)
        self.assertEqual(builder.job_setting.analyst.mappingParameters.numericPrecision, 2)

        builder.prepare_summarymesh.mesh_sieze_units.Kilometer.select()
        self.assertEqual(builder.job_setting.type, SummaryAnalystType.SUMMARYMESH)
        self.assertEqual(builder.job_setting.analyst.meshSizeUnit, DistanceUnit.Kilometer)

        builder.prepare_summarymesh.set_bounds((-180, -90, 180, 90))
        self.assertEqual(builder.job_setting.analyst.query, '-180,-90,180,90')

        builder.prepare_summarymesh.set_mesh_hexagon()
        self.assertEqual(builder.job_setting.analyst.meshType, 1)

        builder.prepare_summarymesh.set_mesh_square()
        self.assertEqual(builder.job_setting.analyst.meshType, 0)

        builder.prepare_summarymesh.set_resolution(100)
        self.assertEqual(builder.job_setting.analyst.resolution, 100)

        builder.prepare_summaryregion.available_region_datasets.s_processing_newyorkZone_R.select()
        self.assertEqual(builder.job_setting.type, SummaryAnalystType.SUMMARYREGION)
        self.assertEqual(builder.job_setting.analyst.regionDataset, 's_processing_newyorkZone_R')

