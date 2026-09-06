import os
import json
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
import requests

app = Flask(__name__)

# ============================================
# SAMPLE ARBITRAGE DATA
# ============================================
def get_arbitrage_opportunities():
    """Returns pre-match arbitrage opportunities."""
    
    current_time = datetime.now().strftime("%H:%M")
    
    # Sample data (will be replaced with real API calls later)
    opportunities = [
        {
            "match": "Real Madrid vs Barcelona",
            "league": "La Liga",
            "market": "GG/NG",
            "bookie_a": "Betpawa",
            "odds_a": 2.15,
            "bookie_b": "Betking",
            "odds_b": 2.05,
            "stake_a": 4761.90,
            "stake_b": 5238.10,
            "profit_pct": 4.76,
            "profit_amount": 476.19,
            "match_time": "15:00",
            "started": current_time > "15:00"
        },
        {
            "match": "Man United vs Liverpool",
            "league": "Premier League",
            "market": "Over/Under 2.5",
            "bookie_a": "Betpawa",
            "odds_a": 1.95,
            "bookie_b": "Betking",
            "odds_b": 2.10,
            "stake_a": 5185.00,
            "stake_b": 4815.00,
            "profit_pct": 2.43,
            "profit_amount": 243.00,
            "match_time": "17:30",
            "started": current_time > "17:30"
        }
    ]
    
    # Filter out matches that have started
    return [opp for opp in opportunities if not opp["started"]]

# ============================================
# HTML TEMPLATE
# ============================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pre-Match Arbitrage Scanner</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, sans-serif; }
        body { background: #0a0a0a; padding: 16px; color: #fff; }
        .container { max-width: 800px; margin: 0 auto; }
        h1 { font-size: 24px; margin-bottom: 8px; color: #00d4ff; }
        .subtitle { color: #888; font-size: 14px; margin-bottom: 20px; }
        .match-card {
            background: #1a1a1a;
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 16px;
            border-left: 4px solid #00d4ff;
        }
        .match-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }
        .match-name { font-size: 18px; font-weight: 600; }
        .league { color: #888; font-size: 14px; }
        .market { color: #00d4ff; font-size: 14px; font-weight: 500; }
        .odds-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin: 12px 0;
        }
        .odds-box {
            background: #222;
            padding: 12px;
            border-radius: 8px;
            text-align: center;
        }
        .odds-box .bookie { color: #888; font-size: 12px; }
        .odds-box .odds { font-size: 24px; font-weight: 700; color: #fff; }
        .odds-box .stake { color: #aaa; font-size: 12px; }
        .profit-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 12px;
            padding-top: 12px;
            border-top: 1px solid #333;
        }
        .profit-pct { color: #00ff88; font-size: 20px; font-weight: 700; }
        .profit-amount { color: #00ff88; font-size: 16px; }
        .match-time { color: #888; font-size: 12px; }
        .live-indicator {
            background: #ff4444;
            color: #fff;
            padding: 2px 10px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
        }
        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: #666;
        }
        .empty-state .icon { font-size: 48px; margin-bottom: 16px; }
        .refresh-note {
            color: #555;
            font-size: 12px;
            text-align: center;
            margin-top: 20px;
        }
        .auto-refresh { color: #00d4ff; }
        .status-badge {
            background: #00ff88;
            color: #000;
            padding: 2px 10px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
        }
        .badge-active { background: #00ff88; color: #000; }
        .badge-inactive { background: #888; color: #fff; }
    </style>
</head>
<body>
    <div class="container">
        <h1>⚽ Pre-Match Arbitrage Scanner</h1>
        <div class="subtitle">
            Live opportunities from Nigerian bookmakers
            <span class="status-badge badge-active">● LIVE</span>
        </div>
        
        <div id="opportunities">
            {% if opportunities %}
                {% for opp in opportunities %}
                <div class="match-card">
                    <div class="match-header">
                        <div>
                            <div class="match-name">{{ opp.match }}</div>
                            <div class="league">{{ opp.league }}</div>
                        </div>
                        <div>
                            <span class="market">{{ opp.market }}</span>
                            <span class="match-time">⏰ {{ opp.match_time }}</span>
                        </div>
                    </div>
                    
                    <div class="odds-row">
                        <div class="odds-box">
                            <div class="bookie">{{ opp.bookie_a }}</div>
                            <div class="odds">{{ opp.odds_a }}</div>
                            <div class="stake">Stake: ₦{{ opp.stake_a|round(2) }}</div>
                        </div>
                        <div class="odds-box">
                            <div class="bookie">{{ opp.bookie_b }}</div>
                            <div class="odds">{{ opp.odds_b }}</div>
                            <div class="stake">Stake: ₦{{ opp.stake_b|round(2) }}</div>
                        </div>
                    </div>
                    
                    <div class="profit-row">
                        <div>
                            <span class="profit-pct">+{{ opp.profit_pct }}%</span>
                            <span class="profit-amount">(₦{{ opp.profit_amount|round(2) }})</span>
                        </div>
                        <div>
                            <span style="color:#888;font-size:12px;">Guaranteed Profit</span>
                        </div>
                    </div>
                </div>
                {% endfor %}
            {% else %}
                <div class="empty-state">
                    <div class="icon">🔍</div>
                    <h2>No Arbitrage Found</h2>
                    <p>No pre-match opportunities available right now.</p>
                    <p style="margin-top:8px;font-size:14px;color:#444;">Check back closer to match time.</p>
                </div>
            {% endif %}
        </div>
        
        <div class="refresh-note">
            🔄 Auto-refreshes every 60 seconds &bull; 
            Matches removed at kickoff &bull;
            <span class="auto-refresh">Last updated: {{ current_time }}</span>
        </div>
    </div>
    
    <script>
        // Auto-refresh every 60 seconds
        setTimeout(function() {
            location.reload();
        }, 60000);
    </script>
</body>
</html>
"""

# ============================================
# ROUTES
# ============================================
@app.route('/', methods=['GET'])
def index():
    """Display arbitrage opportunities."""
    opportunities = get_arbitrage_opportunities()
    current_time = datetime.now().strftime("%H:%M:%S")
    return render_template_string(HTML_TEMPLATE, 
                                   opportunities=opportunities,
                                   current_time=current_time)

@app.route('/api/opportunities', methods=['GET'])
def api_opportunities():
    """Return JSON data for API."""
    return jsonify(get_arbitrage_opportunities())

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"status": "ok", "message": "Bot is working!"})

# ============================================
# MAIN
# ============================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
