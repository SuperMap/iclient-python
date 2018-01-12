import httpretty
from iclientpy.rest.api.management import *
from iclientpy.rest.decorator import HttpMethod
from iclientpy.rest.api.management import PostTileJobItem, TileSize, OutputFormat, TileType, TileSourceInfo
from .abstractrest import AbstractRESTTestCase


class ManagementTest(AbstractRESTTestCase):
    @classmethod
    def setUpClass(cls):
        cls.init_rest(cls)
        cls.init_apifactory(cls)
        cls.init_api(cls, "management")

    def test_workspace(self):
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

    def test_tilejob(self):
        body = '{"postResultType":"CreateChild","newResourceID":"d7bff309-8f7f-48bb-9c4f-bf9b9224fb41","succeed":true,"customResult":{"id":"d7bff309-8f7f-48bb-9c4f-bf9b9224fb41","state":null,"targetTilesetInfo":{"filePath":"/etc/icloud/SuperMapiServer/webapps/iserver/output/sqlite/World_1152242556_256X256_PNG.smtiles","name":"smtiles_tileset_1596041633"},"info":{"originalPoint":{"x":-180,"y":90},"fileVerificationMode":"FILESIZE","cacheRegions":null,"utfGridParameter":null,"resolutions":[1.4062499999999996,0.7041106029214795,0.35205530146073977,0.17602765073036988,0.08801382536518494,0.04400691268259247,0.022003456341296235,0.011001728170648107,0.005500864085324063,0.002750432042662044],"dataConnectionString":"str","transparent":false,"tileVersionDescription":null,"realspaceParameter":null,"createStandardMBTiles":false,"epsgCode":4326,"createNewTileVersion":false,"mapName":"World","convertToPng8":true,"refMapRestAdress":null,"scaleDenominators":[5.91658710909131E8,2.96244033181848E8,1.48122016590924E8,7.4061008295462E7,3.7030504147731E7,1.85152520738655E7,9257626.03693275,4628813.01846637,2314406.50923319,1157203.2546166],"cacheVersion":null,"parentTileVersion":null,"format":"PNG","cacheBounds":{"top":90,"left":-180,"bottom":-90,"leftBottom":{"x":-180,"y":-90},"right":180,"rightTop":{"x":180,"y":90}},"storeConfig":{"innerTileSourceInfo":{"outputPath":"/etc/icloud/SuperMapiServer/webapps/iserver/output/sqlite","type":"SMTiles"},"tileStorageServers":[],"type":"Remote","token":null},"dataPreProcessInfo":null,"actualTileVersion":null,"taskAssignmentType":"DEFAULT","tileType":"Image","autoAvoidEffectEnabled":false,"useLocal":true,"tileSize":"SIZE_256","compressionQuality":0.75,"storageType":null,"vectorBounds":null,"vectorParameter":null}},"newResourceLocation":"http://192.168.20.158:8090/iserver/manager/tileservice/jobs/d7bff309-8f7f-48bb-9c4f-bf9b9224fb41.json"}'
        entity = PostTileJobItem()
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
