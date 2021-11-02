from werkzeug.security import safe_str_cmp

from user import User

users = [
    User(_id=1, username='felipekafuri', password='12345')
]

# u.username is going to be u for u in users
username_mapping = {u.username: u for u in users}

userid_mapping = {u.id: u for u in users}


def authenticate(username, password):
    user = username_mapping.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None) 