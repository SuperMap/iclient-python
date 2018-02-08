from typing import List

from .model import Point2D
from ..decorator import get


class GetMapResult:
    name: str
    center: Point2D
    visibleScales: List[float]


class MapService:

    @get('/maps/{map}')
    def get_map(self, map: str) -> GetMapResult:
        pass
