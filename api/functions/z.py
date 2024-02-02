from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from ..utils.extensions import is_authenticated, user_playlists, login_required, find_user, current_user
from datetime import datetime
import tmdbsimple as tmdb
from ..config.db import *
import uuid
import json

media_bp = Blueprint('media_bp', __name__, template_folder='templates')
api_search = tmdb.Search()

# Unused route
@login_required
def new_movie(user_id):
    """Creates new media to db"""
    user = find_user(user_id=user_id)
    media_type = request.form['type']
    media_item = {
        'type':            media_type,
        'title':           request.form['title'],
        'genre':           request.form['genre'],           # gets removed for ytvid type
        'year_created':    request.form['year_created'],
        'date_watched':    request.form['date_watched'],
        'acts_dirs':       request.form['act_dirs'],        # gets removed for ytvid type
        'tags':            request.form['tags'],
        'created_by_name': user['username'],
        'created_on':      datetime.now()
    }

    if media_type == 'movie':
        pass  # no need to add or remove attributes for movie_type

    elif media_type == 'tvshow':
        media_item['season'] = request.form['season']
        media_item['episode'] = request.form['episode']

    elif media_type == 'ytvid':
        media_item['creator'] = request.form['creator']

        del media_item['genre']
        del media_item['acts_dirs']

    media_id = media.insert_one(media_item).inserted_id

    return redirect(url_for('index_media', media=media.find(), media_id=media_id))
