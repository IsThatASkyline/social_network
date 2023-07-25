from httpx import AsyncClient


async def test_register_user(client_author: AsyncClient, client_guest: AsyncClient):
    user_data = {
        'username': 'author',
        'email': 'author@gmail.com',
        'password': 'author',
        'is_active': True,
        'is_superuser': False,
        'is_verified': False,
    }

    user_data2 = {
        'username': 'guest',
        'email': 'guest@gmail.com',
        'password': 'guest',
        'is_active': True,
        'is_superuser': False,
        'is_verified': False,
    }

    wrong_user_data = {
        'username': 'wrong',
        'email': '.com',
        'password': 'guest',
        'is_active': True,
        'is_superuser': False,
        'is_verified': False,
    }
    resp_422 = await client_guest.post("/auth/register", json=wrong_user_data)
    resp_author = await client_author.post("/auth/register", json=user_data)
    resp_guest = await client_guest.post("/auth/register", json=user_data2)

    assert resp_author.status_code == 201
    assert resp_guest.status_code == 201
    assert resp_422.status_code == 422


async def test_user_login(client_author: AsyncClient, client_guest: AsyncClient):
    resp_author = await client_author.post('/auth/jwt/login', data={
        'username': 'author@gmail.com',
        'password': 'author',
    })

    resp_guest = await client_guest.post('/auth/jwt/login', data={
        'username': 'guest@gmail.com',
        'password': 'guest',
    })

    assert resp_author.status_code == 204
    assert 'blog_cookie' in resp_author.cookies

    client_author.cookies.set('blog_cookie', resp_author.cookies.get('blog_cookie'))
    client_guest.cookies.set('blog_cookie', resp_guest.cookies.get('blog_cookie'))


async def test_add_post(client_author: AsyncClient):
    resp_author = await client_author.post('/social/post', json={'text': 'test_post1'})
    assert resp_author.status_code == 200
    assert resp_author.json()['detail'] == "Запись успешно добавлена"

    resp_422 = await client_author.post('/social/post')
    assert resp_422.status_code == 422


async def test_get_post(client_author: AsyncClient):
    resp_author = await client_author.get('/social/post/1')
    post = resp_author.json()

    assert post['data']['text'] == 'test_post1'
    assert post['data']['owner_id'] == 1
    assert post['data']['likes_amount'] == 0
    assert post['data']['dislikes_amount'] == 0
    assert post['detail'] is None

    resp_404 = await client_author.get('/social/post/2')
    assert resp_404.status_code == 404


async def test_patch_post(client_author: AsyncClient, client_guest: AsyncClient):
    resp_author = await client_author.patch('/social/post/1', json={'text': 'changetesttext'})
    resp_guest = await client_author.get('/social/post/1')
    post = resp_author.json()
    resp_404 = await client_guest.patch('/social/post/1', json={'text': 'changetesttext'})

    assert resp_guest.status_code == 200
    assert post['detail'] == "Запись обновлена"
    assert resp_404.status_code == 404


async def test_like_post(client_author: AsyncClient, client_guest: AsyncClient):
    resp_404 = await client_author.get('/social/post/dislike/123')
    resp_423 = await client_author.get('/social/post/like/1')
    assert resp_423.status_code == 423
    assert resp_423.json()['detail']['detail'] == "Нельзя оценивать свои записи"
    assert resp_404.status_code == 404

    resp_guest_like = await client_guest.get('/social/post/like/1')
    assert resp_guest_like.status_code == 200
    assert resp_guest_like.json()['detail'] == "Запись добавлена в понравившееся"

    resp_guest_unlike = await client_guest.get('/social/post/like/1')
    assert resp_guest_unlike.status_code == 200
    assert resp_guest_unlike.json()['detail'] == "Запись убрана из понравившихся"


async def test_dislike_post(client_author: AsyncClient, client_guest: AsyncClient):
    resp_404 = await client_author.get('/social/post/dislike/123')
    resp_423 = await client_author.get('/social/post/dislike/1')
    assert resp_423.status_code == 423
    assert resp_423.json()['detail']['detail'] == "Нельзя оценивать свои записи"
    assert resp_404.status_code == 404

    resp_guest_dislike = await client_guest.get('/social/post/dislike/1')
    assert resp_guest_dislike.status_code == 200
    assert resp_guest_dislike.json()['detail'] == "Запись добавлена в непонравившееся"

    resp_guest_undislike = await client_guest.get('/social/post/dislike/1')
    assert resp_guest_undislike.status_code == 200
    assert resp_guest_undislike.json()
    assert resp_guest_undislike.json()['detail'] == "Запись убрана из непонравившихся"


async def test_delete_post(client_author: AsyncClient, client_guest: AsyncClient):
    resp_guest = await client_guest.delete('/social/post/1')
    resp_author = await client_author.delete('/social/post/1')
    resp_404 = await client_author.get('/social/post/1')

    assert resp_author.status_code == 200
    assert resp_author.json()['detail'] == 'Запись удалена'
    assert resp_guest.status_code == 404
    assert resp_404.status_code == 404
