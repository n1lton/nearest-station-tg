import os, geo
from dotenv import load_dotenv
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from art import tprint
import io
from networkx.exception import NetworkXNoPath



load_dotenv(".env")
bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher(bot)


def get_keyboard():
    keyboard = types.ReplyKeyboardMarkup()
    button = types.KeyboardButton("Найти ближайшую станцию", request_location=True)
    keyboard.add(button)
    return keyboard


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply(
        "Нажмите 'Найти ближайшую станцию' чтобы построить маршрут",
        reply_markup=get_keyboard()
    )


@dp.message_handler(content_types=['location'])
async def handle_location(message: types.Message):
    await message.answer("Секунду...")

    lat = message.location.latitude
    lon = message.location.longitude
    
    if not geo.check_city(lat, lon):
        await message.answer("Пока что поиск метро работает только в Москве.")
        return

    station = geo.find_nearest(lat, lon)

    try:
        map = geo.create_map(
            (lat, lon), (station["lat"], station["lng"])
        )
        img_data = map._to_png(1) # аргумент функции - кол-во сек на обработку

        await message.answer_photo(io.BytesIO(img_data), f"Ближайшая станция: {station['name']}")

    except NetworkXNoPath:
        await message.answer(f"Произошла ошибка при составлении маршрута. Местоположение станции {station['name']}:")
        await message.answer_location(station["lat"], station["lng"])

def main():
    tprint("NEAREST STATION")
    executor.start_polling(dp)


if __name__ == "__main__":
    main()