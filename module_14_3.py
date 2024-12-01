from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = "_____________________________________________"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

start_kb = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text='Рассчитать'),
        KeyboardButton(text='Информация')
    ],
        [KeyboardButton(text='Купить')]
    ], resize_keyboard=True
)

second_kb = InlineKeyboardMarkup()
button1 = InlineKeyboardButton(
    text="Витамины", callback_data="product_buying")
button2 = InlineKeyboardButton(
    text="Таблетки", callback_data="product_buying")
button3 = InlineKeyboardButton(
    text="Антибиотики", callback_data="product_buying")
button4 = InlineKeyboardButton(
    text="Бады", callback_data="product_buying")
second_kb.add(button1)
second_kb.add(button2)
second_kb.add(button3)
second_kb.add(button4)


@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()


class UserState(StatesGroup):
    gender = State()
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text='Рассчитать')
async def set_gender(message):
    await message.answer("Введите свой пол [м/ж]:")
    await UserState.gender.set()


@dp.message_handler(state=UserState.gender, text=['М', 'м', 'Ж', 'ж'])
async def set_age(message, state):
    await state.update_data(gender=message.text.lower())
    await message.answer("Введите свой возраст (полных лет):")
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост (см.):")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес (кг.):")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    raw_calories = 10 * int(data['weight']) + 6.25 * \
        int(data['growth']) - 5 * int(data['age'])
    if data['gender'] == 'м':
        result = raw_calories + 5
        await message.answer(f"Оптимальное количество калорий: {result}")
    elif data['gender'] == 'ж':
        result = raw_calories - 161
        await message.answer(f"Оптимальное количество калорий: {result}")

    await state.finish()


@dp.message_handler(text=['Здравствуйте', 'Привет'])
async def hello_message(message):
    await message.answer("Здравствуйте! Введите команду /start, чтобы начать общение.")


@dp.message_handler(text=['Информация'])
async def info_message(message):
    await message.answer("Этот бот был создан Владимиром Кондратом")


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    await message.answer(f"Здравствуйте, {message.from_user.username}! Здесь Вы можете заказать из нашей аптеки лекарства или расчитать необходимое количество килокалорий (ккал) в сутки.", reply_markup=start_kb)


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    product_name = ["Витамины", "Таблетки", "Антибиотики", "Бады"]
    product_des = ["Различные витаминки",
                   "Таблетки, чтобы не болеть", "Мощные антибиотики", "Бады для красоты и здоровья"]
    for i in range(4):
        await message.answer_photo(open(f"{i +1}.jpg", "rb"),
                                   f"Название: {product_name[i]} | Описание: {product_des[i]} | Цена: {100 * (i + 1)}")
    await message.answer("Выберите продукт для покупки:", reply_markup=second_kb)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
