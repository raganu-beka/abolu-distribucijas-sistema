from aboli import app, db, auth, Apple, Transaction

if __name__ == '__main__':
    auth.User.create_table(fail_silently=True)
    Apple.create_table(fail_silently=True)
    Transaction.create_table(fail_silently=True)

    app.run(debug=True)