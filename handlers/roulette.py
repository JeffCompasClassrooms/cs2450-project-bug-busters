from flask import Flask, render_template, request, session
import random

app = Flask(__name__)
app.secret_key = 'roulette-secret'

@app.route('/roulette', methods=['GET', 'POST'])
def roulette():
    if 'balance' not in session:
        session['balance'] = 100

    resultMessage = None
    win = False
    balance = session['balance']

    if request.method == 'POST':
        bet_number = int(request.form['betNumber'])
        bet_amount = int(request.form['betAmount'])

        if bet_amount > balance:
            resultMessage = "You don't have enough balance!"
        elif not (0 <= bet_number <= 36):
            resultMessage = "Please bet a number between 0 and 36!"
        else:
            winning_number = random.randint(0, 36)
            if bet_number == winning_number:
                winnings = bet_amount * 35
                balance += winnings
                resultMessage = f"🎉 You WON! The number was {winning_number}. You won ${winnings}!"
                win = True
            else:
                balance -= bet_amount
                resultMessage = f"😞 You lost. The number was {winning_number}. You lost ${bet_amount}."

            session['balance'] = balance

    return render_template('roulette.html', balance=balance, resultMessage=resultMessage, win=win)

if __name__ == '__main__':
    app.run(debug=True)
