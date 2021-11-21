from django.shortcuts import render, redirect
from .services import storage, auth, contacts
import requests


# Create your views here.
def index(request):
    return render(request, 'searcher/index.html')


def get_contact(request):
    name = request.GET["name"]
    email = request.GET["email"]
    phone = request.GET["phone"]

    tokens = storage.load_tokens("koloevvis")
    # Проверить есть ли токен в базе
    try:
        access_token = tokens['access_token']
        refresh_token = tokens['refresh_token']
        expires_in = tokens['expires_in']
        tokens_created_date = tokens['tokens_created_date']
    except KeyError as e:
        # Если токенов нет в базе, перенаправляем на страницу получения кода авторизации
        redirect('index')
    # Проверяем не истек ли срок действия access токена.
    if auth.is_access_token_expired(tokens_created_date, expires_in):
        # Если срок действия токена истек, обновляем access токен и refresh токен
        auth.refresh_tokens(refresh_token)

    subdomain = 'koloevvis'
    link = f'https://{subdomain}.amocrm.ru/api/v4/contacts'
    headers = {'Content-type': 'application/json', 'User-Agent': 'amoCRM-oAuth-client/1.0',
               "Authorization": f"Bearer {access_token}"}

    payload = {"query": f"{email}"}
    r = requests.get(link, params=payload, headers=headers)

    if r.status_code != 204:
        # Если контакт существует, обновляем его
        data = r.json()
        contact_id = data["_embedded"]["contacts"][0]["id"]
        contacts.edit_contact(contact_id, name, phone, email, headers)
    else:
        # Если контакт с таким номером и/или почтой не существует, создаем его
        contact_id = contacts.create_new_contact(name, phone, email, headers)

    contacts.create_lead(contact_id, headers)
    return redirect('index')


def integrate(request):
    client_data = storage.load_client_data()
    client_data["authorization_code"] = request.GET["code"]
    new_client_data = client_data
    storage.save_client_data(new_client_data)
    auth.create_initial_tokens(new_client_data)

    return redirect('index')
