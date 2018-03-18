from vkpoll import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(100))

    def __init__(self, user_id, user_token):
        self.id = user_id
        self.token = user_token

    def update(self, user_token):
        self.token = user_token


class Poll(db.Model):
    __tablename__ = 'poll'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)
    title = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    pub_date = db.Column(db.DateTime)

    def __init__(self, url, title, user_id):
        self.url = url
        self.title = title
        self.user_id = user_id
        self.pub_date = datetime.utcnow()


class Choice(db.Model):
    __tablename__ = 'choice'
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'))
    text = db.Column(db.String)

    def __init__(self, poll_id, text):
        self.poll_id = poll_id
        self.text = text


class ChoiceUser(db.Model):
    __tablename__ = 'choice_of_user'
    id = db.Column(db.Integer, primary_key=True)
    choice_id = db.Column(db.Integer, db.ForeignKey('choice.id'))
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, poll_id, choice_id, user_id):
        self.poll_id = poll_id
        self.choice_id = choice_id
        self.user_id = user_id
