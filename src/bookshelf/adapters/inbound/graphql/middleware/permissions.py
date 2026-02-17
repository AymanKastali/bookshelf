from strawberry.permission import BasePermission

from bookshelf.adapters.inbound.graphql.context import AppInfo


class IsAuthenticated(BasePermission):
    message = "Authentication required. Provide an Authorization header."

    async def has_permission(self, source: object, info: AppInfo, **kwargs: object) -> bool:
        request = info.context.request
        if request is None:
            return False
        auth_header = request.headers.get("Authorization")
        return auth_header is not None and len(auth_header) > 0
