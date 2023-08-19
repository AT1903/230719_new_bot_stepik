from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
import random

user: dict = {'name': str,
              'id': int,
              'in_game': False,
              'attemps': 0,
              'number': int,
              'games': 0,
              'wins': 0}

BOT_TOKEN: str

# Чтение токена
file1 = open('Token.txt', 'r')
BOT_TOKEN = file1.readline().rstrip()
file1.close()


dp: Dispatcher = Dispatcher()
my_bot: Bot = Bot(BOT_TOKEN)


# Функция генератор случайных чисел
def get_random_num(max: int) -> int:
    return random.randrange(max)


# Обработка комманды Старт
@dp.message(Command(commands=['start']))
async def select_start(mess: Message):
    await mess.answer(f'========================\n'
                      f'=== Бот Угадай число ===\n'
                      f'========================\n'
                      f'\n'
                      f'Игрок - {mess.chat.last_name} {mess.chat.first_name}\n'
                      f'Чтобы начать игру отправьте "Да"')
    # 'Игрок - ', mess.chat['first_name'], mess.chat['last_name'])
    # print(mess.model_dump_json(indent=4, exclude_none=False))
    # print(type(mess))
    # print(dir(mess))
    # print(mess.chat.first_name)

    if user['in_game']:
        mess.answer('Вы уже находитесь в игре')
    else:
        mess.answer('Начать новую игру?')


# Обработка комманды Help
@dp.message(Command(commands=['help']))
async def select_help(mess: Message):
    await mess.answer('Чтобы начать игру отправьте "Да"\n'
                      'чтобы просмотреть статистику /stat\n'
                      'чтобы начать игру - /start')


# Обработка комманды Стат
@dp.message(Command(commands=['stat']))
async def select_stat(mess: Message):
    await mess.answer(f'Статистика игрока {mess.chat.last_name} {mess.chat.first_name}\n'
                      f'Количество игр - {user["games"]}\n'
                      f'Количество побед - {user["wins"]}\n'
                      f'чтобы просмотреть статистику /stat\n'
                      f'чтобы начать игру - /start')


# обработка сообщения Да
@dp.message(F.text.in_(['Да', 'да']))
async def start_game(mess: Message):
    print(user)
    if user['in_game']:
        await mess.answer(f'Вы уже находитесь в игре\n'
                          f'У вас осталось {user["attemps"]} попыток')
    else:
        user['in_game'] = True
        user['attemps'] = 5
        user['number'] = get_random_num(101)
        await mess.answer(f'Старт игры!\n'
                          f'Я загадал число от 0 до 99\n'
                          f'У вас осталось {user["attemps"]} попыток')


# Обработка числового значения
# @dp.message(F.text.isdigit())


@dp.message(lambda x: x.text and x.text.isdigit() and 0 < int(x.text) < 100)
async def num_process(mess: Message):
    if user['in_game']:
        # Уменьшаем количество попыток
        user['attemps'] = user['attemps'] - 1
        # проверяем на победу
        if int(mess.text) == user['number']:
            await mess.answer('Вы угадали!!!')
            user['in_game'] = False
            user['games'] = user['games'] + 1
            user['wins'] = user['wins'] + 1
        else:
            # Если не угадал то проверяем количество попыток (проверка на проигрыш)
            if user['attemps'] == 0:
                await mess.answer(f'Осталось {user["attemps"]} попыток. Вы проиграли!\n'
                                  f'Загаданное число - {user["number"]}\n'
                                  f'Чтобы начать игру отправьте "Да"\n'
                                  f'чтобы просмотреть статистику /stat\n')
                user['in_game'] = False
                user['games'] = user['games'] + 1
            else:
                # Если остались попытки то отправляем подсказку
                if int(mess.text) > user['number']:
                    await mess.answer(f'Меньше! Осталось {user["attemps"]} попыток')
                if int(mess.text) < user['number']:
                    await mess.answer(f'Больше! Осталось {user["attemps"]} попыток')
    else:
        await mess.answer('Вы еще не начали игру\n'
                          'Отправьте ''Да'' чтобы начать игру')


@dp.message(Command(commands=['cancel', 'exit']))
async def comm_cancel(mess: Message):
    user['in_game'] = False
    await mess.answer('Вы вышли из игры\n'
                      'чтобы просмотреть статистикку ''/stat''\n'
                      'чтобы начать игру - /start\n')


@dp.message()
async def any_mess(mess: Message):
    if user['in_game']:
        await mess.answer('Во время игры возможно отправлять только числа 0-99\n'
                          'для выхода из игры отправьте /cancel, /exit')
    else:
        await mess.answer('Чтобы начать игру отправьте ''Да''\n'
                          'чтобы просмотреть статистикку ''/stat''\n'
                          'чтобы начать игру - /start\n'
                          'для выхода отправьте /cancel, /exit')

print('====Start====')
dp.run_polling(my_bot)
