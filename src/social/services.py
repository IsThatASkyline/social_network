from fastapi import HTTPException, status
from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.social.models import Post, PostsLikes, PostsDislikes
from src.social.schemas import PostCreate, PostUpdate


CUSTOM_404 = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status": status.HTTP_404_NOT_FOUND,
                "data": None,
                "detail": "Запись не найдена",
            }
        )

CUSTOM_423 = HTTPException(
                status_code=status.HTTP_423_LOCKED,
                detail={
                    "status": status.HTTP_423_LOCKED,
                    "data": None,
                    "detail": "Нельзя оценивать свои записи",
                })


async def get_post_from_db(session: AsyncSession, post_id: int, user_id: int = None):
    if user_id:
        q = select(Post).where(Post.id == post_id, Post.owner_id == user_id)
    else:
        q = select(Post).where(Post.id == post_id)
    post = await session.execute(q)
    return post.scalar_one_or_none()


async def add_post_to_db(session: AsyncSession, new_post: PostCreate, user_id: int):
    stmt = insert(Post).values(**new_post.model_dump(), owner_id=user_id)
    await session.execute(stmt)
    await session.commit()
    return


async def delete_post_from_db(session: AsyncSession, post_id: int):
    stmt = delete(Post).where(Post.id == post_id)
    await session.execute(stmt)
    await session.commit()
    return


async def update_post_in_db(session: AsyncSession, updated_post: PostUpdate, post_id: int):
    stmt = update(Post).where(Post.id == post_id).values(**updated_post.model_dump())
    await session.execute(stmt)
    await session.commit()
    return


async def like_post_in_db(session: AsyncSession, post_id: int, user_id: int):
    q = select(PostsLikes).where(PostsLikes.post_id == post_id, PostsLikes.user_id == user_id)
    res = await session.execute(q)
    liked = res.scalar_one_or_none()
    if not liked:
        stmt = insert(PostsLikes).values(user_id=user_id, post_id=post_id)
        await session.execute(stmt)
        await session.commit()
        return False
    elif liked:
        stmt = delete(PostsLikes).where(PostsLikes.user_id == user_id, PostsLikes.post_id == post_id)
        await session.execute(stmt)
        await session.commit()
        return True


async def dislike_post_in_db(session: AsyncSession, post_id: int, user_id: int):
    q = select(PostsDislikes).where(PostsDislikes.post_id == post_id, PostsDislikes.user_id == user_id)
    res = await session.execute(q)
    disliked = res.scalar_one_or_none()
    if not disliked:
        stmt = insert(PostsDislikes).values(user_id=user_id, post_id=post_id)
        await session.execute(stmt)
        await session.commit()
        return False
    elif disliked:
        stmt = delete(PostsDislikes).where(PostsDislikes.user_id == user_id, PostsDislikes.post_id == post_id)
        await session.execute(stmt)
        await session.commit()
        return True
