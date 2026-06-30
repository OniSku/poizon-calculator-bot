import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
DB_URL = os.getenv("DB_URL")

# Параметры расчета (загружаются из .env)
CNY_RATE = float(os.getenv("CNY_RATE", "0.0"))
COMMISSION = int(os.getenv("COMMISSION", "0"))
DELIVERY_SNEAKERS = int(os.getenv("DELIVERY_SNEAKERS", "0"))
DELIVERY_ACCESSORIES = int(os.getenv("DELIVERY_ACCESSORIES", "0"))