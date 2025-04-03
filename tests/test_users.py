from http import HTTPStatus

from app.schemas.users import UserPublic


def test_create_user(client):
    response = client.post(
        '/v1/users/',
        json={
            'username': 'scott',
            'email': 'scott@example.com',
            'password': 'scottGreatSecret',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'scott',
        'email': 'scott@example.com',
        'id': 1,
    }


def test_create_user_username_should_return_400(client, user):
    response = client.post(
        '/v1/users/',
        json={
            'username': user.username,
            'email': 'great-email@email.com',
            'password': 'great-password',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_email_should_return_400(client, user):
    response = client.post(
        '/v1/users/',
        json={
            'username': 'Great Scott',
            'email': user.email,
            'password': 'great-password',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}


def test_read_users(client, user):
    response = client.get('/v1/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [{'username': user.username, 'email': user.email, 'id': 1}]
    }


def test_read_users_no_content(client):
    response = client.get('/v1/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_user_by_id(client, user):
    response = client.get(f'/v1/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': user.username,
        'email': user.email,
        'id': user.id,
    }


def test_read_user_by_id_should_return_404(client, user):
    mock_user_id = user.id + 1
    response = client.get(f'/v1/users/{mock_user_id}')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()

    response = client.get('/v1/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, token):
    response = client.put(
        f'/v1/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': 1,
    }


def test_update_user_with_wrong_user(client, another_user, token):
    response = client.put(
        f'/v1/users/{another_user.id}',
        json={
            'username': 'bobjoe',
            'email': 'bob@example.com',
            'password': 'bobjoesecret',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permission'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/v1/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_with_wrong_user(client, another_user, token):
    response = client.delete(
        f'/v1/users/{another_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permission'}
