# Telegram Finance Alert Bot

A Python-based Telegram bot that monitors global financial markets and sends
real-time alerts when relevant assets cross predefined thresholds.

This project was built as a personal initiative to practice:
- Financial data handling
- State-aware alert systems
- Clean and maintainable project architecture
- Deploying long-running services on cloud platforms

---

## Features

- Real-time alerts when assets cross positive or negative thresholds
- Persistent state system to avoid repeated notifications
- Market open and close notifications (Europe and US grouped)
- Automatic daily reset of alert state
- Supports indices, commodities and cryptocurrencies
- Deployed as a Render-compatible web service

---

## Assets Monitored

- S&P 500  
- NASDAQ  
- MSCI World  
- MSCI Emerging Markets  
- Gold  
- Silver  
- Bitcoin (EUR)

---

## Project Structure

```text
telegram-finance-bot/
│
├── bot.py              # Main application loop
├── config.py           # Environment variables & configuration
├── requirements.txt
├── README.md
└── utils/
    ├── data.py         # Market data retrieval
    ├── alerts.py       # Threshold-based alert logic with state memory
    └── summary.py      # Telegram message formatting
```

---

## How It Works

1. Market data is periodically fetched using `yfinance`
2. Price variations are calculated against previous close or daily open
3. Alerts are triggered only when a defined threshold is crossed
4. Alert states are stored locally in a JSON file to prevent duplicates
5. The state resets automatically once per day before market open

---

## Why This Project

I built this bot to receive meaningful daily market information without having
to actively search for it.

Instead of constantly checking prices, the bot notifies me only when something
relevant happens: significant movements, extreme volatility, or market
open/close events.

The focus of this project is not prediction, but **signal over noise**.

---

## Run Locally

```bash
pip install -r requirements.txt
python bot.py
```

The following environment variables must be defined:
- TELEGRAM_TOKEN
- USER_CHAT_ID

## Example Output

### Market open notifications

```
Europe (LSE & XETRA) markets have opened.
Opening prices (24/12/2025 08:00)

S&P 500: +0.46%
NASDAQ: +0.57%
MSCI World: +0.49%
Gold: +0.23%
Bitcoin: -0.52%
```
### Alert notifications
```
NASDAQ rises 2.59% today (EXTREME MOVE)
```
## Deployment Notes

The bot is deployed on Render using a free web service.

Since free instances automatically spin down after inactivity, an external
monitoring service periodically pings the application endpoint to keep it
running continuously without requiring a paid background worker.

## Disclaimer

This project is for educational and informational purposes only.
It does not constitute financial advice, investment recommendations, or
market predictions.