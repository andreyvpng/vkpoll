# VKPOLL

# THIS IS OLD VERSION WITHOUT EXTENSIONS

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/ec5d951423a34c7cbc3756d27ac88961)](https://app.codacy.com/app/varf.andrey/vkpoll?utm_source=github.com&utm_medium=referral&utm_content=andreyvpng/vkpoll&utm_campaign=badger)
[![Build Status](https://travis-ci.org/andreyvpng/vkpoll.svg?branch=master)](https://travis-ci.org/andreyvpng/vkpoll)

> Web application for creating private voting with authorization via VK.
> Created polls are available on a private link.

In VK you can create polls only on the wall of personal or public page. Which is not convenient if you want to know the opinion in the conference. The application solves this problem.

### How to deploy

The project uses [postgresql](https://www.postgresql.org/) databases, so you need to create a database and run the server.


> If you use linux instead of 'set', write 'export'

    git clone https://github.com/andreyvpng/vkpoll.git
    cd vkpoll
    pip install -r requirements.txt

    set FLASK_APP=main.py
    set FLASK_DEBUG=<false or true>
    set DATABASE_URL=postgresql://[user[:password]@][netloc][:port][/dbname]

    set VK_API_ID=<put_your_settings>
    set VK_API_SECRET=<put_your_settings>
    set VK_API_URL=<put_your_settings>

Initial database(For first run)

    flask init_db

For run app:

    flask run

For run tests:

    python -m unittest tests\test_app.py
