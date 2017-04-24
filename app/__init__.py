# project/__init__.py

from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
import dbconfig


app = Flask('salsa_app')
app.config.update(
        DEBUG=True#,
        #SQLALCHEMY_DATABASE_URI='sqlite:///../salsa_app.db',
    )

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@localhost/salsa_app'.format(dbconfig.db_user,
                                                                                           dbconfig.db_password)

db = SQLAlchemy(app)


from core.home import home
from admin import admin

app.register_blueprint(home)
app.register_blueprint(admin, url_prefix='/admin', template_folder='templates')


@app.route('/admin')
def home():
    return render_template("admin/admin.html")
