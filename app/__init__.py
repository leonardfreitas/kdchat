from flask import Flask, render_template
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_hashing import Hashing
from flask_login import LoginManager

app = Flask(__name__)

app.config.from_object('config')
socketio = SocketIO( app )
bcrypt = Bcrypt(app)
hashing = Hashing(app)
db = SQLAlchemy( app )
migrate = Migrate( app, db )

login_manager = LoginManager()
login_manager.init_app(app)

manager = Manager( app )
manager.add_command( 'db', MigrateCommand )

from app.models import user
from app.forms import user
from app.controllers import KDC, auth