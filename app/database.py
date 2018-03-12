import psycopg2
import psycopg2.extras


class DataBase:

    def __init__(self, app):
        self.db = psycopg2.connect(
            database=app.config['DATABASE_NAME'],
            user=app.config['DATABASE_USER'],
            password=app.config['DATABASE_PASSWORD'],
            host=app.config['DATABASE_HOST'],
            port=app.config['DATABASE_PORT']
        )
        self.cursor = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def init_db(self, app):
        with app.open_resource('schema.sql', mode='r') as f:
            self.cursor.execute(f.read())
        self.db.commit()

    def create_new_user(self, user_id, user_token):
        self.cursor.execute(
            'insert into USERS (id, token) values(%s, %s)',
            [user_id, user_token]
        )
        self.db.commit()

    def update_token_of_user(self, user_id, user_token):
        self.cursor.execute(
            'update USERS set token = (%s) where id = (%s)',
            [user_id, user_token]
        )
        self.db.commit()

    def get_user(self, user_id):
        self.cursor.execute('select *from USERS where id = (%s)', [user_id])
        user = self.cursor.fetchall()
        return user

    def get_polls_of_user(self, user_id):
        self.cursor.execute('select * from polls where user_id = (%s)', [user_id])
        polls = self.cursor.fetchall()
        return polls

    def create_possible_choice(self, poll_id, text):
        self.cursor.execute(
            'insert into possible_choice(poll_id, text) values(%s, %s)',
            [poll_id, text]
        )
        self.db.commit()

    def create_new_poll(self, poll_url, user_id, poll_question, choices):
        self.cursor.execute(
            "insert into polls (url, user_id, question) values(%s, %s, %s)",
            [poll_url, user_id, poll_question]
        )
        self.cursor.execute('select *from polls where url = (%s)', [poll_url])
        poll_id = self.cursor.fetchall()[0]['id']
        for possible_choice in choices:
            if possible_choice:
                self.create_possible_choice(poll_id, possible_choice)
        self.db.commit()

    def get_poll_via_url(self, url_of_poll):
        self.cursor.execute('select *from polls where url = (%s)', [url_of_poll])
        poll = self.cursor.fetchall()
        if poll:
            return poll[0]
        return dict()

    def get_poll_via_id(self, poll_id):
        self.cursor.execute('select *from polls where id = (%s)', [poll_id])
        poll = self.cursor.fetchall()
        if poll:
            return poll[0]
        return dict()

    def delete_poll(self, poll_id):
        self.cursor.execute(
            'delete from user_choice where poll_id = (%s)',
            [poll_id]
        )
        self.cursor.execute(
            'delete from possible_choice where poll_id = (%s)',
            [poll_id]
        )
        self.cursor.execute('delete from polls where id = (%s)', [poll_id])
        self.db.commit()

    def get_possible_choice(self, poll_id):
        self.cursor.execute(
            'select * from possible_choice where poll_id = (%s)',
            [poll_id]
        )
        options = self.cursor.fetchall()
        ans = dict()
        for option in options:
            self.cursor.execute(
                'select user_id from user_choice where poll_id = (%s) and choice_id= (%s);',
                [option['poll_id'], option['id']]
            )

            users = [item[0] for item in self.cursor.fetchall()]
            ans[option['text']] = {
                'id': option['id'],
                'users': users,
                'count': len(users)
            }
        return ans

    def is_user_take_part(self, user_id, poll_id):
        self.cursor.execute(
            'select choice_id from user_choice where user_id = (%s) and poll_id = (%s)',
            [user_id, poll_id]
        )
        """
            if the user does not participate, this return [], else this return
            [ [ <number_of_choice_id> ] ]
        """
        choice_id = self.cursor.fetchall()
        if choice_id:
            return choice_id[0][0]
        return None

    def create_choice(self, user_id, poll_id, choice_id):
        self.cursor.execute(
            'insert into user_choice(user_id, poll_id, choice_id) values(%s, %s, %s)',
            [user_id, poll_id, choice_id]
        )
        self.db.commit()

    def is_url_available(self, url):
        self.cursor.execute('select *from polls where url = (%s)', [url])
        poll = self.cursor.fetchall()
        return len(poll) == 0

    def get_stat(self):
        stats = dict()
        self.cursor.execute("""
            SELECT
                tablename
            FROM
                pg_catalog.pg_tables
            WHERE
                schemaname != 'pg_catalog'
            AND schemaname != 'information_schema';
        """)
        tablenames = self.cursor.fetchall()
        for tablename in tablenames:
            name = tablename[0]
            # why dont work this?
            # self.cursor.execute('select count(*) from (%s)', [name])
            self.cursor.execute('select count(*) from {0}'.format(name))
            stats[name] = self.cursor.fetchall()[0][0]

        return stats
