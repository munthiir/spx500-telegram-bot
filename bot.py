"""
SPX500 Trading Bot - Telegram Alerts
Strategy: Support/Resistance + 100 EMA
Author: MiniMax Agent
"""

import os
import logging
from flask import Flask, request, jsonify
import httpx

# ============== CONFIGURATION ==============
BOT_TOKEN = "8983707516:AAFKyeq4KLUikh2wI_J2H_yDWQvJqUoKLBY"
CHAT_ID = "1153872007"
ADMIN_USERNAME = "@munthiir"

# Flask app for webhook
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global bot instance
telegram_api = f"https://api.telegram.org/bot{BOT_TOKEN}"

# ============== MESSAGE FORMATTING ==============

def format_alert_message(signal_type, price, level, level_type, ema_distance, strength, timestamp):
    """Format the alert message with emojis and styling"""

    if signal_type == "REVERSAL_BEARISH":
        emoji = "🔴"
        title = "🔥 انعكاس هبوطي محتمل"
        action = "🟢 انتظر PUT"
    elif signal_type == "REVERSAL_BULLISH":
        emoji = "🟢"
        title = "🔥 انعكاس صعودي محتمل"
        action = "🔴 انتظر CALL"
    elif signal_type == "BREAKOUT_BULLISH":
        emoji = "⬆️"
        title = "🚀 اختراق صعودي!"
        action = "🟢 CALL"
    elif signal_type == "BREAKOUT_BEARISH":
        emoji = "⬇️"
        title = "📉 اختراق هبوطي!"
        action = "🔴 PUT"
    elif signal_type == "TEST":
        emoji = "🧪"
        title = "🧪 تنبيه تجريبي"
        action = "اضغط زر للتأكيد"
    else:
        emoji = "⚠️"
        title = "إشارة غير معروفة"
        action = "تحقق من الاستراتيجية"

    message = f"""{emoji} *{title}*

━━━━━━━━━━━━━━━━━━━━
📍 *SPX500 - فريم الساعة*
━━━━━━━━━━━━━━━━━━━━

💰 *السعر الحالي:* `{price}`
📊 *المستوى:* {level} ({level_type})
📏 *البعد عن 100 EMA:* {ema_distance} نقطة
⏱️ *الوقت:* {timestamp}

━━━━━━━━━━━━━━━━━━━━

🎯 *التوصية:* {action}
💪 *قوة الإشارة:* {strength}

━━━━━━━━━━━━━━━━━━━━
⏰ *تنبيه تلقائي من TradingView*
"""
    return message


# ============== TELEGRAM FUNCTIONS ==============

def send_telegram_message(text, chat_id=CHAT_ID):
    """Send message to Telegram"""
    url = f"{telegram_api}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        response = httpx.post(url, json=payload, timeout=10)
        return response.json()
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        return {"ok": False, "error": str(e)}


def send_telegram_with_buttons(text, chat_id=CHAT_ID):
    """Send message with inline buttons"""
    url = f"{telegram_api}/sendMessage"
    keyboard = {
        "inline_keyboard": [
            [{"text": "🟢 CALL", "callback_data": "action_CALL"},
             {"text": "🔴 PUT", "callback_data": "action_PUT"}]
        ]
    }
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
        "reply_markup": keyboard
    }
    try:
        response = httpx.post(url, json=payload, timeout=10)
        return response.json()
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        return {"ok": False, "error": str(e)}


# ============== WEBHOOK HANDLERS ==============

@app.route('/webhook', methods=['POST'])
def webhook():
    """Receive alerts from TradingView"""
    try:
        data = request.get_json()
        logger.info(f"Received webhook: {data}")

        if data:
            signal_type = data.get('signal_type', 'UNKNOWN')
            price = data.get('price', 0)
            level = data.get('level', 0)
            level_type = data.get('level_type', 'UNKNOWN')
            ema_distance = data.get('ema_distance', 0)
            strength = data.get('strength', 'MEDIUM')
            timestamp = data.get('time', 'Unknown')

            message = format_alert_message(
                signal_type=signal_type,
                price=price,
                level=level,
                level_type=level_type,
                ema_distance=ema_distance,
                strength=strength,
                timestamp=timestamp
            )

            result = send_telegram_with_buttons(message)
            logger.info(f"Telegram API response: {result}")

            return jsonify({"status": "success", "sent": True}), 200

    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

    return jsonify({"status": "no_data"}), 400


@app.route('/')
def index():
    """Health check endpoint"""
    return jsonify({
        "status": "Bot is running",
        "strategy": "SPX500 S/R + 100 EMA",
        "chat_id": CHAT_ID,
        "version": "1.0"
    })


@app.route('/test')
def test_endpoint():
    """Test endpoint - sends a test alert"""
    message = format_alert_message(
        signal_type="TEST",
        price=4500.50,
        level=4500,
        level_type="RESISTANCE",
        ema_distance=5.2,
        strength="اختبار",
        timestamp="2024-01-15 09:30:00"
    )

    result = send_telegram_with_buttons(message)
    return jsonify({
        "status": "test_sent",
        "telegram_response": result
    })


@app.route('/setwebhook', methods=['GET'])
def set_webhook():
    """Set webhook for Telegram bot"""
    webhook_url = os.environ.get('WEBHOOK_URL', '')
    if not webhook_url:
        return jsonify({"error": "WEBHOOK_URL not set"}), 400

    url = f"{telegram_api}/setWebhook"
    payload = {"url": webhook_url}

    try:
        response = httpx.post(url, json=payload, timeout=10)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/getwebhookinfo', methods=['GET'])
def get_webhook_info():
    """Get current webhook info"""
    url = f"{telegram_api}/getWebhookInfo"

    try:
        response = httpx.get(url, timeout=10)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============== MAIN ==============

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting bot on port {port}")
    app.run(host="0.0.0.0", port=port, debug=False)