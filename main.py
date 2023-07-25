import requests

print('-----Requests lib-----')
#файл заполнен в VScode перед отправкой в репозиторий GitHub

api_url = 'http://api.open-notify.org/iss-now.json'
response = requests.get(api_url)  # Отправляем GET-запрос и сохраняем ответ в переменной response

if response.status_code == 200:
    print(response.text)
else:
    print(f'Код статуса - {response.status_code}')


print ('----API for numbers----')

api_url = 'http://numbersapi.com/43'
response = requests.get(api_url)  # Отправляем GET-запрос и сохраняем ответ в переменной response

if response.status_code == 200:
    print(response.text)
else:
    print(f'Код статуса - {response.status_code}')