# VKPOLL

> Web application for creating private voting with authorization via VK.

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/ec5d951423a34c7cbc3756d27ac88961)](https://app.codacy.com/app/varf.andrey/vkpoll?utm_source=github.com&utm_medium=referral&utm_content=andreyvpng/vkpoll&utm_campaign=badger)
[![Build Status](https://travis-ci.org/andreyvpng/vkpoll.svg?branch=master)](https://travis-ci.org/andreyvpng/vkpoll)


### Create Poll
Create simple poll in order to know the opinions of people

### Share!
Each poll creates a private link. Share it in the dialogs!


### How to deploy

> If you use linux instead of 'set', write 'export'

```
git clone https://github.com/andreyvpng/vkpoll.git
cd vkpoll
pip install -r requirements.txt

set FLASK_APP=run.py
set DATABASE_URL=<URL LINK TO DATABASE>
```
    
Register an application for use API you can [here](https://vk.com/editapp?act=create).
Choose a website platform. The site address should be as follows: http://yoursite.com/auth/get_token

```commandline
set VK_API_ID=<put_your_application_id>
set VK_API_SECRET=<put_your_secure_key>
set VK_API_URL=<put_your_site_address>
```

Init database(for first run)
```commandline
flask db upgrade
```

Run application

```commandline
flask run
``` 
#### TODO:
- improve code style
- write tests


### License

Copyright (c) 2018, Andrey Varfolomeev. All rights reserved.

Licensed under the BSD 2-Clause License