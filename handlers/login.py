import flask
import tinydb

from handlers import copy
from db import posts, users, helpers

blueprint = flask.Blueprint("login", __name__)

@blueprint.route('/loginscreen')
def loginscreen():
    """Present a form to the user to enter their username and password."""
    db = helpers.load_db()

    # First check if already logged in
    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')

    if username is not None and password is not None:
        if users.get_user(db, username, password):
            # If they are logged in, redirect them to the feed page
            flask.flash('You are already logged in.', 'warning')
            return flask.redirect(flask.url_for('login.index'))

    return flask.render_template('login.html', title=copy.title,
            subtitle=copy.subtitle,hide_leaderboard=True)

@blueprint.route('/login', methods=['POST'])
def login():
    """Log in the user."""
    db = helpers.load_db()

    username = flask.request.form.get('username')
    password = flask.request.form.get('password')
    submit = flask.request.form.get('type')

    user = users.get_user(db, username, password)

    # Handle user creation
    if submit == 'Create':
        if user is not None:
            flask.flash(f'Username {username} already taken!', 'danger')
            return flask.redirect(flask.url_for('login.loginscreen'))
        users.new_user(db, username, password)
        flask.flash(f'User {username} created successfully!', 'success')
        resp = flask.make_response(flask.redirect(flask.url_for('login.index')))
        resp.set_cookie('username', username)
        resp.set_cookie('password', password)
        return resp

    # Handle user deletion
    elif submit == 'Delete':
        if users.delete_user(db, username, password):
            flask.flash(f'User {username} deleted successfully!', 'success')
        resp = flask.make_response(flask.redirect(flask.url_for('login.loginscreen')))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('password', '', expires=0)
        return resp

    # Handle login
    elif user:
        if user.get('banned'):
            flask.flash('Your account has been banned.', 'danger')
            return flask.redirect(flask.url_for('login.loginscreen'))

        # If not banned, proceed with login
        resp = flask.make_response(flask.redirect(flask.url_for('login.index')))
        resp.set_cookie('username', username)
        resp.set_cookie('password', password)
        return resp

    flask.flash('Invalid username or password.', 'danger')
    return flask.redirect(flask.url_for('login.loginscreen'))

@blueprint.route('/logout', methods=['POST'])
def logout():
    """Log out the user."""
    db = helpers.load_db()

    resp = flask.make_response(flask.redirect(flask.url_for('login.loginscreen')))
    resp.set_cookie('username', '', expires=0)
    resp.set_cookie('password', '', expires=0)
    return resp

@blueprint.route('/ban', methods=['POST'])
def ban():
    db = helpers.load_db()

    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')
    if not username or not password:
        return "Unauthorized", 401

    user = users.get_user(db, username, password)
    if not user:
        return "Unauthorized", 401

    users_table = db.table('users')
    User = tinydb.Query()
    users_table.update({'banned': True}, (User.username == username) & (User.password == password))

    resp = flask.make_response(flask.redirect(flask.url_for('login.loginscreen')))
    resp.set_cookie('username', '', expires=0)
    resp.set_cookie('password', '', expires=0)
    return resp

@blueprint.route('/')
def index():
    """Serves the main feed page for the user."""
    db = helpers.load_db()

    # make sure the user is logged in
    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')
    if username is None and password is None:
        return flask.redirect(flask.url_for('login.loginscreen'))
    user = users.get_user(db, username, password)
    if not user:
        flask.flash('Invalid credentials. Please try again.', 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))

    # get the info for the user's feed
    friends = users.get_user_friends(db, user)
    all_posts = []
    for friend in friends + [user]:
        all_posts += posts.get_posts(db, friend)
    # sort posts
    sorted_posts = sorted(all_posts, key=lambda post: post['time'], reverse=True)

    return flask.render_template('feed.html', title=copy.title,
            subtitle=copy.subtitle, user=user, username=username,
            friends=friends, posts=sorted_posts)
