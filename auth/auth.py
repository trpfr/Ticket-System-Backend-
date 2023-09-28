from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy

#  TODO: Добавить имя куки
cookie_transport = CookieTransport(cookie_max_age=3600, cookie_samesite="none", cookie_secure=True)

#  TODO: Почитать, как правильно поступать с секретом, куда его прятать и как генерировать
SECRET = "SECRET"


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
