# -*- coding: utf-8 -*-
# from sqlalchemy import db.Column, db.Integer, String, ForeignKey, DateTime, Table, PrimaryKeyConstraint
# from sqlalchemy.orm import relationship
# from database import Base
from datetime import datetime
from HotOpinion import db


respondents_identifier = db.Table('respondents_identifier',
                                  db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                                  db.Column('poll_id', db.Integer, db.ForeignKey('poll.id')),
                                  )


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))  # User Name
    name_string = db.Column(db.String(100), unique=True)  # User email
    attended_polls = db.relationship('Poll', secondary=respondents_identifier, backref='User')

    def __init__(self, name=None, name_string=None):
        self.name = name
        self.name_string = name_string

    def __repr__(self):
        return 'User %r' % self.name


class Poll(db.Model):
    __tablename__ = 'poll'
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(50))
    question_statement = db.Column(db.Text, nullable=False)
    num_questions = db.Column(db.Integer)  # 응답지 개수
    total_participant = db.Column(db.Integer)  # 총 참여자 수
    questions = db.relationship('Question', backref='Poll')
    comments = db.relationship('Comment', backref='Poll')

    def __init__(self, subject=None, question_statement=None, num_questions=2):
        self.subject = subject
        self.question_statement = question_statement
        self.num_questions = num_questions
        self.total_participant = 0

    def __repr__(self):
        return "poll%d" % self.id


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    choice_num = db.Column(db.Integer)
    answer_description = db.Column(db.Text, nullable=False)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'))
    selected_num = db.Column(db.Integer)  # 선택된 수

    def __init__(self, choice_num, answer_description=None):
        self.choice_num = choice_num
        self.answer_description = answer_description
        self.selected_num = 0

    def __repr__(self):
        return 'Question %d' % self.choice_num

    def set_poll_id(self, poll):
        self.poll_id = poll.id


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    comment_content = db.Column(db.String(200))
    user_name = db.Column(db.String(20))
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'))
    comment_time = db.Column(db.DateTime)

    def __init__(self, user_name, comment_content):
        self.user_name = user_name
        self.comment_content = comment_content
        self.comment_time = datetime.now()

    def update_time(self):
        self.comment_time = datetime.now()
