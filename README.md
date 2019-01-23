# sentiment-stock-trader

## Purpose

This project is an attempt to classify stock-related tweets in order to predict buy/sell patterns.

## Setup

We are using `python3.7`.

```bash
pip3 install -r requirements.txt
python3 -m textblob.download_corpora
```

Add your Twitter API data to a `.env` file in the root directory.

```bash

# Twitter creds
SST_CONSUMER_KEY="key"
SST_CONSUMER_SECRET="secret"
SST_ACCESS_TOKEN="token"
SST_ACCESS_TOKEN_SECRET="token secret"

# MongoDB creds
SST_DB_USER="user"
SST_DB_PASSWORD="password"
SST_DB_URI="uri"

# Alpaca creds
AL_ENDPOINT="https://paper-api.alpaca.markets"
AL_KEY="key"
AL_SECRET="secret"

```

## Execution

```bash
python3 main.py
```
