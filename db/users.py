import tinydb

def new_user(db, username, password, email):
    users = db.table('users')
    User = tinydb.Query()

    if users.get(User.username == username):
        return None  # Username already exists

    user_record = {
        'username': username,
        'password': password,
        'friends': [],
        'coins': 0,
        'banned': False
    }

    return users.insert(user_record)

def get_user(db, username, password):
    users = db.table('users')
    User = tinydb.Query()
    user = users.get((User.username == username) & (User.password == password))
    
    if user:
        # Check if the user is banned
        if user.get('banned', False):  # Defaults to False if 'banned' is not present
            return None  # User is banned
    return user

def get_user_friends(db, username):
    users = db.table('users')
    User = tinydb.Query()
    user = users.get(User.username == username)
    
    if not user:
        return None  # User doesn't exist
    
    # Now retrieve the friends
    friends = []
    for friend_username in user.get('friends', []):
        friend = users.get(User.username == friend_username)
        if friend:
            friends.append(friend)
    
    return friends

def ban_user_by_email(db, email):
    users = db.table('users')
    User = tinydb.Query()
    user = users.get(User.email == email)
    if user:
        users.update({'banned': True}, User.email == email)  # Correct update syntax
        return True
    return False
