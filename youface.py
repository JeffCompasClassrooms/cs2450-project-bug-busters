# std imports
import time

# installed imports
import flask
import timeago
import tinydb

# handlers

from handlers import friends, login, posts, casino
from db import leaderboard
from flask import Blueprint, render_template

blueprint = Blueprint('casino', __name__, url_prefix='/casino')

@blueprint.route('/roulette')
def roulette():
    return render_template('casino/roulette.html')
 


app = flask.Flask(__name__)

@app.template_filter('convert_time')
def convert_time(ts):
    """A jinja template helper to convert timestamps to timeago."""
    return timeago.format(ts, time.time())

app.register_blueprint(friends.blueprint)
app.register_blueprint(login.blueprint)
app.register_blueprint(posts.blueprint)
app.register_blueprint(casino.blueprint)
app.register_blueprint(leaderboard.blueprint)


app.secret_key = 'mygroup'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.run(debug=True, host='0.0.0.0')
