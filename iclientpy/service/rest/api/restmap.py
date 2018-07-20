from typing import List

from .model import Point2D, ChildResourceInfo, PrjCoordSys
from ..decorator import get


class Rectangle2D:
    leftBottom: Point2D
    rightTop: Point2D


class GetMapResult:
    name: str
    center: Point2D
    visibleScales: List[float]
    bounds: Rectangle2D
    viewBounds: Rectangle2D
    prjCoordSys: PrjCoordSys



class MapService:

    @get('/maps/{map}')
    def get_map(self, map: str) -> GetMapResult:
        pass

    @get('/maps/{map}', fixed_queryKWs={'prjCoordSys': '{"epsgCode":4326}'})
    def get_map_4326(self, map: str) -> GetMapResult:
        pass

    @get('/maps')
    def get_map_resources(self) -> List[ChildResourceInfo]:
        pass