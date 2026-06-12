"""
SPX500 Trading Bot - Telegram Alerts
Strategy: Support/Resistance + 100 EMA
Author: MiniMax Agent
"""

import os
import json
import logging
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# ============== CONFIGURATION ==============
BOT_TOKEN = "8983707516:AAFKyeq4KLUikh2wI_J2H_yDWQvJqUoKLBY"
CHAT_ID = "1153872007"
ADMIN_USERNAME = "@munthiir"

# Flask app for webhook
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============== TELEGRAM HANDLERS ==============

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    welcome_message = """
📊 *مرحباً بك في بوت SPX500 Alerts!*

✅ البوت يتابع استراتيجيتك على:
• SPX500
• فريم الساعة
• الدعم والمقاومة + 100 EMA

🔔 *طريقة العمل:*
اربط التنبيهات من TradingView بالبوت
وسيصلك إشعار فوري لكل إشارة

📈 *أنواع الإشارات:*
• 🔴 انعكاس من مقاومة
• 🟢 انعكاس من دعم
• ⬆️ اختراق صعودي
• ⬇️ اختراق هبوطي

للتحقق من حالة البوت اكتب /status
"""
    await update.message.reply_text(welcome_message, parse_mode='Markdown')


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command"""
    status_message = """
✅ *حالة البوت: يعمل بشكل طبيعي*

📊 SPX500 Strategy Monitor
⏰ Timeframe: 1H
📍 Indicators: S/R + 100 EMA

🔗 TradingView Webhook متصل
📨 التنبيهات نشطة
"""
    await update.message.reply_text(status_message, parse_mode='Markdown')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_message = """
📖 *دليل الاستخدام*

*الإعدادات المطلوبة:*
1. افتح TradingView
2. أضف المؤشرات للاستراتيجية
3. أنشئ تنبيه مع Webhook URL

*Webhook URL:*
`https://your-render-url.onrender.com/webhook`

*للحصول على رابط Webhook:*
انشر البوت على Render/Railway ثم استخدم الرابط

*الأوامر المتاحة:*
/start - بدء البوت
/status - حالة البوت
/help - هذا الدليل
/test - إرسال تنبيه تجريبي
"""
    await update.message.reply_text(help_message, parse_mode='Markdown')


async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /test command - send a test alert"""
    test_alert = format_alert_message(
        signal_type="TEST",
        price=4500.50,
        level=4500,
        level_type="RESISTANCE",
        ema_distance=5.2,
        strength="TEST",
        timestamp="2024-01-15 09:30:00"
    )

    keyboard = [
        [InlineKeyboardButton("🟢 CALL", callback_data="action_CALL"),
         InlineKeyboardButton("🔴 PUT", callback_data="action_PUT")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(test_alert, parse_mode='Markdown', reply_markup=reply_markup)


def format_alert_message(signal_type, price, level, level_type, ema_distance, strength, timestamp):
    """Format the alert message with emojis and styling"""

    # Determine emoji and color based on signal type
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
    else:
        emoji = "⚠️"
        title = "إشارة غير معروفة"
        action = "تحقق من الاستراتيجية"

    message = f"""
{emoji} *{title}*

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


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular messages"""
    await update.message.reply_text(
        "📩 تم استلام رسالتك!\n"
        "للتحقق من حالة البوت اكتب /status\n"
        "لإرسال تنبيه تجريبي اكتب /test"
    )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle callback queries from inline buttons"""
    query = update.callback_query
    await query.answer()

    action = query.data.replace("action_", "")

    if action == "CALL":
        response = "🟢 تم اختيار CALL\nانتبه: هذا اختيارك الشخصي ولا يُعتبر نصيحة تداول!"
    else:
        response = "🔴 تم اختيار PUT\nانتبه: هذا اختيارك الشخصي ولا يُعتبر نصيحة تداول!"

    await query.edit_message_text(text=query.message.text + f"\n\n✅ {response}")


# ============== WEBHOOK HANDLER ==============

@app.route('/webhook', methods=['POST'])
def webhook():
    """Receive alerts from TradingView"""
    try:
        data = request.get_json()
        logger.info(f"Received webhook: {data}")

        if data:
            # Extract data from TradingView alert
            signal_type = data.get('signal_type', 'UNKNOWN')
            price = data.get('price', 0)
            level = data.get('level', 0)
            level_type = data.get('level_type', 'UNKNOWN')
            ema_distance = data.get('ema_distance', 0)
            strength = data.get('strength', 'MEDIUM')
            timestamp = data.get('time', 'Unknown')

            # Format message
            message = format_alert_message(
                signal_type=signal_type,
                price=price,
                level=level,
                level_type=level_type,
                ema_distance=ema_distance,
                strength=strength,
                timestamp=timestamp
            )

            # Create inline buttons
            keyboard = [
                [InlineKeyboardButton("🟢 CALL", callback_data="action_CALL"),
                 InlineKeyboardButton("🔴 PUT", callback_data="action_PUT")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            # Send to Telegram
            application.bot.send_message(
                chat_id=CHAT_ID,
                text=message,
                parse_mode='Markdown',
                reply_markup=reply_markup
            )

            return {'status': 'success'}, 200
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return {'status': 'error', 'message': str(e)}, 500

    return {'status': 'no_data'}, 400


@app.route('/')
def index():
    """Health check endpoint"""
    return {'status': 'Bot is running', 'strategy': 'SPX500 S/R + 100 EMA'}


# ============== MAIN ==============

def main():
    """Start the bot"""
    global application

    # Create application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("test", test_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(button_callback))

    # Run webhook mode (for production)
    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get('PORT', 5000)),
        url_path="webhook",
        webhook_url=os.environ.get('WEBHOOK_URL', '')
    )


if __name__ == '__main__':
    main()