import os
import requests
from dotenv import load_dotenv

load_dotenv()

CHAT_ID = os.environ.get('CHAT_ID')
BOT_TOKEN = os.environ.get('BOT_TOKEN')

requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text=hey%20xinran!%20press%20/start%20to%20add%20your%20expenses%20for%20today:)&parse_mode=markdown")
