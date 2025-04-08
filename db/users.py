import tinydb

def new_user(db, username, password, email):
    users = db.table('users')
    User = tinydb.Query()
    if users.get(User.username == username):
        return None
    user_record = {
            'username': username,
            'password': password,
            'friends': [],
            'coins': 0,
            'banned' : False
            }

    return users.insert(user_record)


def update_user_coins(db, user, amount):
    """Adds coins to the user's account."""
    users = db.table('users')
    User = tinydb.Query()
    
    # Update the user's coin balance by the given amount
    users.update({'coins': user['coins'] + amount}, (User.username == user['username']) & (User.password == user['password']))


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
        user['banned'] = True
        users.update(user, User.email == email)
        return True
    return False
