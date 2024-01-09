from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_babelex import Babel
import cloudinary

app = Flask(__name__)
app.secret_key = '4567890sdfghjklcvbnvb4567fg6yug'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/QuanLyNhaSach?charset=utf8mb4' % quote('Nam060902@')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['CART_KEY'] = 'cart'

db = SQLAlchemy(app=app)

login = LoginManager(app=app)

cloudinary.config(cloud_name='dtoc5lqfe', api_key='346556316858336', api_secret='ijP4MyTWOXI-behy-Z3TUso5UAA')

babel = Babel(app=app)


@babel.localeselector
def load_locale():
    return "vi"
