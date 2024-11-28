import peewee

from aboli import db, auth


class Apple(db.Model):
    readiness = peewee.CharField()
    type = peewee.CharField()
    amount_available = peewee.FloatField()
    price = peewee.FloatField()


class Transaction(db.Model):
    type = peewee.CharField()
    user = peewee.ForeignKeyField(auth.User, backref='transactions')
    apple = peewee.ForeignKeyField(Apple, backref='transactions')
    amount = peewee.FloatField()
    total_price = peewee.FloatField()
    address = peewee.TextField(null=True)
    date = peewee.DateField()
