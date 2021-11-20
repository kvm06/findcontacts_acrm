import json


def save_tokens(tokens, subdomain):
    with open(f'searcher/services/tokens/{subdomain}.tokens.json', 'w', encoding='utf-8') as f:
        json.dump(tokens, f, ensure_ascii=False, indent=4, default=True)
    print("Данные токенов обновлены")


def load_tokens(subdomain):
    with open(f'searcher/services/tokens/{subdomain}.tokens.json', 'r') as f:
        data = json.load(f)
    return data


def save_client_data(client_data):
    with open(f'searcher/services/tokens/integration.json', 'w', encoding='utf-8') as f:
        json.dump(client_data, f, ensure_ascii=False, indent=4, default=True)
    print("Данные клиента обновлены")


def load_client_data():
    with open(f'searcher/services/tokens/integration.json') as f:
        data = json.load(f)
    return data

