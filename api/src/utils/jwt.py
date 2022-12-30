from fastapi_jwt_auth import AuthJWT
from fastapi import HTTPException


def get_token(authorize: AuthJWT) -> dict:
    try:
        authorize.jwt_required()
    except JWTDecodeError:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED,
                            detail='Token not valid or expired')
    except MissingTokenError:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED,
                            detail='Token not found')
    token = authorize.get_raw_jwt()

    return token