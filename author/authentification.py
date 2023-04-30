from jwt import encode, decode
from datetime import datetime, timedelta
from rest_framework.exceptions import AuthenticationFailed


def create_access_token(author_id):
    return encode({
        'author_id': author_id,
        'exp': datetime.utcnow() + timedelta(minutes=5),
        'iat': datetime.utcnow()
    }, 'access_secret', algorithm='HS256')


def decode_access_token(token):
    try:
        payload = decode(token, 'access_secret', algorithms='HS256')
        return payload['author_id']
    except:
        raise AuthenticationFailed('Unauthenticated!')


def create_refresh_token(author_id):
    return encode({
        'author_id': author_id,
        'exp': datetime.utcnow() + timedelta(hours=1),
        'iat': datetime.utcnow()
    }, 'refresh_secret', algorithm='HS256')


def decode_refresh_token(token):
    try:
        payload = decode(token, 'refresh_secret', algorithms='HS256')
        return payload['author_id']
    except:
        raise AuthenticationFailed('Unauthenticated!')

