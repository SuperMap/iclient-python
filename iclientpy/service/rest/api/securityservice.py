from ..decorator import post
from .model import PostTokenParameter


class SecurityService:
    @post('/security/tokens', entityKW='entity')
    def post_tokens(self, entity: PostTokenParameter) -> str:
        pass
