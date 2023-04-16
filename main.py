from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN
import logging
from aiogram.dispatcher.filters import Text
from scrapper import *

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start( message: types.Message):
    await message.answer(f'Добрый день {message.from_user.first_name}. Я бот, который поможет вам сравнить цены на любую технику в магазинах города Баку. Просто пошлите мне кратко код модели техники, которой интересуетесь, и я помогу сам просмотреть цены в популярных магазинах.')

@dp.message_handler()
async def echo(message: types.Message):
    await message.reply('Минуту. Выполняется поиск')

    callback_irshad = await irshad(message.text)
    callback_kontakt = await kontakt(message.text)
    callback_b_e = await baku_electronics(message.text)
    callback_optimal = await optimal(message.text)


    irshad_message = '<b>Irshad Electronics</b>\n\n'
    kontakt_message = '<b>Kontakt Home</b>\n\n'
    baku_electronics_message = '<b>Baku Electronics</b>\n\n'
    optimal_message = '<b>Optimal Electronics</b>\n\n'


    if len(callback_irshad) > 0:
        for i in callback_irshad:
            irshad_message += f'{i[0]}\n{i[1]}\n{i[2]}\n\n'
    else:
        irshad_message += 'Результатов нет'

    if len(callback_kontakt) > 0:
        for i in callback_kontakt:
            kontakt_message += f'{i[0]}\n{i[1]}\n{i[2]}\n\n'
    else:
        kontakt_message += 'Результатов нет'

    if len(callback_b_e) > 0:
        for i in callback_b_e:
            baku_electronics_message += f'{i[0]}\n{i[1]}\n{i[2]}\n\n'
    else:
        baku_electronics_message += 'Результатов нет'

    if len(callback_optimal) > 0:
        for i in callback_optimal:
            optimal_message += f'{i[0]}\n{i[1]}\n{i[2]}\n\n'
    else:
        optimal_message += 'Результатов нет'

    try:
        await message.answer(irshad_message, parse_mode='html')
        await message.answer(kontakt_message, parse_mode='html')
        await message.answer(baku_electronics_message, parse_mode='html')
        await message.answer(optimal_message, parse_mode='html')
    except:
        await message.answer('Запрос возвращает слишком большое количество результатов. Пожалуйста сформулируйте запрос конкретнее.')


if __name__ == "__main__":
    executor.start_polling(dp)