from http import HTTPStatus

from fastapi_zero.shemas import UserPublic, UserSchema


def test_root_deve_retornar_ola_mundo(client):
    """
    Esse test tem 3 etapas (AAA)
    - A: Arrange - Arranjo
    - A: Act     - Executa a coisa (o SUI)
    - A: Assert  - Garanta que A é A
    """

    response = client.get('/')

    assert response.json() == {'message': 'Olá mundo'}

    assert response.status_code == HTTPStatus.OK


def test_create_user(client):

    response = client.post(
        '/users/',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': '123456',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'email': 'bob@example.com',
        'id': 1,
        'username': 'bob',
    }


def test_create_user_integraty_error_email(client, user):

    response = client.post(
        '/users/',
        json={
            'username': 'bala',
            'email': user.email,
            'password': '123456',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists'}


def test_create_user_integraty_error_username(client, user):

    response = client.post(
        '/users/',
        json={
            'username': user.username,
            'email': 'emial_test@gmail.com',
            'password': '123456',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already exists'}


def test_read_users(client, user, token):

    user_schema = UserPublic.model_validate(user).model_dump()

    response = client.get(
        '/users/', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, token):

    user.username = 'Teste'
    user_update = UserSchema.model_validate(user).model_dump()

    user_view = UserPublic.model_validate(user).model_dump()

    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json=user_update,
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_view


def test_delete_user(client, user, token):

    response = client.delete(
        f'users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_deleting_other_user(client, token):

    response = client.delete(
        'users/9999',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permisions'}


# def test_update_user_not_found(client):
#     response = client.put(
#         '/users/99',
#         json={
#             'username': 'alice',
#             'email': 'alice@example.com',
#             'password': '654987',
#         },
#     )
#     assert response.status_code == HTTPStatus.NOT_FOUND
#     assert response.json() == {'detail': 'User ID do not exist.'}


def test_read_user(client, user, token):

    response = client.get(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': 1,
    }


def test_read_user_not_found(client):

    for id in [99, -1]:
        response = client.get(f'users/{id}')

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == {'detail': 'User ID do not exist.'}


def test_update_integrity_error(client, user, token):

    client.post(
        '/users',
        json={
            'username': 'alice',
            'email': 'qqqqqqttteste@example.com',
            'password': '654987',
        },
    )

    response_update = client.put(
        '/users/99',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'alice',
            'email': 'qqqqqqttteste@example.com',
            'password': '123456',
        },
    )

    assert response_update.status_code == HTTPStatus.FORBIDDEN
    assert response_update.json() == {'detail': 'Not enough permisions'}


def test_update_forbidden_error(client, user, token):

    response_update = client.put(
        '/users/99',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'alice',
            'email': 'qqqqqqttteste@example.com',
            'password': '123456',
        },
    )

    assert response_update.status_code == HTTPStatus.FORBIDDEN
    assert response_update.json() == {'detail': 'Not enough permisions'}


def test_get_token(client, user):

    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token
