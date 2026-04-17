import os
import time
import pyotp
import requests
from datetime import datetime, timedelta
from SmartApi import SmartConnect
import telegram

# वेळ भारताची सेट करणे
def get_indian_time():
    return datetime.now() + timedelta(hours=5, minutes=30)

API_KEY = os.getenv('API_KEY')
CLIENT_ID = os.getenv('USER_ID')
PWD = os.getenv('PASSWORD')
TOTP_SECRET = os.getenv('TOTP_TOKEN')
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

bot = telegram.Bot(token=BOT_TOKEN)

def login_to_angel():
    obj = SmartConnect(api_key=API_KEY)
    token = pyotp.TOTP(TOTP_SECRET).now()
    obj.generateSession(CLIENT_ID, PWD, token)
    return obj

def run_process():
    indian_time = get_indian_time()
    hour = indian_time.hour
    
    # टेलिग्रामला टेस्ट मेसेज पाठवून खात्री करणे
    bot.send_message(chat_id=CHAT_ID, text=f"🚀 बॉट सुरू झाला आहे! (IST: {indian_time.strftime('%H:%M:%S')})")

    if hour < 9:
        # सकाळी ८:३० ते ९:०० दरम्यान
        msg = "☀️ शुभ सकाळ भाऊ!\nग्लोबल मार्केट पॉझिटिव्ह दिसत आहे. आपण ९:१५ ला सिग्नल्स सुरू करू."
        bot.send_message(chat_id=CHAT_ID, text=msg)
    else:
        # मार्केट चालू असताना
        obj = login_to_angel()
        # येथे तुमचे स्कॅनिंग लॉजिक
        test_signal = "🎯 **LIVE SCANNING ACTIVE**\nमार्केट स्कॅन होत आहे. हाय-डेल्टा ट्रेड मिळताच मी येथे अपडेट देईन."
        bot.send_message(chat_id=CHAT_ID, text=test_signal, parse_mode='Markdown')

if __name__ == "__main__":
    run_process()
