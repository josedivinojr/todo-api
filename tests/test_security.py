from jwt import decode

from app.security import create_access_token, settings


def test_create_jwt():
    data = {'sub': 'great-scott@email.com'}
    token = create_access_token(data)

    result = decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    assert result['sub'] == data['sub']
    assert result['exp']
