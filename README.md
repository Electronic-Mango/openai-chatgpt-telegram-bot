# Simple OpenAI text model Telegram bot

A simple and unofficial Telegram bot wrapping [OpenAI API](https://openai.com/blog/openai-api/) text models (like [ChatGPT](https://openai.com/blog/chatgpt)), build with [`python-telegram-bot`](https://github.com/python-telegram-bot/python-telegram-bot)!

Just start a conversation and all messages in the chat will be used as inputs for ChatGPT.

Conversation/context is not stored permanently and will be removed when the bot is restarted.



## Requirements

This bot was built with `Python 3.11`, [`python-telegram-bot`](https://github.com/python-telegram-bot/python-telegram-bot) and [`openai-python`](https://github.com/openai/openai-python).
Full list of Python requirements is in the `requirements.txt` file, you can use it to install all of them.



## Configuration

Configuration is done through a `.env` file. You can copy example file `.env.example` as `.env` and fill required parameters.

```commandline
cp .env.example .env
```


### Telegram bot

Only required parameter is a [bot token](https://core.telegram.org/bots#creating-a-new-bot).

You can also restrict who can access the bot via `ALLOWED_USERNAMES`.
You can specify multiple usernames delimited by space.
If you don't want to restrict the bot at all you can remove this parameter or leave it empty.

You can also define max response length in characters via `MAX_MESSAGE_LENGTH`.
Bot responses can be up to 4096 characters long, that value is used by default if this parameter is absent.

```dotenv
BOT_TOKEN='<your secret bot token>'
ALLOWED_USERNAMES='myusername friendusername'
MAX_MESSAGE_LENGTH=<custom max response length>
```


### OpenAI API

One required parameter is [API key](https://platform.openai.com/account/api-keys).

```dotenv
OPENAI_TOKEN='<your secret API key>'
```

Through `.env` you can also configure other parameters:
* `OPENAI_MODEL` - which model to use (gpt-3.5-turbo is used by default)
* `OPENAI_SYSTEM_MESSAGE` - system message
* `OPENAI_CONTEXT_LIMIT` - how many messages will be kept in the context aside from prompt, all messages will be kept if empty
* `OPENAI_INITIAL_MESSAGE` - additional message added after system message to all conversations, can be empty for no additional messages
* `OPENAI_LOG` - log level of OpenAI API, either `debug` or `info`, can be empty for no additional logging configuration

Note that `gpt-3.5-turbo` [doesn't pay strong attention to system message](https://platform.openai.com/docs/guides/chat/instructing-chat-models), so changing it might not provide significant changes to responses.
You can use `OPENAI_INITIAL_MESSAGE` to tweak initial behaviour of the model.

```dotenv
OPENAI_MODEL='gpt-3.5-turbo'
OPENAI_SYSTEM_MESSAGE='You are a helpful assistant.'
OPENAI_CONTEXT_LIMIT=1000
OPENAI_INITIAL_MESSAGE='You are a helpful assistant acting like 18th century butler,'
OPENAI_LOG='info'
```


## Commands

* `/start` - prints initial message returned from the model for just system message and optional initial message, doesn't impact conversation context
* `/reset` - resets current conversation and removes all context, other than system message
* `/promptset` - set new custom prompt, changes both system message and custom initial message (overwrites both `OPENAI_SYSTEM_MESSAGE` and `OPENAI_INITIAL_MESSAGE`)
* `/promptreset` - restore prompt to default
* `/promptget` - get custom prompt, won't respond with default one to avoid leaking configuration to users
* `/promptremove` - force-remove any prompts from the conversation, including one defined in configuration files
* `/cancel` - cancels ongoing operation, applies only to `/promptset`


## Running the bot

You can run the bot from the source code directly, or in a Docker container.


### From source code

1. Create a Telegram bot via [BotFather](https://core.telegram.org/bots#6-botfather)
2. Create [OpenAI API key](https://platform.openai.com/account/api-keys)
3. Install all packages from `requirements.txt`
4. Fill `.env` file
5. Run `main.py` file with Python


### Docker

1. Create a Telegram bot via [BotFather](https://core.telegram.org/bots#6-botfather)
2. Create [OpenAI API key](https://platform.openai.com/account/api-keys)
3. Fill `.env` file
4. Run `docker compose up -d --build` in terminal

Note that `.env` file is used only for loading environment variables into Docker container through compose.
The file itself isn't added to the container.



## Vision

Bot can respond to messages containing a **single** photo.
Uploading more photos will result in bot responding to each one separately.
Other messages than photo or text are ignored.


## Disclaimer

This bot is in no way affiliated, associated, authorized, endorsed by, or in any way officially connected with OpenAI.
This is an independent and unofficial project.
Use at your own risk.
