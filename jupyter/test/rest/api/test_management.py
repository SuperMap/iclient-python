import httpretty
from unittest import mock
from iclientpy.rest.api.management import *
from iclientpy.rest.decorator import HttpMethod
from iclientpy.rest.api.management import PostTileJobsItem, TileSize, OutputFormat, TileType, TileSourceInfo
from .abstractrest import AbstractRESTTestCase


class ManagementTest(AbstractRESTTestCase):
    @classmethod
    def setUpClass(cls):
        cls.init_rest(cls)
        cls.init_apifactory(cls)
        cls.init_api(cls, "management")

    def test_workspace(self):
        {}.should
        param = PostWorkspaceParameter()
        param.workspaceConnectionInfo = 'World.sxwu'
        param.servicesTypes = [ServiceType.RESTMAP]
        self.check_api('post_workspaces', self.baseuri + "/manager/workspaces.json", HttpMethod.POST,
                       httpretty.Response(body='[{"serviceType": "RESTMAP", "serviceAddress": "123"}]', status=201),
                       param=param)

        self.check_api('get_workspaces', self.baseuri + "/manager/workspaces.json", HttpMethod.GET,
                       httpretty.Response(
                           body='[{"address": "/etc/icloud/World/World.sxwu","enabled": true,"name": "World.sxwu","serviceName": "map-World/rest","serviceType": "MapService"}]',
                           status=201),
                       param=param)

    def test_tilejobs(self):
        body = '{"postResultType":"CreateChild","newResourceID":"d7bff309-8f7f-48bb-9c4f-bf9b9224fb41","succeed":true,"customResult":{"id":"d7bff309-8f7f-48bb-9c4f-bf9b9224fb41","state":null,"targetTilesetInfo":{"filePath":"/etc/icloud/SuperMapiServer/webapps/iserver/output/sqlite/World_1152242556_256X256_PNG.smtiles","name":"smtiles_tileset_1596041633"},"info":{"originalPoint":{"x":-180,"y":90},"fileVerificationMode":"FILESIZE","cacheRegions":null,"utfGridParameter":null,"resolutions":[1.4062499999999996,0.7041106029214795,0.35205530146073977,0.17602765073036988,0.08801382536518494,0.04400691268259247,0.022003456341296235,0.011001728170648107,0.005500864085324063,0.002750432042662044],"dataConnectionString":"str","transparent":false,"tileVersionDescription":null,"realspaceParameter":null,"createStandardMBTiles":false,"epsgCode":4326,"createNewTileVersion":false,"mapName":"World","convertToPng8":true,"refMapRestAdress":null,"scaleDenominators":[5.91658710909131E8,2.96244033181848E8,1.48122016590924E8,7.4061008295462E7,3.7030504147731E7,1.85152520738655E7,9257626.03693275,4628813.01846637,2314406.50923319,1157203.2546166],"cacheVersion":null,"parentTileVersion":null,"format":"PNG","cacheBounds":{"top":90,"left":-180,"bottom":-90,"leftBottom":{"x":-180,"y":-90},"right":180,"rightTop":{"x":180,"y":90}},"storeConfig":{"innerTileSourceInfo":{"outputPath":"/etc/icloud/SuperMapiServer/webapps/iserver/output/sqlite","type":"SMTiles"},"tileStorageServers":[],"type":"Remote","token":null},"dataPreProcessInfo":null,"actualTileVersion":null,"taskAssignmentType":"DEFAULT","tileType":"Image","autoAvoidEffectEnabled":false,"useLocal":true,"tileSize":"SIZE_256","compressionQuality":0.75,"storageType":null,"vectorBounds":null,"vectorParameter":null}},"newResourceLocation":"http://192.168.20.158:8090/iserver/manager/tileservice/jobs/d7bff309-8f7f-48bb-9c4f-bf9b9224fb41.json"}'
        entity = PostTileJobsItem()
        entity.dataConnectionString = 'map-World'
        entity.mapName = 'World'
        entity.tileSize = TileSize.SIZE_256
        entity.format = OutputFormat.PNG
        entity.transparent = False
        entity.scaleDenominators = [1200000]
        entity.originalPoint = None
        entity.epsgCode = -1
        entity.tileType = TileType.Image
        entity.storageID = 'aa'
        storage = TileSourceInfo()
        storage.type = 'SMTiles'
        storage.outputPath = '/etc/icloud/SuperMapiServer/webapps/iserver/output/sqlite'
        entity.storeConfig = storage
        self.check_api('post_tilejobs', self.baseuri + "/manager/tileservice/jobs.json", HttpMethod.POST,
                       httpretty.Response(body=body, status=201), entity=entity)

        getbody = '[{"id":"2288b51b-562c-4db7-a45d-8a2782126b24","state":{"masterAddress":null,"dataPreProcessBuildConfig":null,"tileMatrixEdgeCount":45,"dataPreProcessState":null,"total":122018,"startTime":1515746622436,"deployedCompleted":8,"tasks":[{"masterAddress":null,"isRetile":false,"jobId":"2288b51b-562c-4db7-a45d-8a2782126b24","tileMatrixToBuilds":[{"novalueFlags":null,"columnCount":45,"rowCount":45,"startingIndex":{"columnIndex":180,"rowIndex":0}}],"taskType":"TILETASK","originalPoint":{"x":-180,"y":90},"scaleConfigs":[{"scaleDenominator":1200000,"cacheRegions":null,"excludeRegions":null,"resolution":0,"tileBoundsWidth":"0.7301506629323473","tileBoundsHeight":"0.730150662932347"}],"id":"650b0c99-db3e-4787-a5c7-58f1b5ba0f7a","state":{"workerId":null,"lastIndex":null,"completed":0,"runState":null},"deployTime":0,"totalTileCount":2025,"dataPreProcessInfo":null}],"buildingScale":{"failedRegion":null,"total":122018,"totalMatrix":null,"workerBuildingInfos":[{"masterAddress":null,"hostName":"ubuntu","address":null,"port":8090,"ip":"192.168.20.158","lastTileRegion":null,"name":"ubuntu_8090","controllable":false,"completed":8100,"id":"38efbec5de2846d1bd499866637aec46","local":true,"token":null}],"scaleDenominator":1200000,"matrixes":[{"novalueFlags":null,"columnCount":494,"rowCount":247,"startingIndex":{"columnIndex":0,"rowIndex":0}}],"nextIndex":{"columnIndex":225,"rowIndex":0},"completed":8100,"completedBytes":0,"completedRegion":null},"scaleInfos":[{"failedRegion":null,"total":122018,"totalMatrix":null,"workerBuildingInfos":[{"masterAddress":null,"hostName":"ubuntu","address":null,"port":8090,"ip":"192.168.20.158","lastTileRegion":null,"name":"ubuntu_8090","controllable":false,"completed":8100,"id":"38efbec5de2846d1bd499866637aec46","local":true,"token":null}],"scaleDenominator":1200000,"matrixes":[{"novalueFlags":null,"columnCount":494,"rowCount":247,"startingIndex":{"columnIndex":0,"rowIndex":0}}],"completed":8100,"completedBytes":18020057,"completedRegion":null}],"pureColorTileCount":5733,"deployedTotal":2025,"remainTime":1019842,"completed":8100,"analystBlankPercentage":0,"tasksToRetry":[],"deployingDataWorkerInfo":[],"scaleConfigs":[{"scaleDenominator":1200000,"cacheRegions":null,"excludeRegions":null,"resolution":0,"tileBoundsWidth":"0.7301506629323473","tileBoundsHeight":"0.730150662932347"}],"completedScale":[],"runState":"BUILDING","noFeaturesTileCount":0,"deployedWorkerInfo":[{"masterAddress":null,"hostName":"ubuntu","address":null,"port":8090,"ip":"192.168.20.158","name":"ubuntu_8090","controllable":false,"id":"38efbec5de2846d1bd499866637aec46","local":true,"token":null}],"completedBytes":18020057,"speedPerSecond":31,"elapsedTime":63297},"targetTilesetInfo":{"filePath":"/etc/icloud/SuperMapiServer/webapps/iserver/output/sqlite/World_1152242556_256X256_PNG.smtiles","name":"smtiles_tileset_1596041633"},"info":{"originalPoint":{"x":-180,"y":90},"fileVerificationMode":"FILESIZE","cacheRegions":null,"utfGridParameter":null,"resolutions":[0.0028521510270794817],"dataConnectionString":"str","transparent":false,"tileVersionDescription":null,"realspaceParameter":null,"createStandardMBTiles":false,"epsgCode":4326,"createNewTileVersion":false,"mapName":"World","convertToPng8":false,"refMapRestAdress":null,"scaleDenominators":[1200000],"cacheVersion":null,"parentTileVersion":null,"format":"PNG","cacheBounds":{"top":90,"left":-180,"bottom":-90,"leftBottom":{"x":-180,"y":-90},"right":180,"rightTop":{"x":180,"y":90}},"storeConfig":{"innerTileSourceInfo":{"outputPath":"/etc/icloud/SuperMapiServer/webapps/iserver/output/sqlite","type":"SMTiles"},"tileStorageServers":[],"type":"Remote","token":null},"dataPreProcessInfo":null,"actualTileVersion":null,"taskAssignmentType":"DEFAULT","tileType":"Image","autoAvoidEffectEnabled":false,"useLocal":true,"tileSize":"SIZE_256","compressionQuality":0,"storageType":null,"vectorBounds":null,"vectorParameter":null}}]'
        self.check_api('get_tilejobs', self.baseuri + "/manager/tileservice/jobs.json", HttpMethod.GET,
                       httpretty.Response(body=getbody, status=201))
        self.check_api('head_tilejobs', self.baseuri + "/manager/tileservice/jobs.json", HttpMethod.HEAD,
                       httpretty.Response(body=getbody, status=201))

    def test_tilejob(self):
        getbody = '{"id":"2288b51b-562c-4db7-a45d-8a2782126b24","state":{"masterAddress":null,"dataPreProcessBuildConfig":null,"tileMatrixEdgeCount":45,"dataPreProcessState":null,"total":122018,"startTime":1515746622436,"deployedCompleted":8,"tasks":[{"masterAddress":null,"isRetile":false,"jobId":"2288b51b-562c-4db7-a45d-8a2782126b24","tileMatrixToBuilds":[{"novalueFlags":null,"columnCount":45,"rowCount":45,"startingIndex":{"columnIndex":180,"rowIndex":0}}],"taskType":"TILETASK","originalPoint":{"x":-180,"y":90},"scaleConfigs":[{"scaleDenominator":1200000,"cacheRegions":null,"excludeRegions":null,"resolution":0,"tileBoundsWidth":"0.7301506629323473","tileBoundsHeight":"0.730150662932347"}],"id":"650b0c99-db3e-4787-a5c7-58f1b5ba0f7a","state":{"workerId":null,"lastIndex":null,"completed":0,"runState":null},"deployTime":0,"totalTileCount":2025,"dataPreProcessInfo":null}],"buildingScale":{"failedRegion":null,"total":122018,"totalMatrix":null,"workerBuildingInfos":[{"masterAddress":null,"hostName":"ubuntu","address":null,"port":8090,"ip":"192.168.20.158","lastTileRegion":null,"name":"ubuntu_8090","controllable":false,"completed":8100,"id":"38efbec5de2846d1bd499866637aec46","local":true,"token":null}],"scaleDenominator":1200000,"matrixes":[{"novalueFlags":null,"columnCount":494,"rowCount":247,"startingIndex":{"columnIndex":0,"rowIndex":0}}],"nextIndex":{"columnIndex":225,"rowIndex":0},"completed":8100,"completedBytes":0,"completedRegion":null},"scaleInfos":[{"failedRegion":null,"total":122018,"totalMatrix":null,"workerBuildingInfos":[{"masterAddress":null,"hostName":"ubuntu","address":null,"port":8090,"ip":"192.168.20.158","lastTileRegion":null,"name":"ubuntu_8090","controllable":false,"completed":8100,"id":"38efbec5de2846d1bd499866637aec46","local":true,"token":null}],"scaleDenominator":1200000,"matrixes":[{"novalueFlags":null,"columnCount":494,"rowCount":247,"startingIndex":{"columnIndex":0,"rowIndex":0}}],"completed":8100,"completedBytes":18020057,"completedRegion":null}],"pureColorTileCount":5733,"deployedTotal":2025,"remainTime":1019842,"completed":8100,"analystBlankPercentage":0,"tasksToRetry":[],"deployingDataWorkerInfo":[],"scaleConfigs":[{"scaleDenominator":1200000,"cacheRegions":null,"excludeRegions":null,"resolution":0,"tileBoundsWidth":"0.7301506629323473","tileBoundsHeight":"0.730150662932347"}],"completedScale":[],"runState":"BUILDING","noFeaturesTileCount":0,"deployedWorkerInfo":[{"masterAddress":null,"hostName":"ubuntu","address":null,"port":8090,"ip":"192.168.20.158","name":"ubuntu_8090","controllable":false,"id":"38efbec5de2846d1bd499866637aec46","local":true,"token":null}],"completedBytes":18020057,"speedPerSecond":31,"elapsedTime":63297},"targetTilesetInfo":{"filePath":"/etc/icloud/SuperMapiServer/webapps/iserver/output/sqlite/World_1152242556_256X256_PNG.smtiles","name":"smtiles_tileset_1596041633"},"info":{"originalPoint":{"x":-180,"y":90},"fileVerificationMode":"FILESIZE","cacheRegions":null,"utfGridParameter":null,"resolutions":[0.0028521510270794817],"dataConnectionString":"str","transparent":false,"tileVersionDescription":null,"realspaceParameter":null,"createStandardMBTiles":false,"epsgCode":4326,"createNewTileVersion":false,"mapName":"World","convertToPng8":false,"refMapRestAdress":null,"scaleDenominators":[1200000],"cacheVersion":null,"parentTileVersion":null,"format":"PNG","cacheBounds":{"top":90,"left":-180,"bottom":-90,"leftBottom":{"x":-180,"y":-90},"right":180,"rightTop":{"x":180,"y":90}},"storeConfig":{"innerTileSourceInfo":{"outputPath":"/etc/icloud/SuperMapiServer/webapps/iserver/output/sqlite","type":"SMTiles"},"tileStorageServers":[],"type":"Remote","token":null},"dataPreProcessInfo":null,"actualTileVersion":null,"taskAssignmentType":"DEFAULT","tileType":"Image","autoAvoidEffectEnabled":false,"useLocal":true,"tileSize":"SIZE_256","compressionQuality":0,"storageType":null,"vectorBounds":null,"vectorParameter":null}}'
        self.check_api('get_tilejob',
                       self.baseuri + '/manager/tileservice/jobs/2288b51b-562c-4db7-a45d-8a2782126b24.json',
                       HttpMethod.GET, httpretty.Response(body=getbody, status=200),
                       id='2288b51b-562c-4db7-a45d-8a2782126b24')
        self.check_api('put_tilejob',
                       self.baseuri + '/manager/tileservice/jobs/2288b51b-562c-4db7-a45d-8a2782126b24.json',
                       HttpMethod.PUT, httpretty.Response(body='{"succeed": true}', status=200),
                       id='2288b51b-562c-4db7-a45d-8a2782126b24', entity=BuildState.STOPPED)
        self.check_api('delete_tilejob',
                       self.baseuri + '/manager/tileservice/jobs/2288b51b-562c-4db7-a45d-8a2782126b24.json',
                       HttpMethod.DELETE, httpretty.Response(body='{"succeed": true}', status=200),
                       id='2288b51b-562c-4db7-a45d-8a2782126b24')
        self.check_api('head_tilejob',
                       self.baseuri + '/manager/tileservice/jobs/2288b51b-562c-4db7-a45d-8a2782126b24.json',
                       HttpMethod.HEAD, httpretty.Response(body='{"succeed": true}', status=200),
                       id='2288b51b-562c-4db7-a45d-8a2782126b24')

    def test_updatetilejob(self):
        entity = PostTilesetUpdateJobs()
        entity.sourceTileSourceInfo = SMTilesTileSourceInfo()
        entity.sourceTileSourceInfo.type = 'SMTiles'
        entity.sourceTileSourceInfo.outputPath = '/etc/icloud/SuperMapiServer/webapps/iserver/output/sqlite12'
        entity.sourceTilesetIdentifier = '/etc/icloud/SuperMapiServer/webapps/iserver/output/sqlite12/World_1179708792_256X256_PNG.smtiles'
        entity.targetTileSourceInfo = SMTilesTileSourceInfo()
        entity.targetTileSourceInfo.type = 'SMTiles'
        entity.targetTileSourceInfo.outputPath = '/etc/icloud/SuperMapiServer/webapps/iserver/output/sqlite13'
        entity.targetTilesetIdentifier = '/etc/icloud/SuperMapiServer/webapps/iserver/output/sqlite13/World_1318435482_256X256_PNG.smtiles'
        entity.scaleDenominators = [4000000.000014754, 8000000.000197801, 15999999.999974867, 31999999.999949735,
                                    63999999.99821653, 124999999.99967217, 249999999.99934435]
        entity.bounds = Rectangle2D()
        entity.bounds.leftBottom = Point2D()
        entity.bounds.leftBottom.x = -180
        entity.bounds.leftBottom.y = -90
        entity.bounds.rightTop = Point2D()
        entity.bounds.rightTop.x = 180
        entity.bounds.rightTop.y = 90
        post_body = '{"postResultType":"CreateChild","newResourceID":"f1341552-d09f-456d-8c06-0b04612b5762","succeed":true,"newResourceLocation":"http://192.168.20.158:8090/iserver/manager/tilesetupdatejobs/f1341552-d09f-456d-8c06-0b04612b5762.json"}'
        self.check_api('post_tilesetupdatejobs', self.baseuri + '/manager/tilesetupdatejobs.json', HttpMethod.POST,
                       httpretty.Response(body=post_body, status=200), entity=entity)
        get_body = '[{"postResultType":"CreateChild","newResourceID":"f1341552-d09f-456d-8c06-0b04612b5762","succeed":true,"newResourceLocation":"http://192.168.20.158:8090/iserver/manager/tilesetupdatejobs/f1341552-d09f-456d-8c06-0b04612b5762.json"}]'
        self.check_api('get_tilesetupdatejobs', self.baseuri + '/manager/tilesetupdatejobs.json', HttpMethod.GET,
                       httpretty.Response(body=get_body, status=200))
        job_get_body = '{"id":"f1341552-d09f-456d-8c06-0b04612b5762","state":{"total":14654,"completedScales":[{"tileMatrix":{"novalueFlags":null,"columnCount":3,"rowCount":2,"startingIndex":{"columnIndex":0,"rowIndex":0}},"total":6,"scaleDenominator":2.4999999999934435E8,"completed":6,"resolution":0.59419813064}],"actualCompleted":12,"toExportScales":[{"tileMatrix":{"novalueFlags":null,"columnCount":10,"rowCount":5,"startingIndex":{"columnIndex":0,"rowIndex":0}},"total":50,"scaleDenominator":6.399999999821653E7,"completed":0,"resolution":0.15211472144},{"tileMatrix":{"novalueFlags":null,"columnCount":19,"rowCount":10,"startingIndex":{"columnIndex":0,"rowIndex":0}},"total":190,"scaleDenominator":3.1999999999949735E7,"completed":0,"resolution":0.076057360722},{"tileMatrix":{"novalueFlags":null,"columnCount":37,"rowCount":19,"startingIndex":{"columnIndex":0,"rowIndex":0}},"total":703,"scaleDenominator":1.5999999999974867E7,"completed":0,"resolution":0.038028680361},{"tileMatrix":{"novalueFlags":null,"columnCount":74,"rowCount":37,"startingIndex":{"columnIndex":0,"rowIndex":0}},"total":2738,"scaleDenominator":8000000.000197801,"completed":0,"resolution":0.019014340181},{"tileMatrix":{"novalueFlags":null,"columnCount":148,"rowCount":74,"startingIndex":{"columnIndex":0,"rowIndex":0}},"total":10952,"scaleDenominator":4000000.000014754,"completed":0,"resolution":0.0095071700903}],"exporttingScale":{"tileMatrix":{"novalueFlags":null,"columnCount":5,"rowCount":3,"startingIndex":{"columnIndex":0,"rowIndex":0}},"total":15,"scaleDenominator":1.2499999999967217E8,"nextIndex":{"columnIndex":2,"rowIndex":6},"completed":6,"resolution":0.29709906532},"startTime":1516238843458,"remainTime":334326,"completed":12,"runState":"RUNNING","elapsedTime":274,"speedPerSecond":57},"info":{"sourceTilesetInfo":{"metaData":{"scaleDenominators":[2.4999999999934435E8,1.2499999999967217E8,6.399999999821653E7,3.1999999999949735E7,1.5999999999974867E7,8000000.000197801,4000000.000014754],"originalPoint":{"x":-180,"y":90},"standardMBTiles":false,"resolutions":[0.59419813064,0.29709906532,0.15211472144,0.076057360722,0.038028680361,0.019014340181,0.0095071700903],"tileWidth":256,"mapStatusHashCode":"1318435482","transparent":false,"mapParameter":null,"tileType":"Image","tileFormat":"PNG","bounds":{"top":90,"left":-180,"bottom":-90,"leftBottom":{"x":-180,"y":-90},"right":180,"rightTop":{"x":180,"y":90}},"tileRuleVersion":"1.1","prjCoordSys":{"distanceUnit":"METER","projectionParam":null,"epsgCode":4326,"coordUnit":"DEGREE","name":"Longitude / Latitude Coordinate System---GCS_WGS_1984","projection":null,"type":"PCS_EARTH_LONGITUDE_LATITUDE","coordSystem":{"datum":{"name":"D_WGS_1984","type":"DATUM_WGS_1984","spheroid":{"flatten":0.00335281066474748,"name":"WGS_1984","axis":6378137,"type":"SPHEROID_WGS_1984"}},"unit":"DEGREE","spatialRefType":"SPATIALREF_EARTH_LONGITUDE_LATITUDE","name":"GCS_WGS_1984","type":"GCS_WGS_1984","primeMeridian":{"longitudeValue":0,"name":"Greenwich","type":"PRIMEMERIDIAN_GREENWICH"}}},"mapName":"World","tileHeight":256},"name":"smtiles_tileset_1596041633","tileVersions":null},"targetTileSourceInfo":{"outputPath":"/etc/icloud/SuperMapiServer/webapps/iserver/output/sqlite12","type":"SMTiles"},"targetInfo":"/etc/icloud/SuperMapiServer/webapps/iserver/output/sqlite12/World_1179708792_256X256_PNG.smtiles","scaleDenominators":[2.4999999999934435E8,1.2499999999967217E8,6.399999999821653E7,3.1999999999949735E7,1.5999999999974867E7,8000000.000197801,4000000.000014754],"relatedObject":null,"sourceTilesetDesc":{"filePath":"/etc/icloud/SuperMapiServer/webapps/iserver/output/sqlite13/World_1318435482_256X256_PNG.smtiles","name":"smtiles_tileset_1596041633"},"sourceTileSourceInfo":{"outputPath":"/etc/icloud/SuperMapiServer/webapps/iserver/output/sqlite13","type":"SMTiles"},"targetTilesetIdentifier":"/etc/icloud/SuperMapiServer/webapps/iserver/output/sqlite12/World_1179708792_256X256_PNG.smtiles","bounds":{"top":90,"left":-180,"bottom":-90,"leftBottom":{"x":-180,"y":-90},"right":180,"rightTop":{"x":180,"y":90}},"tileVersions":null,"targetTilesetInfo":{"metaData":{"scaleDenominators":[2.4999999999934435E8,1.2499999999967217E8,6.399999999821653E7,3.1999999999949735E7,1.5999999999974867E7,8000000.000197801,4000000.000014754],"originalPoint":{"x":-180,"y":90},"standardMBTiles":false,"resolutions":[0.59419813064,0.29709906532,0.15211472144,0.076057360722,0.038028680361,0.019014340181,0.0095071700903],"tileWidth":256,"mapStatusHashCode":"1179708792","transparent":false,"mapParameter":null,"tileType":"Image","tileFormat":"PNG","bounds":{"top":90,"left":-180,"bottom":-90,"leftBottom":{"x":-180,"y":-90},"right":180,"rightTop":{"x":180,"y":90}},"tileRuleVersion":"1.1","prjCoordSys":{"distanceUnit":"METER","projectionParam":null,"epsgCode":4326,"coordUnit":"DEGREE","name":"Longitude / Latitude Coordinate System---GCS_WGS_1984","projection":null,"type":"PCS_EARTH_LONGITUDE_LATITUDE","coordSystem":{"datum":{"name":"D_WGS_1984","type":"DATUM_WGS_1984","spheroid":{"flatten":0.00335281066474748,"name":"WGS_1984","axis":6378137,"type":"SPHEROID_WGS_1984"}},"unit":"DEGREE","spatialRefType":"SPATIALREF_EARTH_LONGITUDE_LATITUDE","name":"GCS_WGS_1984","type":"GCS_WGS_1984","primeMeridian":{"longitudeValue":0,"name":"Greenwich","type":"PRIMEMERIDIAN_GREENWICH"}}},"mapName":"World","tileHeight":256},"name":"smtiles_tileset_1596041633","tileVersions":null},"targetTilesetDesc":{"filePath":"/etc/icloud/SuperMapiServer/webapps/iserver/output/sqlite12/World_1179708792_256X256_PNG.smtiles","name":"smtiles_tileset_1596041633"},"sourceTilesetIdentifier":"/etc/icloud/SuperMapiServer/webapps/iserver/output/sqlite13/World_1318435482_256X256_PNG.smtiles"}}'
        self.check_api('get_tilesetupdatejob',
                       self.baseuri + '/manager/tilesetupdatejobs/f1341552-d09f-456d-8c06-0b04612b5762.json',
                       HttpMethod.GET, httpretty.Response(body=job_get_body, status=200),
                       id='f1341552-d09f-456d-8c06-0b04612b5762')

    def test_deletemapcomponent(self):
        self.check_api('delete_mapcomponent', self.baseuri + '/manager/services/map.json', HttpMethod.DELETE,
                       httpretty.Response(body='{"succeed": true}', status=200), name='map')

    @mock.patch('builtins.open', mock.mock_open(read_data='1'))
    def test_fileuploadtask(self):
        param = PostFileUploadTasksParam()
        post_fileuploadtasks = '{"newResourceID":"38efbec5de2846d1bd499866637aec46_74d0dd27cf454fe1875f0b94490e7280","succeed":true,"newResourceLocation":"http://192.168.20.158:8090/iserver/manager/filemanager/uploadtasks/38efbec5de2846d1bd499866637aec46_74d0dd27cf454fe1875f0b94490e7280"}'
        self.check_api('post_fileuploadtasks', self.baseuri + '/manager/filemanager/uploadtasks.json', HttpMethod.POST,
                       httpretty.Response(body=post_fileuploadtasks, status=200), entity=param)
        taskid = '38efbec5de2846d1bd499866637aec46_74d0dd27cf454fe1875f0b94490e7280'
        post_fileuploadtask = '{"fileName":"World0","fileSize":0,"filePath":"/etc/icloud/SuperMapiServer/webapps/iserver/./World0/","isDirectory":true}'
        with open('./World.zip', 'rb') as fileb:
            self.check_api('post_fileuploadtask',
                           self.baseuri + '/manager/filemanager/uploadtasks/38efbec5de2846d1bd499866637aec46_74d0dd27cf454fe1875f0b94490e7280.json',
                           HttpMethod.POST, httpretty.Response(body=post_fileuploadtask, status=200), id=taskid,
                           file=fileb, toFile='./World.zip')
        get_fileuploadtask = '{"uploadedByteCount":0,"path":"/etc/icloud/SuperMapiServer/upload","progress":100,"state":"UPLOADING","uploadedDataMD5":null,"taskID":"38efbec5de2846d1bd499866637aec46_9f2791745913493abe53d2db755ecaf1","md5":null}'
        self.check_api('get_fileuploadtask',
                       self.baseuri + '/manager/filemanager/uploadtasks/38efbec5de2846d1bd499866637aec46_74d0dd27cf454fe1875f0b94490e7280.json',
                       HttpMethod.GET, httpretty.Response(body=get_fileuploadtask, status=200), id=taskid)

    def test_get_service_mongodb_cache(self):
        get_mng_service_body = '{"isStreamingService":false,"interfaceTypes":"com.supermap.services.rest.RestServlet","isSet":false,"instances":[{"interfaceType":"com.supermap.services.rest.RestServlet","componentType":"com.supermap.services.components.impl.MapImpl","name":"cache-World/rest","componentSetName":null,"authorizeSetting":{"permittedRoles":[],"deniedRoles":[],"type":"PUBLIC"},"id":null,"componentName":"map-smtiles-World2","interfaceName":"rest","enabled":true,"status":"OK"}],"isClusterService":false,"type":"com.supermap.services.components.impl.MapImpl","interfaceNames":"rest","clusterInterfaceNames":"","isDataflowService":false,"component":{"isScSet":false,"scSetSetting":null,"scSetting":{"disabledInterfaceNames":"","instanceCount":0,"name":"map-smtiles-World2","alias":"","interfaceNames":"rest","type":"com.supermap.services.components.impl.MapImpl","config":{"cacheReadOnly":false,"cacheConfigs":null,"useVectorTileCache":false,"utfGridCacheConfig":null,"tileCacheConfig":null,"vectorTileCacheConfig":null,"expired":0,"logLevel":"info","outputPath":"","useCache":false,"outputSite":"","useUTFGridCache":false,"clip":false},"providers":"smtiles-World2","enabled":true}},"providerNames":"smtiles-World2","name":"cache-World","alias":"","providers":[{"spsetSetting":null,"isSPSet":false,"spSetting":{"name":"smtiles-World2","alias":null,"innerProviders":null,"type":"com.supermap.services.providers.SMTilesMapProvider","config":{"dataPrjCoordSysType":null,"watermark":null,"cacheVersion":"4.0","outputPath":"./output","filePath":"/etc/icloud/SuperMapiServer/bin/iserver/output/sqlite113/World_1881337416_256X256_PNG.smtiles","cacheMode":null,"name":null,"outputSite":"http://{ip}:{port}/iserver/output/"},"enabled":true}}]}'
        response = httpretty.Response(body=get_mng_service_body, status=200)
        self.check_api(Management.get_service, self.baseuri + '/manager/services/cache-World.json', HttpMethod.GET,
                       response, service_name='cache-World')

    def test_get_service_mongodb_cache(self):
        get_mng_service_body = '{"isStreamingService":false,"interfaceTypes":"com.supermap.services.wms.WMSServlet","isSet":false,"instances":[{"interfaceType":"com.supermap.services.wms.WMSServlet","componentType":"com.supermap.services.components.impl.MapImpl","name":"map-World/wms111","componentSetName":null,"authorizeSetting":{"permittedRoles":[],"deniedRoles":[],"type":"PUBLIC"},"id":null,"componentName":"map-World","interfaceName":"wms111","enabled":true,"status":"OK"}],"isClusterService":false,"type":"com.supermap.services.components.impl.MapImpl","interfaceNames":"wms111","clusterInterfaceNames":"","isDataflowService":false,"component":{"isScSet":false,"scSetSetting":null,"scSetting":{"disabledInterfaceNames":"","instanceCount":0,"name":"map-World","alias":"","interfaceNames":"wms111","type":"com.supermap.services.components.impl.MapImpl","config":{"cacheReadOnly":true,"cacheConfigs":null,"useVectorTileCache":false,"utfGridCacheConfig":{"outputPath":"C:/supermappackages/supermap-iserver-9.0.1-win64-deploy/webapps/iserver/output/sqlite","type":"UTFGrid","datastoreType":"TILES"},"tileCacheConfig":{"serverAdresses":["192.168.20.144:27017"],"database":"sampledb","password":"xyz123","type":"MongoDB","datastoreType":"TILES","username":"myTester"},"vectorTileCacheConfig":{"outputPath":"C:/supermappackages/supermap-iserver-9.0.1-win64-deploy/webapps/iserver/output/sqlite","type":"SVTiles","datastoreType":"TILES"},"expired":0,"logLevel":null,"outputPath":null,"useCache":true,"outputSite":null,"useUTFGridCache":false,"clip":false},"providers":"map-World","enabled":true}},"providerNames":"map-World","name":"map-World","alias":"","providers":[{"spsetSetting":null,"isSPSet":false,"spSetting":{"name":"map-World","alias":null,"innerProviders":null,"type":"com.supermap.services.providers.UGCMapProvider","config":{"extractCacheToFile":true,"workspacePath":"C:/supermappackages/data/World/World.sxwu","dataPrjCoordSysType":null,"watermark":null,"cacheVersion":"4.0","inflatDisabled":false,"maps":null,"useCompactCache":false,"excludedFieldsInMaps":null,"poolSize":0,"preferedPNGType":"PNG","datasourceInfos":null,"multiThread":true,"multiInstance":false,"layerCountPerDataType":0,"ignoreHashcodeWhenUseCache":false,"outputPath":null,"cacheMode":null,"name":null,"leftTopCorner":null,"outputSite":null,"cacheDisabled":false,"queryExpectCount":1000,"ugcMapSettings":[]},"enabled":true}}]}'
        response = httpretty.Response(body=get_mng_service_body, status=200)
        result = self.check_api(Management.get_service, self.baseuri + '/manager/services/cache-World.json', HttpMethod.GET,
                       response, service_name='cache-World') #type: MngServiceInfo
        config = result.component.scSetting.config #type: MapConfig
        self.assertIsInstance(config, MapConfig)
        cacheconfig = config.tileCacheConfig #type: MongoDBTilesourceInfo
        self.assertIsInstance(cacheconfig, MongoDBTilesourceInfo)
        self.assertEqual(cacheconfig.serverAdresses, ["192.168.20.144:27017"])

    def test_get_datastores(self):
        body = '[{"id":"mongodb","dataStoreInfo":{"serverAdresses":["127.0.0.1:88"],"database":"mongodb","password":"mongodb","type":"MongoDB","datastoreType":"TILES","username":"mongodb"}}]'
        response = httpretty.Response(body=body, status=200)
        self.check_api(Management.get_datastores, self.baseuri + '/manager/datastores.json', HttpMethod.GET,
                       response)
