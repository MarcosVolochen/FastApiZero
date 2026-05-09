from http import HTTPStatus


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


def test_read_users(client):

    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'username': 'bob',
                'email': 'bob@example.com',
                'id': 1,
            }
        ],
    }


def test_update_user(client):

    response = client.put(
        '/users/1',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': '654987',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_update_user_not_found(client):
    response = client.put(
        '/users/99',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': '654987',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Foi mal, não tem'}


def test_read_user(client):

    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_read_user_not_found(client):

    for id in [99, -1]:
        response = client.get(f'users/{id}')

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == {'detail': 'Foi mal, não tem'}


def test_delete_user(client):

    response = client.delete('users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_delete_user_not_found(client):

    for id in [99, -1]:
        response = client.delete(f'users/{id}')

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == {'detail': 'Foi mal, não tem'}
