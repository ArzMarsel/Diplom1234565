import asyncio
from aiogram import Bot, Dispatcher, executor, types
import requests
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

class UpdateStatus(StatesGroup):
    choosing = State()
    updating = State()

def get_main_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    button = types.InlineKeyboardButton(text="Получить принятые Connect", callback_data="fetch_accepted")
    keyboard.add(button)
    return keyboard


TOKEN = '7443078722:AAGDjE1s6u7l3f4nt4V6TugeEW_n7cDGk0o'  # Токен, который вы получили от BotFather
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("Привет! Нажмите на кнопку ниже, чтобы получить список принятых Connect.", reply_markup=get_main_keyboard())


@dp.callback_query_handler(lambda c: c.data.startswith('choose_'))
async def choose_connect(callback_query: types.CallbackQuery):
    connect_id = callback_query.data.split('_')[1]
    status_keyboard = InlineKeyboardMarkup(row_width=1)
    statuses = [('delivering', 'Доставляется'), ('cooking', 'Готовится')]
    for status_code, status_text in statuses:
        button = InlineKeyboardButton(text=status_text, callback_data=f'update_{connect_id}_{status_code}')
        status_keyboard.add(button)
    await UpdateStatus.updating.set()
    await callback_query.message.answer('Выберите новый статус:', reply_markup=status_keyboard)
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data.startswith('update_'), state=UpdateStatus.updating)
async def update_status(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data.split('_')
    connect_id, new_status = data[1], data[2]
    response = requests.post(f'http://127.0.0.1:8000/api/update-connect-status/{connect_id}/', json={'status': new_status})
    if response.status_code == 200:
        await callback_query.message.answer('Статус успешно обновлён!')
    else:
        await callback_query.message.answer('Ошибка при обновлении статуса.')
    await state.finish()
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'fetch_accepted')
async def fetch_accepted(callback_query: types.CallbackQuery):
    response = requests.get('http://127.0.0.1:8000/api/accepted-connects/')
    if response.status_code == 200:
        connects = response.json()
        keyboard = InlineKeyboardMarkup()
        for connect in connects:
            text = f"Пользователь: {connect['user__username']}, Блюдо: {connect['dish__name']}, Количество: {connect['quantity']}"
            button_text = "Изменить статус"
            button = InlineKeyboardButton(text=button_text, callback_data=f"choose_{connect['id']}")
            keyboard.add(button)
        await callback_query.message.answer('Принятые заказы:', reply_markup=keyboard)
    else:
        await callback_query.message.answer('Ошибка при получении данных.')
    await callback_query.answer()
async def send_telegram_message(chat_id, text):
    await bot.send_message(chat_id=chat_id, text=text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)