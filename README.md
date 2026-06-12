# SPX500 Telegram Trading Bot

## 📊 Strategy Overview

**Strategy:** Support/Resistance + 100 EMA
**Instrument:** SPX500
**Timeframe:** 1H (Hourly)
**Broker:** Compatible with TradingView

### Signal Types

| Signal | Emoji | Description | Action |
|--------|-------|-------------|--------|
| Bearish Reversal | 🔴 | Price near resistance + 100 EMA | PUT |
| Bullish Reversal | 🟢 | Price near support + 100 EMA | CALL |
| Bullish Breakout | ⬆️ | Close above resistance | CALL |
| Bearish Breakout | ⬇️ | Close below support | PUT |

---

## 🚀 Quick Setup Guide

### Step 1: Deploy the Bot (Choose One)

#### Option A: Render (Recommended - Free)

1. Go to [render.com](https://render.com) and sign up
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repo (or upload files manually)
4. Set the following:
   - **Name:** `spx500-telegram-bot`
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn bot:app`
5. Add Environment Variable:
   - **Key:** `WEBHOOK_URL`
   - **Value:** `https://spx500-telegram-bot.onrender.com` (your Render URL)
6. Click **"Create Web Service"**
7. Wait for deployment (2-3 minutes)

#### Option B: Railway (Free Tier)

1. Go to [railway.app](https://railway.app) and sign up
2. Click **"New Project"** → **"Deploy from GitHub"**
3. Upload the files to a GitHub repo
4. Add Environment Variable: `WEBHOOK_URL`
5. Deploy!

#### Option C: Your Own VPS

```bash
# SSH to your server
ssh user@your-vps-ip

# Clone or upload files
cd /opt
git clone <your-repo>
cd telegram-spx500-bot

# Install dependencies
pip install -r requirements.txt

# Run with screen or systemd
python bot.py
```

---

### Step 2: Configure TradingView

1. Open TradingView
2. Add SPX500 chart (e.g., US500, SPX)
3. Set timeframe to **1 Hour**
4. Open Pine Editor (bottom of screen)
5. Copy and paste content from `spx500_strategy.pine`
6. Click **"Add to Chart"**

---

### Step 3: Create Alerts

1. Click on chart → **"Alert"** (or press `Alt+A`)
2. Create alert for each condition:

#### Alert 1: Bearish Reversal
- **Condition:** (your strategy's) `nearResistanceAndEMA`
- **Options:** Check ✅ *"Alert will fire once per bar"*
- **Message:** (leave empty, we'll use webhook)

#### Alert 2: Bullish Reversal
- Same but for `nearSupportAndEMA`

#### Alert 3: Bullish Breakout
- Condition: `resistanceBreakout`

#### Alert 4: Bearish Breakout
- Condition: `supportBreakout`

---

### Step 4: Connect TradingView to Telegram Bot

1. After deploying, test your webhook URL:
   ```
   https://your-render-url.onrender.com/webhook
   ```

2. For each TradingView alert, go to **"Notifications"** tab:
   - Check ✅ **"Webhook URL"**
   - Enter your webhook URL

3. **Test first!** Use `/test` command in Telegram to verify connection

---

## 📱 Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Start the bot |
| `/status` | Check bot status |
| `/help` | Show help guide |
| `/test` | Send a test alert |

---

## 🔧 Configuration

Edit `bot.py` if needed:

```python
BOT_TOKEN = "YOUR_BOT_TOKEN"          # From BotFather
CHAT_ID = "YOUR_CHAT_ID"              # Your Telegram ID
ADMIN_USERNAME = "@your_username"     # Your Telegram username
```

---

## 📊 How It Works

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   TradingView   │───▶│  Python Bot     │───▶│   Telegram      │
│   (Chart)       │    │  (Webhook)      │    │   (You)         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
      Alerts               Process               Notifications
```

---

## ⚠️ Disclaimer

**Trading involves risk. This bot is for educational purposes only.**

- Signals are NOT financial advice
- Always verify signals manually
- Use proper risk management
- Check your local regulations

---

## 📞 Support

For issues or questions, check:
- TradingView Pine Script documentation
- Telegram Bot API documentation
- Render/Railway deployment guides

---

**Author:** MiniMax Agent
**Version:** 1.0.0