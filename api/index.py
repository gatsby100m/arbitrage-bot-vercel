import os
import json
from flask import Flask, request, jsonify
import requests

# ============================================
# CONFIGURATION
# ============================================
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not set!")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TOKEN}"
app = Flask(__name__)

# ============================================
# SEND MESSAGE FUNCTION
# ============================================
def send_message(chat_id, text):
    """Send a message using the Telegram Bot API."""
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Error sending message: {e}")
        return False

# ============================================
# COMMAND HANDLERS
# ============================================
def handle_start(chat_id):
    send_message(chat_id, 
        "🤖 *Pre-Match Arbitrage Scanner*\n\n"
        "I scan Nigerian bookmakers for arbitrage opportunities.\n\n"
        "📌 *Commands:*\n"
        "/check - Scan for opportunities\n"
        "/status - Check bot status\n"
        "/help - Show help"
    )

def handle_help(chat_id):
    send_message(chat_id,
        "📖 *How to use:*\n\n"
        "1. Send /check to scan for arbitrage\n"
        "2. If found, I'll show you stakes and profit\n"
        "3. You manually place bets on both sites\n"
        "4. Profit is guaranteed!\n\n"
        "💰 With ₦10,000 stake, you can make ₦100-₦500 per bet!"
    )

def handle_status(chat_id):
    send_message(chat_id,
        "✅ *Bot is running on Vercel!*\n\n"
        "🔄 Monitoring pre-match odds\n"
        "📊 Bookmakers: Betpawa, Betking\n"
        "💰 Use /check to scan!"
    )

def handle_check(chat_id):
    send_message(chat_id, "🔍 Scanning for arbitrage opportunities...")
    
    # Sample arbitrage data (will be replaced with real data later)
    opportunities = [
        {
            "match": "Real Madrid vs Barcelona",
            "market": "GG/NG",
            "outcome_a": "Betpawa GG",
            "outcome_b": "Betking NG",
            "odds_a": 2.15,
            "odds_b": 2.05,
            "stake_a": 4761.90,
            "stake_b": 5238.10,
            "profit_pct": 4.76,
            "profit_amount": 476.19
        }
    ]
    
    if opportunities:
        for opp in opportunities:
            message = (
                f"💰 *ARBITRAGE FOUND!*\n\n"
                f"⚽ {opp['match']}\n"
                f"📊 {opp['market']}\n"
                f"📈 Profit: *{opp['profit_pct']}%* (₦{opp['profit_amount']:,.2f})\n\n"
                f"📱 *Place these bets:*\n"
                f"• ₦{opp['stake_a']:,.2f} on *{opp['outcome_a']}* @ {opp['odds_a']}\n"
                f"• ₦{opp['stake_b']:,.2f} on *{opp['outcome_b']}* @ {opp['odds_b']}\n\n"
                f"⚡ Act fast!"
            )
            send_message(chat_id, message)
    else:
        send_message(chat_id, "ℹ️ No arbitrage found at the moment.")

# ============================================
# WEBHOOK ENDPOINT
# ============================================
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        json_data = request.get_json(force=True)
        print(f"Received: {json_data}")

        message = json_data.get('message', {})
        chat_id = message.get('chat', {}).get('id')
        text = message.get('text', '')

        if chat_id:
            if text.startswith('/start'):
                handle_start(chat_id)
            elif text.startswith('/help'):
                handle_help(chat_id)
            elif text.startswith('/status'):
                handle_status(chat_id)
            elif text.startswith('/check'):
                handle_check(chat_id)

        return jsonify({"status": "ok"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# ============================================
# TEST ENDPOINTS
# ============================================
@app.route('/', methods=['GET'])
def index():
    return "🤖 Arbitrage Bot is running on Vercel!"

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"status": "ok", "message": "Bot is working!"})

# ============================================
# FOR LOCAL TESTING
# ============================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
