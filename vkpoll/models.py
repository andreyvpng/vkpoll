from vkpoll import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(100))

    def __init__(self, user_id, token):
        self.id = user_id
        self.token = token

    def update(self, user_token):
        self.token = user_token


class Poll(db.Model):
    __tablename__ = 'poll'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)
    title = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    pub_date = db.Column(db.DateTime, nullable=False,
                         default=db.func.current_timestamp())


class Choice(db.Model):
    __tablename__ = 'choice'
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'))
    text = db.Column(db.String)


class ChoiceUser(db.Model):
    __tablename__ = 'choice_of_user'
    id = db.Column(db.Integer, primary_key=True)
    choice_id = db.Column(db.Integer, db.ForeignKey('choice.id'))
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
