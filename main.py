import qrcode
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.types import FSInputFile
from aiogram.filters import Command

from config import TG_BOT_TOKEN, MAX_TEXT_LEN

bot = Bot(token=TG_BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command(commands=['start']))
async def command_start(message: Message):
    await message.answer('Привет. Пришли мне текст или ссылку и я сгенерирую тебе QR-Код')


@dp.message()
async def text_to_qr(message: Message):
    if len(message.text) > MAX_TEXT_LEN:
        await message.reply(f'Извините, такой большой текст я не смогу обработать (максимум {MAX_TEXT_LEN} символов)')
    else:
        qr = qrcode.QRCode(version=1,
                           error_correction=qrcode.constants.ERROR_CORRECT_L,
                           box_size=20,
                           border=1)
        qr.add_data(message.text)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color='black', back_color='white')
        time = message.date.strftime('%y%m%d_%H%M%S')
        chat_id = message.chat.id
        qr_img.save(f'qr-codes/{chat_id}_{time}.png')
        qr_img = FSInputFile(f'qr-codes/{chat_id}_{time}.png')
        await message.reply_photo(qr_img, caption='Ваш QR-Код готов!')


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
