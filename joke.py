import asyncio
import aiohttp
from gtts import gTTS
from aiogram.filters import Command
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import config  # ваш файл с токеном
from googletrans import Translator
import os
import tempfile
from aiogram.types import FSInputFile

translator = Translator()

# Создаем экземпляры бота и диспетчера
bot = Bot(token=config.TOKEN)
dp = Dispatcher()

# Приветствие /start
@dp.message(Command(commands=['start']))
async def start_handler(message: Message):
    await message.answer(
        "Привет! Я гиковский бот-шутка. Используйте /joke или нажмите кнопку ниже, чтобы получить шутку:",
        reply_markup=get_joke_button()
    )


# Ваша функция получения шутки
async def get_gamer_joke():
    url = 'https://geek-jokes.sameerkumar.website/api?format=json'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                joke_en = data['joke']
                # переводим
                joke_ru = translator.translate(joke_en, src='en', dest='ru').text
                return joke_ru
            else:
                return "Не удалось получить шутку :("



# Обработчик /joke
@dp.message(Command(commands=['joke']))
async def handle_joke(message: Message):
    joke = await get_gamer_joke()
    await message.answer(joke, reply_markup=get_joke_button())
    # Создаем голосовое
    await send_voice_from_text(bot, message,     # Создаем голосовое
    await send_voice_from_text(bot, message, joke))


# Создаем клавиатуру
def get_joke_button():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Раскачать шутку 🔄", callback_data='refresh_joke')]
    ])

# Обработка "Раскачать шутку" с голосовым
@dp.callback_query(F.data == 'refresh_joke')
async def refresh_joke_callback(callback: CallbackQuery):
    await callback.answer()
    joke = await get_gamer_joke()
    # Обновляем текст шутки
    await callback.message.edit_text(
        joke,
        reply_markup=get_joke_button()
    )
    translated_text = joke  # тут можно вставить перевод

    # Создаем голосовое сообщение из перевода
    await send_voice_from_text(bot, callback.message, translated_text)


async def send_voice_from_text(bot, message, text):
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as fp:
        filename = fp.name
        tts = gTTS(text=text, lang='ru')
        tts.save(filename)
    try:
        voice_file = FSInputFile(path=filename)
        await bot.send_voice(chat_id=message.chat.id, voice=voice_file)
    finally:
        os.remove(filename)



# Асинхронная точка входа
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())