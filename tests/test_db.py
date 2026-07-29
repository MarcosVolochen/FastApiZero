from dataclasses import asdict

from sqlalchemy import select

from fastapi_zero.models import User


def test_create_user(session, mock_db_time):

    with mock_db_time(model=User) as time:
        new_user = User(
            username='alvaro',
            email='alvaro@exemplo.com',
            password='123123',
        )

        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        new_user.email = 'alvaro_atualizado@exemplo.com'

        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        user = session.scalar(select(User).where(User.username == 'alvaro'))

        assert asdict(user) == {
            'id': 1,
            'username': 'alvaro',
            'email': 'alvaro_atualizado@exemplo.com',
            'password': '123123',
            'created_at': time,
            'updated_at': time,
        }


def test_update_user(session, mock_db_time):

    with mock_db_time(model=User) as time:
        new_user = User(
            username='test',
            email='test@exemplo.com',
            password='123123',
        )

        session.add(new_user)
        session.commit()

        user_instance = session.scalar(
            select(User).where(User.username == 'test')
        )
        user_instance.password = '987654321'
        user_instance.email = 'update@exemplo.com'

        session.commit()

        user = session.scalar(select(User).where(User.username == 'test'))

        assert asdict(user) == {
            'id': 1,
            'username': 'test',
            'email': 'update@exemplo.com',
            'password': '987654321',
            'created_at': time,
            'updated_at': time,
        }
