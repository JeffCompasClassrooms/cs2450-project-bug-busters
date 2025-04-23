from flask import Blueprint, render_template, request, session
import random

blueprint = Blueprint('casino', __name__, template_folder='../templates')

@blueprint.route('/casino')
def casino_page():
    return render_template('casino.html')


@blueprint.route('/roulette', methods=['GET', 'POST'])
def roulette():
    if 'balance' not in session:
        session['balance'] = 100

    balance = session['balance']
    resultMessage = None
    win = False

    if request.method == 'POST':
        try:
            bet_number = int(request.form['betNumber'])
            bet_amount = int(request.form['betAmount'])

            if bet_amount > balance:
                resultMessage = "❌ Not enough balance!"
            elif not (0 <= bet_number <= 36):
                resultMessage = "❌ Bet must be between 0 and 36!"
            else:
                winning_number = random.randint(0, 36)
                if bet_number == winning_number:
                    winnings = bet_amount * 35
                    balance += winnings
                    resultMessage = f"🎉 You WON! Number was {winning_number}. You won ${winnings}!"
                    win = True
                else:
                    balance -= bet_amount
                    resultMessage = f"😞 You lost. Number was {winning_number}. You lost ${bet_amount}."

                session['balance'] = balance

        except (ValueError, KeyError):
            resultMessage = "⚠️ Invalid input. Try again."

    return render_template('roulette.html', balance=balance, resultMessage=resultMessage, win=win)


@blueprint.route('/blackjack')
def blackjack():
    # This route can be expanded with actual blackjack logic later
    return render_template('blackjack.html')
