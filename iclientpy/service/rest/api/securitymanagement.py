from typing import List
from ..decorator import post, get, put, delete
from .model import UserEntity, UserInfo, RoleEntity, MethodResult


class SecurityManagement:

    @get('/manager/security/users')
    def get_users(self) -> List[List[str]]:
        pass

    @post('/manager/security/users', entityKW='entity')
    def post_users(self, entity: UserEntity) -> MethodResult:
        pass

    @put('/manager/security/users', entityKW='entity')
    def put_users(self, entity: List[str]) -> MethodResult:
        pass

    @get('/manager/security/users/{username}')
    def get_user(self, username: str) -> UserInfo:
        pass

    @put('/manager/security/users/{username}', entityKW='entity')
    def put_user(self, username: str, entity: UserEntity) -> MethodResult:
        pass

    @delete('/manager/security/users/{username}')
    def delete_user(self, username: str) -> MethodResult:
        pass

    @get('/manager/security/roles')
    def get_roles(self) -> List[RoleEntity]:
        pass

    @post('/manager/security/roles', entityKW='entity')
    def post_roles(self, entity: RoleEntity) -> MethodResult:
        pass

    @put('/manager/security/roles', entityKW='entity')
    def put_roles(self, entity: List[str]) -> MethodResult:
        pass

    @get('/manager/security/roles/{role}')
    def get_role(self, role: str) -> RoleEntity:
        pass

    @put('/manager/security/roles/{role}', entityKW='entity')
    def put_role(self, role: str, entity: RoleEntity) -> MethodResult:
        pass

    @delete('/manager/security/roles/{role}')
    def delete_role(self, role: str) -> MethodResult:
        pass


class PortalSecurityManagement(SecurityManagement):
    @get('/manager/security/portalusers')
    def get_users(self) -> List[UserInfo]:
        pass
