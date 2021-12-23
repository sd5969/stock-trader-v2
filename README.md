# stock-trader-v2

## Purpose

This project is another stock trader running a simple proprietary algorithm.

## Setup

We are using `python3.7`.

```bash
cd monitor
pip3 install -r requirements.txt
python3 -m textblob.download_corpora

cd ../trade
pip3 install -r requirements.txt
```

Add your Twitter API data to a `.env` file in the `monitor` and `trade` directories.

```bash

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

Execute the trade application:

```bash
python3 trade/main.py
```
