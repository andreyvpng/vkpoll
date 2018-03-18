from functools import wraps
from random import choice
from string import ascii_letters

from flask import Blueprint, session, request, redirect, flash, \
    render_template, url_for, abort

from vkpoll import db
from ..forms import CreatePollForm, DeletePollForm, VotePollForm
from ..models import Poll, Choice, ChoiceUser

poll = Blueprint('poll', __name__)


def is_logged(func):
    """ Processing requests for unauthorized users """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('logged_in'):
            flash('You are not authorized!', category='danger')
            return redirect(url_for('index'))
        return func(*args, **kwargs)

    return wrapper


@poll.route('/poll/<url_of_poll>')
def show_poll(url_of_poll):
    current_poll = Poll.query.filter_by(url=url_of_poll).first()
    if not current_poll:
        abort(404)

    options = Choice.query.filter_by(poll_id=current_poll.id).all()

    options_table = [
        {
            'text': option.text,
            'score': len(ChoiceUser.query.filter_by(
                poll_id=current_poll.id,
                choice_id=option.id
            ).all())
        }
        for option in options
    ]

    vote_poll_form = VotePollForm(
        poll_id=current_poll.id,
        poll_url=current_poll.url,
    )

    vote_poll_form.options.choices = [
        (option.id, option.text) for option in options
    ]

    is_user_take_part = ChoiceUser.query.filter_by(
        poll_id=current_poll.id,
        user_id=session.get('id')
    ).all() != []

    return render_template(
        'poll.html',
        poll=current_poll,
        options=options_table,
        DeletePollForm=DeletePollForm(poll_id=current_poll.id),
        VotePollForm=vote_poll_form,
        is_user_take_part=is_user_take_part
    )


@poll.route('/my_polls')
@is_logged
def my_polls():
    polls = Poll.query.filter_by(user_id=session['id']).all()
    return render_template('my_polls.html', polls=polls)


@poll.route('/new', methods=['GET', 'POST'])
@is_logged
def new():
    form = CreatePollForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('add_poll.html', form=form)

        while True:
            url_length = 8
            url_of_poll = ''.join(choice(ascii_letters) for _ in range(
                url_length))

            check_of_poll = Poll.query.filter_by(url=url_of_poll).all()

            if not check_of_poll:
                break

        question = form.title.data
        possible_options = [item for item in form.options.data if item]
        created_poll = Poll(
            url=url_of_poll,
            title=question,
            user_id=session['id']
        )
        db.session.add(created_poll)
        db.session.commit()

        for choice_text in possible_options:
            created_choice = Choice(poll_id=created_poll.id, text=choice_text)
            db.session.add(created_choice)

        db.session.commit()
        flash('Poll successfully created', category='success')
        return redirect(url_for('poll.show_poll', url_of_poll=url_of_poll))
    return render_template('add_poll.html', form=form)


@poll.route('/del', methods=['POST'])
@is_logged
def delete():
    form = DeletePollForm()
    poll_ = Poll.query.filter_by(id=form.poll_id.data).all()
    if not poll_:
        flash('This poll does not exist', category='danger')
    elif poll_[0].user_id == session.get('id'):
        choice_of_users = ChoiceUser.query.filter_by(poll_id=poll_[0].id).all()
        for choice_user in choice_of_users:
            db.session.delete(choice_user)

        options = Choice.query.filter_by(poll_id=poll_[0].id).all()
        for option in options:
            db.session.delete(option)

        db.session.commit()
        db.session.delete(poll_[0])
        db.session.commit()

        flash('Poll successfully deleted', category='success')
    else:
        flash('You do not have the right to remove this poll!',
              category='danger')

    return redirect(url_for('index'))


@poll.route('/make_choice', methods=['POST'])
@is_logged
def make_choice():
    form = VotePollForm()

    check_of_poll = Choice.query.filter_by(
        poll_id=form.poll_id.data,
        id=form.options.data
    ).first()

    if not check_of_poll:
        flash('This poll does not exist', category='danger')
        return redirect(url_for('index'))

    new_choice_user = ChoiceUser(
        poll_id=form.poll_id.data,
        choice_id=form.options.data,
        user_id=session['id']
    )
    db.session.add(new_choice_user)
    db.session.commit()
    return redirect(url_for('poll.show_poll', url_of_poll=form.poll_url.data))
