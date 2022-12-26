import uuid

from bson.binary import Binary
from http import HTTPStatus
from typing import Optional, Union

from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import JWTDecodeError, MissingTokenError

from src.services.review import ReviewService, get_review_service
from src.models.models import ReviewAPI, Review


# Объект router, в котором регистрируем обработчики
router = APIRouter()


@router.post('/{review_id}/rate',
             summary='Добавление оценки к рецензии на фильм',
             description='''
             Добавление оценки к рецензии на фильм
             '''
             )
async def review_rating_add(
        review_id: str,
        value: int = Body(),
        token: HTTPAuthorizationCredentials = Depends(HTTPBearer(bearerFormat='Bearer')),
        authorize: AuthJWT = Depends(),
        review_like_service: ReviewService = Depends(get_review_service)
    ) -> dict:
    """
    Добавление оценки к рецензии на фильм
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

    response = await review_like_service.add_like_to_review(
        user_id=token['user_uuid'],
        review_id=str(review_id),
        value=value,
    )
    if not response:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                            detail='Review is not exists')

    response = {'id': str(response.inserted_id)}

    return response


@router.post('/',
             summary='Добавление рецензии на фильм',
             description='''
             Добавление рецензии на фильм
             '''
             )
async def review_add(
        film_id: uuid.UUID = Body(),
        text: str = Body(),
        token: HTTPAuthorizationCredentials = Depends(HTTPBearer(bearerFormat='Bearer')),
        authorize: AuthJWT = Depends(),
        review_like_service: ReviewService = Depends(get_review_service)
    ) -> dict:
    """
    Добавление рецензии на фильм
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

    response = await review_like_service.add_review(
        user_id=token['user_uuid'],
        film_id=str(film_id),
        text=text,
    )
    if not response:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                            detail='Review already exists')

    response = {'id': str(response.inserted_id)}

    return response


@router.get('/',
            summary='Получение списка рецензий',
            description='''
            Получение списка рецензий
            '''
            )
async def reviews_get(
        sort: Optional[str] = None,
        limit: Optional[int] = 50,
        page: Optional[int] = 1,
        review_like_service: ReviewService = Depends(get_review_service)
    ) -> dict:
    """
    Получение списка рецензий
    """
    response = await review_like_service.get_reviews(sort, limit, page)

    return response
