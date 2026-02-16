from strawberry.permission import BasePermission
from strawberry.types import Info


class IsAuthenticated(BasePermission):
    message = "Authentication required. Provide an Authorization header."

    async def has_permission(self, source: object, info: Info, **kwargs: object) -> bool:
        request = info.context.get("request")
        if request is None:
            return False
        auth_header = request.headers.get("Authorization")
        return auth_header is not None and len(auth_header) > 0
