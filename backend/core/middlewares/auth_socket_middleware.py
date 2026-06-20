from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser

from core.services.jwt_service import JWTService


@database_sync_to_async
def get_user_from_socket_token(token: str):
    try:
        return JWTService.validate_socket_token(token)
    except ValueError:
        return AnonymousUser()


class AuthSocketMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = scope.get('query_string', b'').decode('utf-8')
        query_params = parse_qs(query_string)
        token = query_params.get('token', [None])[0]

        scope['user'] = await get_user_from_socket_token(token) if token else AnonymousUser()

        return await super().__call__(scope, receive, send)