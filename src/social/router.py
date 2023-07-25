from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.social.services import get_post_from_db, CUSTOM_404, add_post_to_db, delete_post_from_db, update_post_in_db, \
    like_post_in_db, dislike_post_in_db, CUSTOM_423
from src.auth.models import User
from src.database import get_async_session
from src.social.schemas import PostCreate, PostUpdate
from src.auth.base_config import current_active_user


router = APIRouter(
    prefix='/social',
    tags=['social']
)


@router.get('/post/{post_id}')
async def get_post(post_id: int, session: AsyncSession = Depends(get_async_session)):
    post = await get_post_from_db(session, post_id)
    if post:
        return {
            "status": status.HTTP_200_OK,
            "data": post,
            "detail": None,
        }
    else:
        raise CUSTOM_404


@router.post('/post')
async def add_post(new_post: PostCreate, user: User = Depends(current_active_user), session: AsyncSession = Depends(get_async_session)):
    await add_post_to_db(session, new_post, user.id)
    return {
            "status": status.HTTP_200_OK,
            "data": None,
            "detail": "Запись успешно добавлена",
        }


@router.delete('/post/{post_id}')
async def delete_post(post_id: int, user: User = Depends(current_active_user), session: AsyncSession = Depends(get_async_session)):
    post = await get_post_from_db(session, post_id, user.id)
    if post:
        await delete_post_from_db(session, post_id)
        return {
            "status": status.HTTP_200_OK,
            "data": None,
            "detail": "Запись удалена",
        }
    else:
        raise CUSTOM_404


@router.patch('/post/{post_id}')
async def update_post(updated_post: PostUpdate, post_id: int, user: User = Depends(current_active_user), session: AsyncSession = Depends(get_async_session)):
    post = await get_post_from_db(session, post_id, user.id)
    if post:
        await update_post_in_db(session, updated_post, post_id)
        return {
            "status": status.HTTP_200_OK,
            "data": None,
            "detail": "Запись обновлена",
        }
    else:
        raise CUSTOM_404


@router.get('/post/like/{post_id}')
async def like_post(post_id: int, user: User = Depends(current_active_user), session: AsyncSession = Depends(get_async_session)):
    post = await get_post_from_db(session, post_id)
    if post:
        if post.owner_id != user.id:
            liked = await like_post_in_db(session, post_id, user.id)
            if not liked:
                return {
                    "status": status.HTTP_200_OK,
                    "data": None,
                    "detail": "Запись добавлена в понравившееся",
                }
            else:
                return {
                    "status": status.HTTP_200_OK,
                    "data": None,
                    "detail": "Запись убрана из понравившихся",
                }
        elif post.owner_id == user.id:
            raise CUSTOM_423
    else:
        raise CUSTOM_404


@router.get('/post/dislike/{post_id}')
async def dislike_post(post_id: int, user: User = Depends(current_active_user), session: AsyncSession = Depends(get_async_session)):
    post = await get_post_from_db(session, post_id)
    if post:
        if post.owner_id != user.id:
            disliked = await dislike_post_in_db(session, post_id, user.id)
            if not disliked:
                return {
                    "status": status.HTTP_200_OK,
                    "data": None,
                    "detail": "Запись добавлена в непонравившееся",
                }
            else:
                return {
                    "status": status.HTTP_200_OK,
                    "data": None,
                    "detail": "Запись убрана из непонравившихся",
                }
        elif post.owner_id == user.id:
            raise CUSTOM_423
    else:
        raise CUSTOM_404
