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
