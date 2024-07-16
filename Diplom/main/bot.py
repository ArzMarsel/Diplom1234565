import asyncio
from aiogram import Bot, Dispatcher, executor, types
import requests
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class UpdateStatus(StatesGroup):
    choosing = State()
    updating = State()


def get_main_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    button_cooking = types.InlineKeyboardButton(text="Получить готовящиеся Connect", callback_data="fetch_cooking")
    button_accepted = types.InlineKeyboardButton(text="Получить принятые Connect", callback_data="fetch_accepted")
    keyboard.add(button_cooking, button_accepted)
    return keyboard



TOKEN = '7443078722:AAGDjE1s6u7l3f4nt4V6TugeEW_n7cDGk0o'  # Токен, который вы получили от BotFather
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("Привет! Нажмите на кнопку ниже, чтобы получить список принятых Connect.",
                         reply_markup=get_main_keyboard())


@dp.callback_query_handler(lambda c: c.data.startswith('choose_'))
async def choose_connect(callback_query: types.CallbackQuery):
    parts = callback_query.data.split('_')
    connect_id = parts[1]
    next_status = parts[2]  # Извлекаем следующий статус из callback_data

    if next_status == 'delivering':
        status_text = 'Доставляется'
    elif next_status == 'cooking':
        status_text = 'Готовится'
    else:
        status_text = 'Неизвестный статус'

    keyboard = InlineKeyboardMarkup(row_width=1)
    button = InlineKeyboardButton(text=f"Подтвердить '{status_text}'",
                                  callback_data=f'update_{connect_id}_{next_status}')
    keyboard.add(button)

    await UpdateStatus.updating.set()
    await callback_query.message.answer(f'Выберите действие для заказа #{connect_id}:', reply_markup=keyboard)
    await callback_query.answer()



@dp.callback_query_handler(lambda c: c.data.startswith('update_'), state=UpdateStatus.updating)
async def update_status(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data.split('_')
    connect_id, new_status = data[1], data[2]
    # Передаем запрос в соответствующий API endpoint в зависимости от нового статуса
    endpoint = 'update-connect-status' if new_status == 'delivering' else 'unknown'
    response = requests.post(f'http://127.0.0.1:8000/api/update-connect-status/{connect_id}/',
                             json={'status': new_status})

    if response.status_code == 200:
        await callback_query.message.answer(f'Статус успешно обновлён на "{new_status}"!')
    else:
        await callback_query.message.answer('Ошибка при обновлении статуса.')
    await state.finish()
    await callback_query.answer()



@dp.callback_query_handler(lambda c: c.data == 'fetch_cooking')
async def fetch_cooking(callback_query: types.CallbackQuery):
    response = requests.get('http://127.0.0.1:8000/api/cooking-connects/')  # Меняем на новый endpoint
    if response.status_code == 200:
        connects = response.json()
        if connects:
            for connect in connects:
                text = f"Пользователь: {connect['user__username']}, Блюдо: {connect['dish__name']}, Количество: {connect['quantity']}"
                button_text = "Перевести в 'Доставляется'"
                keyboard = InlineKeyboardMarkup()
                button = InlineKeyboardButton(text=button_text, callback_data=f"choose_{connect['id']}_delivering")
                keyboard.add(button)
                await callback_query.message.answer(text, reply_markup=keyboard)
        else:
            await callback_query.message.answer('Заказы, готовящиеся к доставке, отсутствуют.')
    else:
        await callback_query.message.answer('Ошибка при получении данных.')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'fetch_accepted')
async def fetch_accepted(callback_query: types.CallbackQuery):
    response = requests.get('http://127.0.0.1:8000/api/accepted-connects/')
    if response.status_code == 200:
        connects = response.json()
        if connects:
            for connect in connects:
                text = f"Пользователь: {connect['user__username']}, Блюдо: {connect['dish__name']}, Количество: {connect['quantity']}"
                button_text = "Перевести в 'Готовится'"
                keyboard = InlineKeyboardMarkup()
                button = InlineKeyboardButton(text=button_text, callback_data=f"choose_{connect['id']}_cooking")
                keyboard.add(button)
                await callback_query.message.answer(text, reply_markup=keyboard)
        else:
            await callback_query.message.answer('Принятые заказы отсутствуют.')
    else:
        await callback_query.message.answer('Ошибка при получении данных.')
    await callback_query.answer()

async def send_telegram_message(chat_id, text):
    await bot.send_message(chat_id=chat_id, text=text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
