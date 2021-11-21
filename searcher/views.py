from django.shortcuts import render, redirect
from .services import storage, auth, contacts
import requests

# Create your views here.
def index(request):
    return render(request, 'searcher/index.html')

def get_contact(request):
    """
    Ищет в AmoCRM контакт с указанным email и(или) телефоном. Если контакт не найден создает новый, заполнив имя, почту и телефон.
    Если контакт найден, обновляет его входящими данными.
    Затем создает сделку по указанному контакту в первом статусе воронки.
    """
    # Сохраняем данные полученные из запроса
    name = request.GET["name"]
    email = request.GET["email"]
    phone = request.GET["phone"]

    # Загружаем токены и другие данные из сервера
    tokens = storage.load_tokens("koloevvis")
    # Проверяем вернулись ли данные
    try:
        access_token = tokens['access_token']
        refresh_token = tokens['refresh_token']
        expires_in = tokens['expires_in']
        tokens_created_date = tokens['tokens_created_date']
    except KeyError as e:
        # Если токенов нет в базе, перенаправляем на страницу получения кода авторизации
        redirect('index')
    # Если токены получены, проверяем не истек ли срок действия access токена.
    if auth.is_access_token_expired(tokens_created_date, expires_in):
        # Если срок действия токена истек, обновляем access токен и refresh токен
        auth.refresh_tokens(refresh_token)

    link = f'https://koloevvis.amocrm.ru/api/v3/contacts'
    headers = {'Content-type': 'application/json', 'User-Agent': 'amoCRM-oAuth-client/1.0',
               "Authorization": f"Bearer {access_token}"}

    # Собираем данные для запроса на получение контактов
    payload = {"query": email}
    r = requests.get(link, params=payload, headers=headers)
    # Если не удалось найти по email, ищем по телефону
    if r.status_code == 204:
        payload = {"query": phone}
        r = requests.get(link, params=payload, headers=headers)

    # Проверяем результаты поиска по обоим параметрам
    if r.status_code == 401:  # Пользователь не авторизован
        redirect('index')
    elif r.status_code == 204:  # Контакт не найден
        # Создаем новый контакт с полученными данными
        contact_id = contacts.create_new_contact(name, phone, email, headers)
    else:
        # Если контакт существует, обновляем его полученными данными
        data = r.json()
        contact_id = data["_embedded"]["contacts"][0]["id"]
        contacts.edit_contact(contact_id, name, phone, email, headers)
    # Создаем новую сделку и привязываем к ней контакт
    contacts.create_lead(contact_id, headers)

    return redirect('index')


def integrate(request):
    """Redirect URI на который пользователь будет перенаправлен после получения кода авторизации.
    При получении кода авторизации, метод сохраняет его на сервере, а затем автоматически обменивает его
    на access token и refresh token.
    """
    client_data = storage.load_client_data()
    client_data["authorization_code"] = request.GET["code"]
    new_client_data = client_data
    storage.save_client_data(new_client_data)
    auth.create_initial_tokens(new_client_data)

    return redirect('index')
