import uuid

from http import HTTPStatus
from typing import Optional, Union

from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import JWTDecodeError, MissingTokenError

from src.services.bookmark import BookMarkService, get_bookmark_service
from src.models.models import Bookmark, BookmarkAPI


# Объект router, в котором регистрируем обработчики
router = APIRouter()


@router.post('/',
             summary='Добавление фильма в закладки',
             description='''
             Асинхронное добавление фильма в закладки
             '''
             )
async def bookmark_add(
        film_id: uuid.UUID = Body(),
        token: HTTPAuthorizationCredentials = Depends(HTTPBearer(bearerFormat='Bearer')),
        authorize: AuthJWT = Depends(),
        bookmark_service: BookMarkService = Depends(get_bookmark_service)
    ) -> dict:
    """
    Добавление фильма в закладки пользователя
    """
    try:
        authorize.jwt_required()
    except JWTDecodeError:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED,
                            detail='Token not valid or expired')
    except MissingTokenError:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED,
                            detail='Token not found')
    token = authorize.get_raw_jwt()

    response = await bookmark_service.add_bookmark(
        user_id=token['user_uuid'],
        film_id=str(film_id),
    )
    if not response:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                            detail='Bookmark already exists')

    response = {'id': str(response.inserted_id)}

    return response


@router.delete('/',
               summary='Удаление фильма из закладок пользователя',
               description='''
               Асинхронное удаление фильма из закладок пользователя
               '''
               )
async def bookmark_delete(
        film_id: uuid.UUID = Body(),
        token: HTTPAuthorizationCredentials = Depends(HTTPBearer(bearerFormat='Bearer')),
        authorize: AuthJWT = Depends(),
        bookmark_service: BookMarkService = Depends(get_bookmark_service)
    ) -> dict:
    """
    Удаление фильма из закладок пользователя
    """
    try:
        authorize.jwt_required()
    except JWTDecodeError:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED,
                            detail='Token not valid or expired')
    except MissingTokenError:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED,
                            detail='Token not found')

    token = authorize.get_raw_jwt()
    response = await bookmark_service.delete_bookmark(
        user_id=token['user_uuid'],
        film_id=str(film_id),
    )

    if not response:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                            detail='Bookmark is not exists')
    response = {'msg': 'DELETED'}

    return response


@router.get('/',
            response_model=list[BookmarkAPI],
            summary='Получение фильмов пользователя из закладок',
            description='''
            Получение фильмов пользователя из закладок
            '''
            )
async def bookmarks_get(
        token: HTTPAuthorizationCredentials = Depends(HTTPBearer(bearerFormat='Bearer')),
        authorize: AuthJWT = Depends(),
        bookmark_service: BookMarkService = Depends(get_bookmark_service)
    ) -> Union[list[BookmarkAPI], None]:
    """
    Получение фильмов пользователя из закладок
    """
    try:
        authorize.jwt_required()
    except JWTDecodeError:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED,
                            detail='Token not valid or expired')
    except MissingTokenError:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED,
                            detail='Token not found')
    token = authorize.get_raw_jwt()

    response = await bookmark_service.get_bookmarks(
        user_id=token['user_uuid'],
    )
    print(response)

    return response
