# TODO: make a list of users ranked by number of coins
import tinydb
import users

def update_coins(db,username,coins):
    users = db.table('users')
    User = tinydb.Query()
    user = users.get(User.username == username)
    if user:
        # TODO: add boundaries so we can only add/subract a valid amount of coins
        users.update({'coins': coins}, User.username == username)
        return f"{username} now has {coins} coins."
    return "User not found."

def get_leaderboard(db):
    users = db.table('users')
    sorted_users = sorted(users.all(), key=lambda x: x.get('coins', 0), reverse = True)
    
    for rank,user in enumerate(sorted_users, start=1):
        print(f"{rank}. {user['username']} - {user['coins']} coins")
