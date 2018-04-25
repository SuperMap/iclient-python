from ..decorator import get
from typing import List
from iclientpy.rest.api.model import GetMyDepartmentsResult, GetMyDepartmentsMembersResult


class MyDepartments:

    @get('/mycontent/departments')
    def get_mydepartments(self) -> List[GetMyDepartmentsResult]:
        pass

    @get('/mycontent/departments/members')
    def get_mydepartments_members(self) -> List[GetMyDepartmentsMembersResult]:
        pass
