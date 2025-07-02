import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery
from aiogram.types import Message, FSInputFile
from aiogram.types import BotCommand
from aiogram.utils.keyboard import InlineKeyboardBuilder
from googletrans import Translator
from gtts import gTTS
import aiohttp
import random
import config  # ваш файл с токеном
import logging
# Импортируем клавиатуру
from keyboards import inline_keyboards
import keyboards as kb



@dp.message(Command(commands=['translator']))
async def handle_translation(message):
    # Получаем текст после команды
    user_text = message.text.removeprefix('/translator').strip()

    if not user_text:
        await message.answer("Пожалуйста, отправьте текст для перевода.")
        return

    try:
        # Переводим на английский
        translation = translator.translate(user_text, dest='en')
        translated_text = translation.text

        # Создаем голосовое из переведенного текста
        tts = gTTS(text=translated_text, lang='en')
        filename = 'voice.ogg'
        tts.save(filename)

        # Отправляем переведенный текст
        await message.answer(f"Перевод: {translated_text}")

        # Отправляем голосовое сообщение
        voice_file = FSInputFile(path=filename)
        await bot.send_voice(chat_id=message.chat.id, voice=voice_file)

        # Удаляем временный файл
        os.remove(filename)

    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")


@dp.message(Command(commands=['translator_en']))
async def handle_translation(message):
    # Получаем текст после команды
    user_text = message.text.removeprefix('/translator_en').strip()

    if not user_text:
        await message.answer("Пожалуйста, отправьте текст для перевода.")
        return

    try:
        # Переводим на русский
        translation = translator.translate(user_text, dest='ru')
        translated_text = translation.text

        # Создаем голосовое из переведенного текста
        tts = gTTS(text=translated_text, lang='ru')
        filename = 'voice.ogg'
        tts.save(filename)

        # Отправляем переведенный текст
        await message.answer(f"Перевод: {translated_text}")

        # Отправляем голосовое сообщение
        voice_file = FSInputFile(path=filename)
        await bot.send_voice(chat_id=message.chat.id, voice=voice_file)

        # Удаляем временный файл
        os.remove(filename)

    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")



# Настраиваем логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=config.TOKEN)
dp = Dispatcher()  # Передача бота сюда
translator = Translator()

# Установка команд
async def set_commands():
    commands = [
        BotCommand(command='start', description='Запустить бота'),
        BotCommand(command='help', description='Помощь'),
        BotCommand(command='weather', description='Погода в Москве')
    ]
    await bot.set_my_commands(commands)

# Обработчики команд
# @dp.message(Command(commands=['start']))
# async def handle_start(message: Message):
#     await message.answer(
#         f"Привет, {message.from_user.first_name}! Я бот, готовый помочь тебе.\n"
#         "Введи /help, чтобы узнать команды.Выберите ссылку:",
#          reply_markup=inline_keyboards
#     )
#
# # Обработчик нажатий кнопок "Привет" и "Пока"
# @dp.message()
# async def handle_message(message: Message):
#     user_name = message.from_user.first_name
#
#     text = message.text
#     if text == "привет":
#         await message.answer(f"Привет, {user_name}!")
#     elif text == "пока":
#         await message.answer(f"До свидания, {user_name}!")
#
#
# @dp.message(CommandStart())
# async def start_handler(message: Message):
#     await message.answer(
#         f'Привет, {message.from_user.first_name}!',
#         reply_markup=await kb.get_initial_keyboard()
#     )

@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        f'Привет, {message.from_user.first_name}!',
        reply_markup=await kb.get_initial_keyboard()
    )

@dp.message(Command(commands=['dynamic']))
async def handle_dynamic(message: Message):
    await message.answer(
        "Нажми кнопку ниже:",
        reply_markup=await kb.get_initial_keyboard()
    )

@dp.callback_query(F.data == 'show_more')
async def show_more_callback(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=await kb.get_expanded_keyboard())

@dp.callback_query(F.data == 'option_1')
async def option_1_callback(callback: CallbackQuery):
    await callback.answer("Вы выбрали Опция 1")
    await callback.message.answer("Вы выбрали Опция 1!")

@dp.callback_query(F.data == 'option_2')
async def option_2_callback(callback: CallbackQuery):
    await callback.answer("Вы выбрали Опция 2")
    await callback.message.answer("Вы выбрали Опция 2!")





@dp.message(Command(commands=['help']))
async def handle_help(message):
    await message.answer("Доступные команды:\n/start - запуск\n/help - помощь\n/weather - погода в Москве\n/voice - голосовое сообщение\n/translator - перевод на английский\n/translator_en - перевод на русский")

@dp.message(Command(commands=['weather']))
async def handle_weather(message):
    city = 'Moscow'  # Можно расширить для получения названия города из сообщения
    weather_info = await get_weather(city)
    await message.answer(weather_info)


# Функция получения погоды
async def get_weather(city):
    api_key = 'a87950ff9d0c603a399e983698308834'  # вставьте свой API ключ сюда
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            if data.get('cod') != 200:
                return "Не удалось получить погоду"
            description = data['weather'][0]['description']
            temp = data['main']['temp']
            return f"Погода в {city}:\n{description}\nТемпература: {temp}°C"



# Обработка фото
@dp.message(F.photo)
async def handle_photo(message):
    responses = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
    await message.answer(random.choice(responses))
    # Создаём папку, если не существует
    folder_name = 'img'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    # Загружаем самое большое фото
    await bot.download(message.photo[-1], destination=f'img/{message.photo[-1].file_id}.jpg')
    await message.answer("Фото сохранено!")



@dp.message(Command(commands=['translator']))
async def handle_translation(message):
    # Получаем текст после команды
    user_text = message.text.removeprefix('/translator').strip()

    if not user_text:
        await message.answer("Пожалуйста, отправьте текст для перевода.")
        return

    try:
        # Переводим на английский
        translation = translator.translate(user_text, dest='en')
        translated_text = translation.text

        # Создаем голосовое из переведенного текста
        tts = gTTS(text=translated_text, lang='en')
        filename = 'voice.ogg'
        tts.save(filename)

        # Отправляем переведенный текст
        await message.answer(f"Перевод: {translated_text}")

        # Отправляем голосовое сообщение
        voice_file = FSInputFile(path=filename)
        await bot.send_voice(chat_id=message.chat.id, voice=voice_file)

        # Удаляем временный файл
        os.remove(filename)

    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")


@dp.message(Command(commands=['translator_en']))
async def handle_translation(message):
    # Получаем текст после команды
    user_text = message.text.removeprefix('/translator_en').strip()

    if not user_text:
        await message.answer("Пожалуйста, отправьте текст для перевода.")
        return

    try:
        # Переводим на английский
        translation = translator.translate(user_text, dest='ru')
        translated_text = translation.text

        # Создаем голосовое из переведенного текста
        tts = gTTS(text=translated_text, lang='ru')
        filename = 'voice.ogg'
        tts.save(filename)

        # Отправляем переведенный текст
        await message.answer(f"Перевод: {translated_text}")

        # Отправляем голосовое сообщение
        voice_file = FSInputFile(path=filename)
        await bot.send_voice(chat_id=message.chat.id, voice=voice_file)

        # Удаляем временный файл
        os.remove(filename)

    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")




@dp.message(Command('voice'))
async def voice(message):
    voice = FSInputFile("voice.ogg")
    await message.answer_voice(voice)



# Основная функция

async def main():
    await set_commands()
    # Запуск polling с правильным переданным ботом
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())


