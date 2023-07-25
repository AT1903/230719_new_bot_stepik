import requests
import time
# import pprint

API_URL: str = 'https://api.telegram.org/bot'
BOT_TOKEN: str = ''
TEXT: str = 'Апдейт на полученное сообщение - '
TEXT_RECV: str
MAX_COUNTER: int = 100

offset: int = -2
counter: int = 0
chat_id: int
timeout: int = 10
3
# Чтение токена
file1 = open('Token.txt', 'r')
BOT_TOKEN = file1.readline().rstrip()
file1.close()

# Проверка формируемой ссылки и печать итогового словаря
# print(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}')
# updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()
# pp = pprint.PrettyPrinter(depth=6)
# pp.pprint(updates)

while counter < MAX_COUNTER:
    print(f'Попытка - {counter}')
    start_time = time.time()
    updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}&timeout={timeout}').json()
    if updates['result']:
        for res in updates['result']:
            offset = res['update_id']
            chat_id = res['message']['from']['id']
            TEXT_RECV = res['message']['text']
            requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={TEXT}{TEXT_RECV}')            
            print((f'{TEXT}{TEXT_RECV}'))
    end_time = time.time()
    print((f'время на работу {start_time - end_time}'))

    counter += 1
    time.sleep(1)  # 1 second


# print('-----Requests lib-----')
# # файл заполнен в VScode перед отправкой в репозиторий GitHub

# api_url = 'http://api.open-notify.org/iss-now.json'
# # Отправляем GET-запрос и сохраняем ответ в переменной response
# response = requests.get(api_url)

# if response.status_code == 200:
#     print(response.text)
# else:
#     print(f'Код статуса - {response.status_code}')

# print('----API for numbers----')

# api_url = 'http://numbersapi.com/43'
# # Отправляем GET-запрос и сохраняем ответ в переменной response
# response = requests.get(api_url)

# if response.status_code == 200:
#     print(response.text)
# else:
#     print(f'Код статуса - {response.status_code}')
