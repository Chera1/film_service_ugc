import uuid

from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_jwt_auth import AuthJWT

from src.services.like import FilmLikeService, get_film_like_service
from src.utils.jwt import get_token


# Объект router, в котором регистрируем обработчики
router = APIRouter()


@router.post('/',
             summary='Добавление лайка',
             description='''
             Добавление лайка
             '''
             )
async def like_add(
        film_id: uuid.UUID = Body(),
        value: int = Body(),
        token: HTTPAuthorizationCredentials = Depends(HTTPBearer(bearerFormat='Bearer')),
        authorize: AuthJWT = Depends(),
        film_like_service: FilmLikeService = Depends(get_film_like_service)
    ) -> dict:
    """
    Добавление лайка пользователя
    """
    token = get_token(authorize)

    response = await film_like_service.add_film_like(
        user_id=token['user_uuid'],
        film_id=str(film_id),
        value=value,
    )
    if not response:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                            detail='Like already exists')

    response = {'id': str(response.inserted_id)}

    return response


@router.delete('/{film_id}',
               summary='Удаление лайка',
               description='''
               Удаление лайка пользователя
               '''
               )
async def like_delete(
        film_id: uuid.UUID,
        token: HTTPAuthorizationCredentials = Depends(HTTPBearer(bearerFormat='Bearer')),
        authorize: AuthJWT = Depends(),
        film_like_service: FilmLikeService = Depends(get_film_like_service)
    ) -> dict:
    """
    Удаление лайка пользователя
    """
    token = get_token(authorize)

    response = await film_like_service.delete_film_like(
        user_id=token['user_uuid'],
        film_id=str(film_id),
    )

    if not response:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                            detail='Like is not exists')
    response = {'msg': 'DELETED'}

    return response


@router.put('/{film_id}',
            summary='Обновление лайка',
            description='''
            Обновление лайка пользователя
            '''
            )
async def like_update(
        film_id: uuid.UUID,
        value: int = Body(),
        token: HTTPAuthorizationCredentials = Depends(HTTPBearer(bearerFormat='Bearer')),
        authorize: AuthJWT = Depends(),
        film_like_service: FilmLikeService = Depends(get_film_like_service)
    ) -> dict:
    """
    Обновление лайка пользователя
    """
    token = get_token(authorize)

    response = await film_like_service.update_film_like(
        user_id=token['user_uuid'],
        film_id=str(film_id),
        value=value,
    )

    if not response:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                            detail='Like is not exists')
    response = {'msg': 'UPDATED'}

    return response


@router.get('/{film_id}/average',
            summary='Подсчет среднего рейтинга для фильма',
            description='''
            Подсчет среднего рейтинга для фильма
            '''
            )
async def like_average(
        film_id: uuid.UUID,
        film_like_service: FilmLikeService = Depends(get_film_like_service)
    ) -> dict:
    """
    Подсчет среднего рейтинга для фильма
    """
    response = await film_like_service.average_film_likes(
        film_id=str(film_id),
    )

    if not response:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                            detail='Film is not exists')

    response = response[0]
    response["_id"] = str(uuid.UUID(bytes=response["_id"]))

    return response


@router.get('/{film_id}/summary',
            summary='Информация по оценкам, поставленным фильму',
            description='''
            Информация по оценкам, поставленным фильму
            '''
            )
async def like_summary(
        film_id: uuid.UUID,
        film_like_service: FilmLikeService = Depends(get_film_like_service)
    ) -> dict:
    """
    Информация по оценкам, поставленным фильму
    """
    response = await film_like_service.summary_film_likes(
        film_id=str(film_id),
    )

    if not response:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                            detail='Film is not exists')

    return response