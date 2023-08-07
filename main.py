from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

BOT_TOKEN: str = ''

# Чтение токена
file1 = open('Token.txt', 'r')
BOT_TOKEN = file1.readline().rstrip()
file1.close()

# создаем бота
bot: Bot = Bot(BOT_TOKEN)
dp: Dispatcher = Dispatcher()

# =====================================================
# обработка любого типа сообщения эхо ответом
# =====================================================


# обработка старт
@dp.message(Command(commands=['start']))
async def process_start_command(mess: Message):
    await mess.answer('Нажата кнопка Старт\n'
                      '--Тестовый бот--')
    # await mess.answer(mess.model_dump_json(indent=4))


# обработка help
@dp.message(Command(commands=['help']))
async def process_help_command(mess: Message):
    await mess.reply('Нажата кнопка помощь\n'
                     '--Тестовый бот--')


# dp.message.register(process_start_command, Command(commands=['start']))
# dp.message.register(process_help_command, Command(commands=['help']))

# обработка остальных сообщений


@dp.message()
async def any_mess(mess: Message):
    await mess.copy_to(chat_id=mess.chat.id)


dp.run_polling(bot)
exit()

# =====================================================
# Второй способ добавить хэндлеры - регистрация вручную
# =====================================================


# обработка старт
async def process_start_command(mess: Message):
    await mess.answer('Нажата кнопка Старт\n'
                      '--Тестовый бот--')
    # await mess.answer(mess.model_dump_json(indent=4))


# обработка help
async def process_help_command(mess: Message):
    await mess.reply('Нажата кнопка помощь\n'
                     '--Тестовый бот--')


# обработка фото
async def send_photo_echo(mess: Message):
    await mess.answer_photo(mess.photo[0].file_id)

# обработка эхо

# Регистрация обработчиков
dp.message.register(process_start_command, Command(commands=['start']))
dp.message.register(process_help_command, Command(commands=['help']))
dp.message.register(send_photo_echo, F.photo)

dp.run_polling(bot)
exit()


# ================================
# Первый способ добавить хэндлеры
# ================================

# Обработка команды старт
 

@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
    await message.answer('Это тестовый бот')


@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer('Выбрана опция Help')


@dp.message()
async def send_echo(message: Message):
    await message.reply(message.text)

if __name__ == '__main__':
    dp.run_polling(bot)
