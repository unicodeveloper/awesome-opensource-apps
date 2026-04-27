![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) 
![Status](https://img.shields.io/badge/Status-Active%20Automation-success?style=for-the-badge) 
![Focus](https://img.shields.io/badge/Focus-Financial%20Monitoring-blue?style=for-the-badge)



# 🏛️ SG Financial Monitor (Python Edition)
**SG Financial Monitor** is a professional-grade Telegram bot written entirely in **Python**. It serves as a strategic intelligence terminal, fetching live market data and performing real-time technical analysis using industry-standard Python data libraries.
### 🐍 Python Technical Stack
This project leverages the power of Python to handle complex data streams and mathematical calculations:
 * **pyTelegramBotAPI**: For high-speed, asynchronous communication with the Telegram Bot API.
 * **Pandas**: The core "analytical brain" used to process price dataframes and calculate technical indicators.
 * **Requests**: For robust API polling from global financial sources (Binance, CoinGecko, Yahoo Finance).
### 🧠 The Logic: How RSI is Calculated in Python
The bot calculates the **Relative Strength Index (RSI)** by processing the last 100 hours of market data through a custom Python function:
 1. **Data Acquisition**: It fetches a JSON payload of the last 100 hourly "Klines" (candlesticks).
 2. **Series Conversion**: Python’s pandas.Series converts raw strings into floating-point numbers for math operations.
 3. **Calculating Deltas**: Using closes.diff(), Python finds the price change between each hour.
 4. **Smoothing**: It applies a **14-period rolling mean** to separate "Gains" from "Losses."
 5. **The Formula**:
   
### ⚙️ Installation Requirements
To run this bot, you must have **Python 3.10** or higher installed on your system (PC, Mac, or Termux).
**1. Install the required Python packages:**
```bash
pip install pyTelegramBotAPI pandas requests

```
**2. Configure the script:**
Open sgfinfree.py in your code editor and insert your API_TOKEN.
**3. Launch the terminal:**
```bash
python sgfinfree.py

```
### 📊 Strategic Indicators Provided
 * **RSI (1h):** Identifies if an asset is Overbought (>70) or Oversold (<30).
 * **24h Range Position:** A mathematical calculation showing where the current price sits relative to the day's High and Low.
 * **Market Status:** Automated logic that translates raw Python data into "Bullish," "Bearish," or "Neutral" labels.
### ⚖️ Disclaimer
*This code is a tool for informational purposes. It is written in Python for speed and accuracy, but it does not constitute financial advice. Use the data as a reference for your own strategic analysis.*
