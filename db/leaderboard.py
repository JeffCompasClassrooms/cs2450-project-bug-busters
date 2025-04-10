from flask import Blueprint, current_app
from tinydb import TinyDB

# Create a Blueprint
blueprint = Blueprint('leaderboard', __name__)

# Initialize TinyDB
db = TinyDB('db.json')

def get_leaderboard():
    users = db.table('users')
    all_users = users.all()
    
    # Sort users by coins in descending order
    leaderboard = sorted(all_users, key=lambda user: user.get('coins', 0), reverse=True)
    
    return leaderboard

# Add a context processor to make leaderboard data available to all templates
@blueprint.app_context_processor
def inject_leaderboard():
    return {'leaderboard': get_leaderboard()}