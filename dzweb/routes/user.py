from flask import Blueprint, render_template, request, session, g, redirect, url_for, flash, make_response, jsonify
from dzweb.db import get_db, get_all_apps
from bcrypt import checkpw
from flask_babel import _
import json
from dzweb.routes.auth import login_required
from datetime import datetime, timedelta

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.before_request
@login_required
def load_added_apps():
    # Fetch all apps from the database
    apps = get_all_apps()
    
    # Store all apps in the context for sidebar rendering
    g.appname_appurl_dict = {app['appname']: app['appurl'] for app in apps}


@bp.route('/')
@login_required
def userhome():
    apps = get_all_apps()
    return render_template('user/userhome.html', apps=apps)


@bp.route('/edit-product')
@login_required
def edit_product():
    return render_template('user/edit-product-permission.html')


@bp.route('/edit-hire')
@login_required
def edit_hire():
    return render_template('user/edit-hire-permission.html')
