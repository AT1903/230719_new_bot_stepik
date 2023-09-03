from typing import Any
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, BaseFilter
from aiogram.types import Message

import random


Users = {}
BOT_TOKEN: str
admin_ids: list[int] = [1859997762, 178876776, 197177271]


# Фильтр на проверку админ. прав
class filter_admin(BaseFilter):
    def __init__(self, list_admins) -> None:
        self.list_admins = list_admins

    async def __call__(self, mess: Message):
        return mess.from_user.id in self.list_admins

    # async def __call__(self, *args: Any, **kwds: Any) -> Any:
    #     return super().__call__(*args, **kwds)

    # def __call__(self, mess: Message):
    #     return mess.from_user.id in self.list_admins


# Чтение токена
file1 = open('Token.txt', 'r')
BOT_TOKEN = file1.readline().rstrip()
file1.close()


# Мой фильтр для обработки сообщений "Да"
def my_filter(mess: Message) -> bool:
    return mess.text in ('Да', 'да')


# Функция генератор случайных чисел
def get_random_num(max: int) -> int:
    return random.randrange(max)


# Фильтрующая фукция (задача 1)
def custom_filter(list_in: list) -> bool:
    sum = 0
    for i in list_in:
        if str(i).isdigit() and int(i) == i and i % 7 == 0:
            sum = sum + i
    return (sum < 83)


some_list = [7, 14, 28, 32, 32, 56]
print('Результат 1')
print(custom_filter(some_list))

print('Результат 1')
some_list = [7, 14, 28, 32, 32, '56']
print(custom_filter(some_list))
print('_______')

# Анонимная функция (задача 2)
anonymous_filter = lambda x: len([s for s in x if s in ['я', 'Я']]) >= 23
print(anonymous_filter('Я - последняя буква в алфавите!'))
print(anonymous_filter('яяяяяяяяяяяяяяяяяяяяяяяя, яяяяяяяяяяяяяяяя и яяяяяяяя тоже!'))
print('_______')


dp: Dispatcher = Dispatcher()
my_bot: Bot = Bot(BOT_TOKEN)


# Проверка фильтра наследованного от BaseFilter
@dp.message(filter_admin(admin_ids))
async def is_admin(mess: Message):
    await mess.answer('Администратор')


# Обработка комманды Старт
@dp.message(Command(commands=['start']))
async def select_start(mess: Message):
    await mess.answer(f'========================\n'
                      f'=== Бот Угадай число ===\n'
                      f'========================\n'
                      f'\n'
                      f'Игрок - {mess.chat.last_name} {mess.chat.first_name}\n'
                      f'Чтобы начать игру отправьте "Да"')
    if mess.from_user.id not in Users:
        await mess.answer('Вы зарегистрированы в игре\n')
        Users[mess.from_user.id] = {'name': str,
                                    'id_user': int,
                                    'in_game': False,
                                    'attemps': 0,
                                    'number': int,
                                    'games': 0,
                                    'wins': 0}
    if Users[mess.from_user.id]['in_game']:
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
    if mess.from_user.id in Users:
        await mess.answer(f'Статистика игрока {mess.chat.last_name} {mess.chat.first_name}\n'
                          f'Количество игр - {Users[mess.from_user.id]["games"]}\n'
                          f'Количество побед - {Users[mess.from_user.id]["wins"]}\n'
                          f'чтобы просмотреть статистику /stat\n'
                          f'чтобы начать игру - /start')
    else:
        await mess.answer('Вы не зарегистрированы\n'
                          'чтобы начать игру - /start')


# обработка сообщения Да
# @dp.message(F.text.in_(['Да', 'да']))
@dp.message(my_filter)
async def start_game(mess: Message):
    print(Users)
    if Users[mess.from_user.id]['in_game']:
        await mess.answer(f'Вы уже находитесь в игре\n'
                          f'У вас осталось {Users[mess.from_user.id]["attemps"]} попыток')
    else:
        Users[mess.from_user.id]['in_game'] = True
        Users[mess.from_user.id]['attemps'] = 5
        Users[mess.from_user.id]['number'] = get_random_num(101)
        await mess.answer(f'Старт игры!\n'
                          f'Я загадал число от 0 до 99\n'
                          f'У вас осталось {Users[mess.from_user.id]["attemps"]} попыток')


# Обработка числового значения
@dp.message(lambda x: x.text and x.text.isdigit() and 0 < int(x.text) < 100)
async def num_process(mess: Message):
    if Users[mess.from_user.id]['in_game']:
        # Уменьшаем количество попыток
        Users[mess.from_user.id]['attemps'] = Users[mess.from_user.id]['attemps'] - 1
        # проверяем на победу
        if int(mess.text) == Users[mess.from_user.id]['number']:
            await mess.answer('Вы угадали!!!')
            Users[mess.from_user.id]['in_game'] = False
            Users[mess.from_user.id]['games'] = Users[mess.from_user.id]['games'] + 1
            Users[mess.from_user.id]['wins'] = Users[mess.from_user.id]['wins'] + 1
        else:
            # Если не угадал то проверяем количество попыток (проверка на проигрыш)
            if Users[mess.from_user.id]['attemps'] == 0:
                await mess.answer(f'Осталось {Users[mess.from_user.id]["attemps"]} попыток. Вы проиграли!\n'
                                  f'Загаданное число - {Users[mess.from_user.id]["number"]}\n'
                                  f'Чтобы начать игру отправьте "Да"\n'
                                  f'чтобы просмотреть статистику /stat\n')
                Users[mess.from_user.id]['in_game'] = False
                Users[mess.from_user.id]['games'] = Users[mess.from_user.id]['games'] + 1
            else:
                # Если остались попытки то отправляем подсказку
                if int(mess.text) > Users[mess.from_user.id]['number']:
                    await mess.answer(f'Меньше! Осталось {Users[mess.from_user.id]["attemps"]} попыток')
                if int(mess.text) < Users[mess.from_user.id]['number']:
                    await mess.answer(f'Больше! Осталось {Users[mess.from_user.id]["attemps"]} попыток')
    else:
        await mess.answer('Вы еще не начали игру\n'
                          'Отправьте ''Да'' чтобы начать игру')


# Обработка команды отмена / выход
@dp.message(Command(commands=['cancel', 'exit']))
async def comm_cancel(mess: Message):
    Users[mess.from_user.id]['in_game'] = False
    await mess.answer('Вы вышли из игры\n'
                      'чтобы просмотреть статистикку ''/stat''\n'
                      'чтобы начать игру - /start\n')


# Фильтр стикеров
@dp.message(F.content_type == 'sticker')
async def sticker_procc(mess: Message):
    await mess.answer('Стикер')
    mess.from_user.username


# Магический фильтр
@dp.message(F.from_user.first_name == 'Alexander')
async def proc_name(mess: Message):
    await mess.answer('Имя пользователя')



# Обработка всех других сообзений которые не попали в фильтры
@dp.message()
async def any_mess(mess: Message):
    if Users[mess.from_user.id]['in_game']:
        await mess.answer('Во время игры возможно отправлять только числа 0-99\n'
                          'для выхода из игры отправьте /cancel, /exit')
    else:
        await mess.answer('Чтобы начать игру отправьте ''Да''\n'
                          'чтобы просмотреть статистикку ''/stat''\n'
                          'чтобы начать игру - /start\n'
                          'для выхода отправьте /cancel, /exit')
        print(mess.model_dump_json(indent=4, exclude_none=True))

print('====Start====')
dp.run_polling(my_bot)
