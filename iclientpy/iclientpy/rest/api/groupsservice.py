from typing import List
from ..decorator import get
from iclientpy.rest.api.model import GetGroupsResult, GroupOrderBy, JoinType, FilterField


class GroupsService:
    @get('/web/groups', queryKWs=['tags', 'userNames', 'isPublic', 'orderBy', 'joinTypes', 'keywords', 'fileterFields'])
    def get_groups(self, tags: List[str], userNames: List[str], isPublic: bool, orderBy: GroupOrderBy,
                   joinTypes: List[JoinType], keywords: List[str],
                   fileterFields: List[FilterField]) -> GetGroupsResult:
        pass
