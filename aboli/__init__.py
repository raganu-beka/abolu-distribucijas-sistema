import flask
from flask_peewee.db import Database
from flask_peewee.auth import Auth
from flask_peewee.admin import Admin, ModelAdmin

DATABASE = {
    'name': 'aboli.db',
    'engine': 'peewee.SqliteDatabase'
}
DEBUG = True
SECRET_KEY = 'noslepums'

app = flask.Flask(__name__)
app.config.from_object(__name__)

db = Database(app)
auth = Auth(app, db)
admin = Admin(app, auth)

from aboli.routes import *
from aboli.panels import *

admin.register(Apple, AppleAdmin)
admin.register(auth.User, UserAdmin)
admin.register(Transaction, TransactionAdmin)
admin.setup()