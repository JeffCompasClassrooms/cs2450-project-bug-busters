from flask import Blueprint, render_template
from tinydb import TinyDB

# Create a Blueprint
blueprint = Blueprint('leaderboard', __name__, template_folder='../templates')

# Initialize TinyDB
db = TinyDB('db.json')

def get_leaderboard():
    users = db.table('users')
    all_users = users.all()
    
    # Sort users by coins in descending order
    leaderboard = sorted(all_users, key=lambda user: user.get('coins', 0), reverse=True)
    
    return leaderboard

@blueprint.route('/leaderboard')
def leaderboard_page():
    leaderboard = get_leaderboard()
    return render_template('leaderboard.html', leaderboard=leaderboard)
