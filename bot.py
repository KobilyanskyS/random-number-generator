import random

# importing Aiogram
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# importing the database management file
import database as db

# bot token
API_TOKEN = 'YOUR_TOKEN'

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Keyboard for language selection
button_ru = KeyboardButton('🇷🇺 Русский')
button_en = KeyboardButton('🇬🇧 English')
language_kb = ReplyKeyboardMarkup(resize_keyboard=True)
language_kb.add(button_ru,button_en)

# Set range of numbers from user in states
class numbersForm(StatesGroup):
    number_from = State()
    number_to = State()

# /start command
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    db.set_user(message.from_user.id)
    await message.answer("Hi!\nI am a random number generator bot\nDefault number range: from 1 to 100\nMy commands:\n/language - Select a language.\n/range - Set your own range of numbers.\n/generate - Generate a number\n/reset - Sets the default range of numbers (from 1 to 100)\n\nПривет!\nЯ бот-генератор случайных чисел\nДиапазон чисел по умолчанию: от 1 до 100\nМои команды:\n/language - Выбрать язык.\n/range - Задать свой диапазон чисел.\n/generate - Сгенерировать число\n/reset - Устанавливает диапазон чисел по умолчанию (от 1 до 100)")

# /language command
@dp.message_handler(commands=['language'])
async def choose_language(message: types.Message):
    await message.answer("Выберите язык:\nChoose the language:", reply_markup=language_kb)

# /range command
@dp.message_handler(commands=['range'])
async def choose_range(message: types.Message):
    await numbersForm.number_from.set()
    if db.get_language(message.from_user.id) == 1:
        await message.answer("Введите начальное число: ", reply_markup=types.ReplyKeyboardRemove())
    elif db.get_language(message.from_user.id) == 0:
        await message.answer("Set an initial number: ", reply_markup=types.ReplyKeyboardRemove())

# hadler for number_from
@dp.message_handler(lambda message: message.text.isdigit(), state=numbersForm.number_from)
async def process_number_from(message: types.Message, state: FSMContext):
    await numbersForm.next()
    await state.update_data(number_from=int(message.text))
    if db.get_language(message.from_user.id) == 1:
        await message.answer("Введите конечное число: ")
    elif db.get_language(message.from_user.id) == 0:
        await message.answer("Set a finite number: ")

# hadler for number_to
@dp.message_handler(lambda message: message.text.isdigit(), state=numbersForm.number_to)
async def process_number_to(message: types.Message, state: FSMContext):
    await numbersForm.next()
    await state.update_data(number_to=int(message.text))
    async with state.proxy() as data:
        db.set_range(int(md.text(data['number_from'])), int(md.text(data['number_to'])), message.from_user.id)
        if db.get_language(message.from_user.id) == 1:
            await message.answer(md.text('Ваш диапазон чисел установлен: ', 'от ', data['number_from'], ' до ', data['number_to']))
            await message.answer("Введите команду /generate, чтобы сгененрировать число")
        elif db.get_language(message.from_user.id) == 0:
            await message.answer(md.text('Your range of numbers is set: ', 'from ', data['number_from'], ' to ', data['number_to']))
            await message.answer("Enter the /generate command to generate a number")
        await state.finish()

# handler for Russian language
@dp.message_handler(Text(equals="🇷🇺 Русский"))
async def russian_lg(message: types.Message):
    db.choose_language(1, message.from_user.id)
    await message.reply("Язык изменён на русский", reply_markup=types.ReplyKeyboardRemove())

# handler for English language
@dp.message_handler(Text(equals="🇬🇧 English"))
async def english_lg(message: types.Message):
    db.choose_language(0, message.from_user.id)
    await message.reply("Language switched to English", reply_markup=types.ReplyKeyboardRemove())

# /generate command
@dp.message_handler(commands=['generate'])
async def generate(message: types.Message):
    # get the initial and final numbers from the database.
    num_from = db.get_range(message.from_user.id)[0][0]
    num_to = db.get_range(message.from_user.id)[0][1] + 1
    # generate a number
    try:
        generated_number = random.randrange(num_from, num_to)
        if db.get_language(message.from_user.id) == 1:
            await message.answer("Ваше число: " + str(generated_number))
        elif db.get_language(message.from_user.id) == 0:
            await message.answer("Your number: " + str(generated_number))
    except ValueError:
        if db.get_language(message.from_user.id) == 1:
            await message.answer("Вы ввели неправильный диапазон чисел\nВозможно начальное число больше конечного\nИспользуйте команду /range, чтобы задать числовой диапазон")
        elif db.get_language(message.from_user.id) == 0:
            await message.answer("You entered the wrong range of numbers\nPerhaps the initial number is greater than the final\nUse the /range command to set the numeric range")

# /reset command
@dp.message_handler(commands=['reset'])
async def reset_range(message: types.Message):
    db.set_user(message.from_user.id)
    db.reset(message.from_user.id)
    if db.get_language(message.from_user.id) == 1:
        await message.answer("Ваш диапазон сброшен.\nТекущий диапазон: от 1 до 100")
    elif db.get_language(message.from_user.id) == 0:
        await message.answer("Your range is reset.\nCurrent range: from 1 to 100")

# handler for other messages (not necessary)
@dp.message_handler()
async def echo(message: types.Message):
    if db.get_language(message.from_user.id) == 1:
        await message.reply("Я не знаю, как вам ответить 🥺\nЧтобы узнать больше информации, введите команду /start")
    elif db.get_language(message.from_user.id) == 0:
        await message.reply("I do not know how to answer you 🥺\nTo find out more information, enter the /start command")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)