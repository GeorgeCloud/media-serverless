# from flask import Flask
from pymongo import MongoClient
# from flask_login import LoginManager
# from flask_bcrypt import Bcrypt
from os import environ
from .config import Config

# app = Flask(__name__)
# app.config.from_object(Config)
# bcrypt = Bcrypt(app)

SECRET_KEY = "key"

# ======= DB Setup ==========
DB_URI = environ.get('kjsbfkjsdbf', 'mongodb+srv://turtle:UnojcaL0xelyDRsU@gjhm.lfn7yup.mongodb.net/gjhm?retryWrites=true&w=majority')
client = MongoClient(DB_URI)
db = client.get_default_database()
# ===========================


# ======= Collections ==========
users = db.users
users.create_index('username', unique=True)

playlists = db.playlists
media = db.media
reviews = db.reviews
friend_requests = db.friend_requests
# =========================


# ======= Authentication ==========
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'auth.view'
#
# @login_manager.user_loader
# def load_user(user_id):
#     return users.find_one({'_id': user_id})
# =================================
