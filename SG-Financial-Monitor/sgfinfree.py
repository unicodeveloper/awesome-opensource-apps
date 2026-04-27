import telebot
import requests
import pandas as pd

# --- CONFIGURATION ---
# Replace with your token from @BotFather
API_TOKEN='Write your API Token here'
bot = telebot.TeleBot(API_TOKEN)

# --- ANALYTICAL BRAIN ---

def calculate_rsi(symbol):
    """Calculates RSI using the last 100 hours of Binance data."""
    try:
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}USDT&interval=1h&limit=100"
        data = requests.get(url, timeout=5).json()
        closes = pd.Series([float(x[4]) for x in data])
        delta = closes.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return f"{rsi.iloc[-1]:.2f}"
    except: return "N/A"

def get_strategy_label(rsi, range_pos):
    """Translates raw numbers into strategic advice."""
    analysis = ""
    if rsi != "N/A":
        val = float(rsi)
        if val > 70: analysis += "⚠️ *OVERBOUGHT:* Market is overheated. Correction likely.\n"
        elif val < 30: analysis += "✅ *OVERSOLD:* High value zone. Potential bounce.\n"
        else: analysis += "⚖️ *STABLE:* Momentum is currently neutral.\n"
    
    if range_pos > 85: analysis += "🚀 *RESISTANCE:* Testing the daily ceiling.\n"
    elif range_pos < 15: analysis += "🛡️ *SUPPORT:* Testing the daily floor.\n"
    
    return analysis if analysis else "📊 *SIDEWAYS:* Market is consolidating."

# --- COMMAND HANDLERS ---

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    # This creates the 'Grey Text' placeholder in the message box
    markup = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True, 
        input_field_placeholder="Type /p [ticker] here..."
    )
    
    welcome_text = (
        "🏦 *Welcome to SG Financial Monitor*\n"
        "──────────────────\n"
        "Strategic Intelligence Terminal for active market monitoring.\n\n"
        "🛠 *How to use:*\n"
        "Simply type `/p` followed by any asset name or ticker.\n\n"
        "🔹 *Crypto:* `/p xrp` | `/p cardano` | `/p bitcoin`\n"
        "🔹 *Stocks:* `/p tsla` | `/p nvda` | `/p apple`\n\n"
        "📊 *Indicators Included:*\n"
        "• Real-time Price & 24h Change\n"
        "• RSI (1h) Momentum Analysis\n"
        "• Global Market Ranking (Crypto)\n"
        "• 52-Week Range Context (Stocks)\n"
        "──────────────────\n"
        "⚠️ *DISCLAIMER:* This is an automated monitoring tool. Content does NOT constitute financial advice. Trade at your own risk."
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(commands=['p'])
def handle_price(message):
    query = message.text.replace('/p ', '').strip()
    if not query or query == "/p":
        bot.reply_to(message, "Please enter an asset. Example: `/p xrp`")
        return

    bot.send_chat_action(message.chat.id, 'typing')

    # 1. ATTEMPT CRYPTO (Binance + CoinGecko)
    try:
        # Search for ID (allows searching by name like 'Ripple')
        s_res = requests.get(f"https://api.coingecko.com/api/v3/search?query={query}", timeout=5).json()
        if s_res['coins']:
            c = s_res['coins'][0]
            m_res = requests.get(f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={c['id']}", timeout=5).json()
            if m_res:
                m = m_res[0]
                rsi = calculate_rsi(c['symbol'].upper())
                # Calculate Daily Range Position
                r_pos = ((m['current_price'] - m['low_24h']) / (m['high_24h'] - m['low_24h'])) * 100 if (m['high_24h'] - m['low_24h']) != 0 else 50
                strategy = get_strategy_label(rsi, r_pos)

                resp = (
                    f"🏦 *SG Financial Monitor*\n"
                    f"──────────────────\n"
                    f"🪙 *Asset:* {m['name']} ({c['symbol'].upper()})\n"
                    f"💰 *Price:* ${m['current_price']:,.4f} ({m['price_change_percentage_24h']:.2f}%)\n"
                    f"🏆 *Rank:* #{m['market_cap_rank']} | *RSI:* {rsi}\n"
                    f"📊 *Range Pos:* {r_pos:.1f}%\n"
                    f"──────────────────\n"
                    f"🧠 *STRATEGIC ANALYSIS:*\n{strategy}\n"
                    f"──────────────────\n"
                    f"📍 *Source:* CoinGecko + Binance Intelligence\n"
                    f"\n ⚖️ Not financial advice. Informational only.\n📢 Share the Alpha: Forward this briefing."
                )
                bot.reply_to(message, resp, parse_mode="Markdown")
                return
    except Exception as e: pass

    # 2. ATTEMPT STOCKS (Yahoo Finance)
    try:
        y_url = f"https://query1.finance.yahoo.com/v8/finance/chart/{query.upper()}"
        res = requests.get(y_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5).json()
        meta = res['chart']['result'][0]['meta']
        price = meta['regularMarketPrice']
        change = ((price - meta['previousClose']) / meta['previousClose']) * 100
        
        resp = (
            f"🏛️ *SG Financial Monitor*\n"
            f"──────────────────\n"
            f"📈 *Stock:* {query.upper()}\n"
            f"💵 *Price:* ${price:,.2f} ({change:+.2f}%)\n"
            f"🗓️ *Prev Close:* ${meta['previousClose']:,.2f}\n"
            f"──────────────────\n"
            f"🧠 *MARKET STATUS:* {'📈 Bullish' if change > 0 else '📉 Bearish'}\n"
            f"──────────────────\n"
            f"📍 *Source:* Yahoo Finance Intelligence\n"
            f"\n⚖️ Not financial advice. Informational only.\n📢 Share the Alpha: Forward this briefing."
        )
        bot.reply_to(message, resp, parse_mode="Markdown")
    except:
        bot.reply_to(message, "❌ *Asset Not Found.* Please check the ticker and try again.")

# --- START POLLING ---
print("--- SG Financial Monitor is LIVE ---")
bot.polling(none_stop=True)

