from flask_peewee.admin import ModelAdmin

from aboli.models import Transaction

def has_bought_apples(user):
    return Transaction.select().where(
        (Transaction.user == user) & (Transaction.type == 'pirkums')).exists()

def has_sold_apples(user):
    return Transaction.select().where(
        (Transaction.user == user) & (Transaction.type == 'nodosana')).exists()

def has_bought_fertilizer(user):
    return Transaction.select().where(
        (Transaction.user == user) & (Transaction.type == 'meslojums')).exists()


class AppleAdmin(ModelAdmin):
    columns = ('readiness', 'type', 'amount_available', 'price')


class UserAdmin(ModelAdmin):
    def has_bought_apples(self, obj):
        return 'Yes' if has_bought_apples(obj) else 'No'

    def has_sold_apples(self, obj):
        return 'Yes' if has_sold_apples(obj) else 'No'

    def has_bought_fertilizer(self, obj):
        return 'Yes' if has_bought_fertilizer(obj) else 'No'

    columns = ('username', 'email', 'has_bought_apples',
               'has_sold_apples', 'has_bought_fertilizer')


class TransactionAdmin(ModelAdmin):
    columns = ('type', 'total_price', 'date', 'user', 'apple')