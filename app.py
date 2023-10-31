from flask import Flask
from flask_login import LoginManager

from flask_wtf.csrf import CSRFProtect

import config
from blueprints.admin import app as admin
from blueprints.general import app as general
from blueprints.user import app as user
from extentions import db
from models.user import User

app = Flask(__name__)

app.register_blueprint(general)
app.register_blueprint(admin)
app.register_blueprint(user)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
db.init_app(app)
csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = config.SECRET_KEY
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
  return User.query.filter(User.id == user_id)


with app.app_context():
  db.create_all()


if __name__ == '__main__':
  app.run(debug=True ,host='0.0.0.0')