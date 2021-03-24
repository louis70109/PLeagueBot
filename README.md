# P+ League LINE Chatbot

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-%3E%3D%203.5-blue.svg)](https://badge.fury.io/py/lotify)

![](https://i.imgur.com/8FwPz53.png)

<img height="200" border="0" alt="QRcode" src="https://qr-official.line.me/sid/L/611lsquw.png">

<a href="https://line.me/R/ti/p/%40611lsquw"><img height="50" border="0" alt="加入好友" src="https://scdn.line-apps.com/n/line_add_friends/btn/zh-Hant.png"></a>

# Prerequisite

- flask/Python 3.8
- LINE v10.14
- PostgreSQL

> You need Github, LINE, Heroku accounts to deploy this bot.

# Developer Side

## Environment property

These properties are need to export in environment.

```
LINE_CHANNEL_ACCESS_TOKEN=
LINE_CHANNEL_SECRET=
DATABASE_URL=postgres://USER:PASSWORD@127.0.0.1:5432/postgres
```

> You need to modify DATABASE_URL as your postgresql settings.

## LINE account (LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET)

- Got A LINE Bot API developer account
  Make sure you already registered, if you need use LINE Bot.

* Go to LINE Developer Console
  - Close auto-reply setting on "Messaging API" Tab.
  - Setup your basic account information. Here is some info you will need to know.
    - Callback URL: `https://{YOUR_URL}/webhooks/line`
    - Verify your webhook.
* You will get following info, need fill back to `.env` file.
  - Channel Secret
  - Channel Access Token (You need to issue one here)

## Local testing

Run `Scripts/` profiles first, sync official website data to database as crawler.

1. first terminal window

```
cp .env.example .env

# By docker (choose one)
docker-compose up

# By localized (choose one)
pip install -r requirements.txt --user
python api.py
```

2. Create a provisional Https:

```
ngrok http 5000
```

or maybe you have npm environment:

```
npx ngrok http 5000
```

![](https://i.imgur.com/azVdG8j.png)

3. Copy url to LINE Developer Console

## Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

- Enable `clock` button to schedule corn.

![](https://i.imgur.com/iA0dvI9.png)

- Add `Heroku Postgres` and it would create `DATABASE_URL` environment variable automatically.

![](https://i.imgur.com/wCFeUlu.png)

If you are not sure where are files in, use following up commands:

```
heroku run bash
heroku logs --tail
```

# License

MIT License
