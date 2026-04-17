import os
import time
import pyotp
import requests
from datetime import datetime, timedelta
from SmartApi import SmartConnect
import telegram

# भारताची वेळ (IST) काढण्यासाठी फंक्शन
def get_indian_time():
    return datetime.now() + timedelta(hours=5, minutes=30)

# GitHub Secrets मधून डेटा मिळवणे
API_KEY = os.getenv('API_KEY')
CLIENT_ID = os.getenv('USER_ID')
PWD = os.getenv('PASSWORD')
TOTP_SECRET = os.getenv('TOTP_TOKEN')
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

# टेलिग्राम बॉट सेटअप
bot = telegram.Bot(token=BOT_TOKEN)

def login_to_angel():
    try:
        obj = SmartConnect(api_key=API_KEY)
        token = pyotp.TOTP(TOTP_SECRET).now()
        obj.generateSession(CLIENT_ID, PWD, token)
        return obj
    except Exception as e:
        print(f"Login Error: {e}")
        return None

def run_process():
    indian_time = get_indian_time()
    
    # १. सर्वात आधी कन्फर्मेशन मेसेज पाठवणे
    try:
        bot.send_message(
            chat_id=CHAT_ID, 
            text=f"📚 **Keep learning, keep earning!** 💰\n\n(बॉट यशस्वीरित्या सुरू झाला आहे | वेळ: {indian_time.strftime('%H:%M:%S')})",
            parse_mode='Markdown'
        )
    except Exception as e:
        print(f"Telegram Error: {e}")

    # २. मार्केट वेळेनुसार पुढचे काम
    hour = indian_time.hour
    minute = indian_time.minute

    if hour < 9 or (hour == 9 and minute < 15):
        # सकाळी ९:१५ च्या आधी
        msg = "☀️ **Morning Update:**\nग्लोबल मार्केटचे कल तपासले जात आहेत. ९:१५ नंतर हाय-विन सिग्नल्ससाठी तयार राहा! 🚀"
        bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode='Markdown')
    else:
        # मार्केट चालू असताना लॉगिन आणि स्कॅनिंग
        obj = login_to_angel()
        if obj:
            scan_msg = "🔍 **Live Market Scanning Active**\nमी सध्या ऑप्शन्स डेटा स्कॅन करत आहे. बेस्ट ट्रेड मिळताच तुम्हाला कळवले जाईल."
            bot.send_message(chat_id=CHAT_ID, text=scan_msg, parse_mode='Markdown')
        else:
            bot.send_message(chat_id=CHAT_ID, text="❌ Angel One लॉगिन अयशस्वी. कृपया API/TOTP चेक करा.")

if __name__ == "__main__":
    run_process()
