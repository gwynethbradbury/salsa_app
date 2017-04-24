from flask import Blueprint, abort
from jinja2 import TemplateNotFound

import dbconfig
from flask import request, session, flash, redirect, url_for, render_template


if dbconfig.test:
    from mock_access_helper import MockAccessHelper as AccessHelper
else:
    from access_helper import AccessHelper
AH = AccessHelper()

home = Blueprint('home', __name__,template_folder='templates')#,
                 # static_folder='core/static')


@home.route('/')#, defaults={'page': 'index'})
def get_news_articles():
    instances = AH.get_news()
    return render_template("index.html",news_articles=instances)

@home.route('/<page>')
def show(page):
    try:
        return render_template('%s.html' % page)
    except TemplateNotFound:
        abort(404)


dbas = 1
nc = 2
iam = 3


@home.route('/nextcloud')
def my_nextcloud_projects():
    instances = []
    instances = AH.get_projects(nc)
    return render_template("nextcloud.html", instances=instances)


@home.route('/dbas')
def my_dbas():
    instances = AH.get_projects(dbas)
    return render_template("dbas.html", instances=instances)

@home.route('/iam')
def my_iam():
    instances = AH.get_projects(iam)
    return render_template("iam.html", instances=instances)


@home.route('/events')
def upcoming_events():
    events = AH.get_events()
    return render_template("events.html",futureevents=events[2],nowevents=events[1],pastevents=events[0])


@home.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != home.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != home.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('pages/login.html', error=error)


@home.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))