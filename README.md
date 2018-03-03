# VKPOLL
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
    set DATABASE_NAME=<put_your_settings>
    set DATABASE_USER=<put_your_settings>
    set DATABASE_PASSWORD=<put_your_settings>
    set DATABASE_HOST=<put_your_settings>
    set DATABASE_PORT=<put_your_settings>

    set VK_API_ID=<put_your_settings>
    set VK_API_SECRET=<put_your_settings>
    set VK_API_URL=<put_your_settings>

Initial database(For first run)

    flask init_db

For run app:

    flask run
