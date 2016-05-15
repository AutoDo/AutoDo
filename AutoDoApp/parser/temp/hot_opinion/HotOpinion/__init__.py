from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect
from flask_restless.manager import APIManager
import config


csrf = CsrfProtect()

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = config.MYSQL_URI
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['POSTS_PER_PAGE'] = config.POST_PER_PAGE
app.config['COMMENTS_PER_PAGE'] = config.COMMENT_PER_PAGE
app.config['SUPER_USER_EMAIL'] = config.SUPER_USER_EMAIL
db = SQLAlchemy(app)


from HotOpinion.models import Poll, Question, Comment, User

manager = APIManager(app=app,
                     flask_sqlalchemy_db=db
                     )
manager.create_api(Poll, methods=['GET', 'POST'], results_per_page=3)
manager.create_api(Question, methods=['GET', 'POST'])
manager.create_api(Comment, methods=['GET', 'POST'])
manager.create_api(User, methods=['GET', 'POST'])

csrf.init_app(app)

import HotOpinion.contollers
