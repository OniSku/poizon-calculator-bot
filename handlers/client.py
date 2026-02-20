from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select

from core.config import (
    CNY_RATE, COMMISSION, DELIVERY_SNEAKERS,
    DELIVERY_ACCESSORIES, ADMIN_ID, ADMIN_USERNAME
)
from database.models import Order, User  # Добавь User
from database.db import async_session

client_router = Router()


class CalcStates(StatesGroup):
    choosing_category = State()
    entering_price = State()


def get_categories_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="Кроссовки", callback_data="cat_sneakers")
    builder.button(text="Сумки/Аксессуары", callback_data="cat_accs")
    builder.adjust(1)
    return builder.as_markup()


def get_order_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="🛍 Оформить заказ", url=f"https://t.me/{ADMIN_USERNAME}")
    builder.button(text="🔄 Новый расчет", callback_data="start_over")
    builder.adjust(1)
    return builder.as_markup()


@client_router.message(CommandStart())
@client_router.callback_query(F.data == "start_over")
async def cmd_start(event: types.Message | types.CallbackQuery, state: FSMContext):
    await state.clear()

    # РЕГИСТРАЦИЯ/ПРОВЕРКА ПОЛЬЗОВАТЕЛЯ
    user_id = event.from_user.id
    username = event.from_user.username

    async with async_session() as session:
        result = await session.execute(select(User).where(User.tg_id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            new_user = User(tg_id=user_id, username=username)
            session.add(new_user)
            await session.commit()

    text = "Привет! Я помогу рассчитать стоимость товара с Poizon.\nВыбери категорию:"

    if isinstance(event, types.Message):
        await event.answer(text, reply_markup=get_categories_kb())
    else:
        await event.message.edit_text(text, reply_markup=get_categories_kb())
        await event.answer()

    await state.set_state(CalcStates.choosing_category)


@client_router.callback_query(F.data.startswith("cat_"))
async def callbacks_category(callback: types.CallbackQuery, state: FSMContext):
    category = callback.data.split("_")[1]
    await state.update_data(category=category)
    await callback.message.edit_text("Введите стоимость товара в юанях (¥):")
    await state.set_state(CalcStates.entering_price)
    await callback.answer()


@client_router.message(CalcStates.entering_price)
async def process_price(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("Пожалуйста, введите только цифры.")

    price_cny = int(message.text)
    user_data = await state.get_data()
    category = user_data.get("category")

    delivery = DELIVERY_SNEAKERS if category == "sneakers" else DELIVERY_ACCESSORIES
    total_rub = round(price_cny * CNY_RATE + delivery + COMMISSION)

    result_text = (
        f"📊 Результат расчета:\n\n"
        f"Цена: {price_cny} ¥\n"
        f"Курс: {CNY_RATE} руб.\n"
        f"Доставка: {delivery} руб.\n"
        f"Комиссия: {COMMISSION} руб.\n\n"
        f"💰 Итого к оплате: {total_rub} руб."
    )

    async with async_session() as session:
        new_order = Order(
            user_tg_id=message.from_user.id,
            description=f"Категория: {category}, Цена: {price_cny}Y, Итого: {total_rub}р",
            status="calculated"
        )
        session.add(new_order)
        await session.commit()

    try:
        await message.bot.send_message(
            ADMIN_ID,
            f"🔔 Новый расчет!\nПользователь: @{message.from_user.username or 'скрыт'}\nСумма: {total_rub} руб."
        )
    except Exception as e:
        print(f"Ошибка уведомления админа: {e}")

    await message.answer(result_text, reply_markup=get_order_kb())
    await state.set_state(CalcStates.choosing_category)