from flask import Blueprint, render_template, session, redirect, url_for, request
import random
import flask

from handlers import copy
from db import posts, users, helpers

blackjack_bp = Blueprint('blackjack', __name__, url_prefix='/blackjack')

card_categories = ['Hearts', 'Diamonds', 'Clubs', 'Spades'] # hi byeee
cards_list = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']

def create_deck():
    deck = [(card, category) for category in card_categories for card in cards_list]
    random.shuffle(deck)
    return deck

def card_value(card):
    if card[0] in ['Jack', 'Queen', 'King']:
        return 10
    elif card[0] == 'Ace':
        return 11
    return int(card[0])

def calculate_score(cards):
    score = sum(card_value(card) for card in cards)
    aces = sum(1 for card in cards if card[0] == 'Ace')
    
    while score > 21 and aces:
        score -= 10
        aces -= 1
    
    return score

@blackjack_bp.route('/', methods=['GET', 'POST'])
def blackjack_page():
    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')
    
    if username and password:
        db = helpers.load_db()
        user = users.get_user(db, username, password)
        if user:
            session.setdefault('coins', user['coins'])
    
    player_score = calculate_score(session.get('player_cards', []))
    dealer_score = calculate_score(session.get('dealer_cards', []))

    return render_template('blackjack.html', 
                           player_cards=session.get('player_cards', []), 
                           dealer_cards=session.get('dealer_cards', []), 
                           player_score=player_score, 
                           dealer_score=dealer_score, 
                           game_over=session.get('game_over', False),
                           coins=session.get('coins', 0),
                           bet=session.get('bet', 0))

@blackjack_bp.route('/place_bet', methods=['POST'])
def place_bet():
    """Handles bet submission before game starts."""
    bet = int(request.form.get('bet', 0))
    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')

    if username and password:
        db = helpers.load_db()
        user = users.get_user(db, username, password)

        if user and bet > 0 and bet <= user['coins']:
            session['bet'] = bet
            session['coins'] -= bet  # Deduct locally
            users.update_user_coins(db, user, -bet)  # Deduct in DB

            # Initialize game
            session['deck'] = create_deck()
            session['player_cards'] = [session['deck'].pop(), session['deck'].pop()]
            session['dealer_cards'] = [session['deck'].pop(), session['deck'].pop()]
            session['game_over'] = False
        else:
            return redirect(url_for('blackjack.blackjack_page'))  # Invalid bet

    return redirect(url_for('blackjack.blackjack_page'))

@blackjack_bp.route('/hit')
def hit():
    if not session.get('game_over', False):
        session['player_cards'].append(session['deck'].pop())
        session.modified = True

        if calculate_score(session['player_cards']) > 21:
            session['game_over'] = True

    return redirect(url_for('blackjack.blackjack_page'))

@blackjack_bp.route('/stand')
def stand():
    if not session.get('game_over', False):
        while calculate_score(session['dealer_cards']) < 17:
            session['dealer_cards'].append(session['deck'].pop())
            session.modified = True

        session['game_over'] = True
        player_score = calculate_score(session['player_cards'])
        dealer_score = calculate_score(session['dealer_cards'])
        bet = session.get('bet', 0)

        username = flask.request.cookies.get('username')
        password = flask.request.cookies.get('password')

        if username and password:
            db = helpers.load_db()
            user = users.get_user(db, username, password)
            if user and bet > 0:
                if player_score > 21:  # Player busts, loses bet
                    pass
                elif dealer_score > 21 or player_score > dealer_score:  # Player wins
                    session['coins'] += bet * 2
                    users.update_user_coins(db, user, bet * 2)
                elif player_score == dealer_score:  # Tie, refund bet
                    session['coins'] += bet
                    users.update_user_coins(db, user, bet)

    return redirect(url_for('blackjack.blackjack_page'))


@blackjack_bp.route('/reset')
def reset():
    """Resets the game session and clears the bet."""
    session.pop('bet', None)
    session.pop('player_cards', None)
    session.pop('dealer_cards', None)
    session.pop('game_over', None)
    return redirect(url_for('blackjack.blackjack_page'))

