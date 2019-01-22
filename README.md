# sentiment-stock-trader

## Purpose

This project is an attempt to classify stock-related tweets in order to predict buy/sell patterns.

## Setup

We are using `python2.7`.

```bash
pip install -r requirements.txt
python -m textblob.download_corpora
```

Add your Twitter API data to a `.env` file in the root directory.

```bash
SST_CONSUMER_KEY="key"
SST_CONSUMER_SECRET="secret"
SST_ACCESS_TOKEN="token"
SST_ACCESS_TOKEN_SECRET="token secret"
```

## Execution

```bash
python main.py
```
