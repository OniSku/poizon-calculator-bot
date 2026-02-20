import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
DB_URL = os.getenv("DB_URL")

# Параметры расчета
CNY_RATE = 12.7  # Курс юаня
COMMISSION = 1500  # Твоя комиссия
DELIVERY_SNEAKERS = 1350  # Доставка кроссовок
DELIVERY_ACCESSORIES = 850  # Доставка аксессуаров