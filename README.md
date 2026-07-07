# OmniMap Telegram Bot

A Telegram bot for the **OmniMap** platform — work with your maps from Telegram.
One microservice in the OmniMap platform (see
[omnimap-back](https://github.com/PavelNikolaeW/omnimap-back) and
[omnimap-front](https://github.com/PavelNikolaeW/omnimap-front)).

## Stack

Python · Telegram Bot API · pytest

## Run

```bash
pip install -r requirements.txt
# set the bot token via environment (see .env / your config)
python -m bot            # entrypoint lives under bot/
pytest tests/ -v         # tests
```
