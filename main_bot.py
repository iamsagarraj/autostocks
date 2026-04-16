import os
import time
import pyotp
import requests
from datetime import datetime
from SmartApi import SmartConnect
import telegram

# GitHub Secrets मधून माहिती घेणे (Security साठी)
API_KEY = os.getenv('API_KEY')
CLIENT_ID = os.getenv('USER_ID')
PWD = os.getenv('PASSWORD')
TOTP_SECRET = os.getenv('TOTP_TOKEN')
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

bot = telegram.Bot(token=BOT_TOKEN)

# १. सकाळी ८:३० चा ग्लोबल सेंटिमेंट मेसेज
def send_morning_sentiment():
    try:
        # येथे आपण Gift Nifty चा डेटा API मधून घेऊ शकतो, सध्या एक जनरल लॉजिक
        message = f"☀️ शुभ सकाळ भाऊ! (Date: {datetime.now().date()})\n\n📊 आजचे मार्केट सेंटिमेंट:\n- Global Markets: Positive 🚀\n- Gift Nifty: Flat to Positive\n\nआज आपण High Delta (0.55-0.60) ट्रेड्सवर लक्ष ठेवू. तयार राहा! 🔥"
        bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        print(f"Error in morning update: {e}")

# २. अँजल वन लॉगिन
def login_to_angel():
    obj = SmartConnect(api_key=API_KEY)
    token = pyotp.TOTP(TOTP_SECRET).now()
    data = obj.generateSession(CLIENT_ID, PWD, token)
    return obj

# ३. मुख्य स्कॅनिंग लॉजिक (Simplified for automation)
def start_scanning():
    obj = login_to_angel()
    # समजा आपण १० ते ३:१५ पर्यंत स्कॅन करतोय
    print("Market Scanning Started...")
    
    # येथे तुमचे RSI/VWAP/Greeks लॉजिक चालेल
    # उदाहरण सिग्नल:
    signal_msg = "🎯 **NEW SIGNAL** 🎯\n\n🚀 NIFTY 24500 CE\n💰 Entry: Above 150\n📉 SL: 130\n🎯 Target: 190\n\nDelta: 0.58 | OI: Long Buildup ✅"
    bot.send_message(chat_id=CHAT_ID, text=signal_msg, parse_mode='Markdown')

if __name__ == "__main__":
    # वेळ तपासून फंक्शन कॉल करा
    now = datetime.now().hour
    if now < 9:
        send_morning_sentiment()
    else:
        start_scanning()
