from flask import Blueprint, render_template

blueprint = Blueprint('casino', __name__, template_folder='../templates')

@blueprint.route('/casino')
def casino_page():
    return render_template('casino.html')

@blueprint.route('/roulette')
def roulette():
    return render_template('roulette.html')

@blueprint.route('/slots')
def slots():
    return render_template('slots.html')

@blueprint.route('/dice')
def dice():
    return render_template('dice.html')
