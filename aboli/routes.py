import flask
from datetime import datetime as dt

from aboli import app, auth
from aboli.models import Transaction, Apple


@app.route('/')
def index():
    return flask.render_template('base.html')


@app.route('/buy_apples', methods=['GET', 'POST'])
@auth.login_required
def buy_apples():
    user = auth.get_logged_in_user()

    if flask.request.method == 'POST':
        apple = Apple.get_by_id(int(flask.request.form.get('type')))
        amount = float(flask.request.form.get('amount'))

        if amount >= apple.amount_available:
            flask.flash('Nav pieejams ābolu daudzums')
            return flask.redirect(flask.url_for('buy_apples'))

        new_transaction = Transaction(
            type='pirkums', user=user, apple=apple,
            amount=amount, total_price=apple.price*amount,
            date=dt.now().date()
        )
        apple.amount_available = apple.amount_available - amount

        new_transaction.save()
        apple.save()

        flask.flash(f'Āboli nopirkti par {apple.price*amount} EUR')
        return flask.redirect(flask.url_for('index'))

    apples = Apple.select().where((Apple.type != 'Mēslojums') & (Apple.amount_available > 0))
    return flask.render_template('buy_apples.html',
                                 apples=apples, user=user)


@app.route('/sell_apples', methods=['GET', 'POST'])
@auth.login_required
def sell_apples():
    user = auth.get_logged_in_user()

    if flask.request.method == 'POST':
        apple = Apple.get_by_id(int(flask.request.form.get('type')))
        price = 0.01 if flask.request.form.get('price') == '1' else 0
        amount = float(flask.request.form.get('amount'))
        address = flask.request.form.get('address')
        pickup_date = dt.strptime(flask.request.form.get('date'), '%Y-%m-%d').date()

        new_transaction = Transaction(
            type='nodosana', user=user, apple=apple,
            amount=amount, total_price=price*amount,
            address=address, date=pickup_date
        )
        apple.amount_available = apple.amount_available + amount

        new_transaction.save()
        apple.save()

        flask.flash(f'Āboli nodoti par {apple.price*amount} EUR')
        return flask.redirect(flask.url_for('index'))

    apples = Apple.select().where((Apple.type != 'Mēslojums') & (Apple.amount_available > 0))
    return flask.render_template('sell_apples.html',
                                 apples=apples, user=user)


@app.route('/get_fertilizer')
@auth.login_required
def get_fertilizer():
    user = auth.get_logged_in_user()
    fertilizer = Apple.get(Apple.type == 'Mēslojums')

    if flask.request.method == 'POST':
        amount = float(flask.request.form.get('amount'))

        new_transaction = Transaction(
            type='meslojums', user=user, apple=fertilizer,
            amount=amount, total_price=fertilizer.price*amount,
            date=dt.now().date()
        )
        fertilizer.amount_available = fertilizer.amount_available - amount

        new_transaction.save()
        fertilizer.save()

        flask.flash(f'Mēslojums nopirkts par {fertilizer.price*amount} EUR')
        return flask.redirect(flask.url_for('index'))

    return flask.render_template('get_fertilizer.html',
                                 fertilizer=fertilizer, user=user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if auth.get_logged_in_user():
        flask.flash('Lietotājs jau ir ienācis sistēmā')
        return flask.redirect(flask.url_for('index'))

    if flask.request.method == 'POST':
        user = auth.User(
            username=flask.request.form.get('username'),
            email=flask.request.form.get('email'),
            admin=False,
            active=True,
        )
        user.set_password(flask.request.form.get('password'))
        user.save()

        flask.flash('Lietotājs izveidots')
        auth.login_user(user)
        return flask.redirect(flask.url_for('index'))

    return flask.render_template('register.html')


@app.route('/logout')
@auth.login_required
def logout():
    auth.logout()
    flask.flash('Lietotājs ir izgājis no sistēmas')
    return flask.redirect(flask.url_for('index'))