import requests
import json


def create_new_contact(name, phone, email, headers):
    URL = "https://koloevvis.amocrm.ru/api/v4/contacts"
    sent_data = [
        {
            "name": name,
            "custom_fields_values": [
                {
                    "field_id": 685191,
                    "values": [
                        {
                            "value": email
                        }
                    ]
                },
                {
                    "field_id": 685189,
                    "values": [
                        {
                            "value": phone
                        }
                    ]
                }
            ]
        },
    ]
    r = requests.post(URL, data=json.dumps(sent_data), headers=headers)
    data = r.json()
    contact_id = data["_embedded"]["contacts"][0]["id"]
    return contact_id


def edit_contact(contact_id, name, phone, email, headers):
    URL = f"https://koloevvis.amocrm.ru/api/v4/contacts/{contact_id}"
    sent_data = {
        "name": name,
        "custom_fields_values": [
            {
                "field_id": 685191,
                "values": [
                    {
                        "value": email
                    }
                ]
            },
            {
                "field_id": 685189,
                "values": [
                    {
                        "value": phone
                    }
                ]
            }
        ]
    }
    r = requests.patch(URL, data=json.dumps(sent_data), headers=headers)


def create_lead(contact_id, headers):
    URL = "https://koloevvis.amocrm.ru/api/v4/leads"
    print("I am here")
    sent_data = [
        {
            "_embedded": {
                "contacts": [
                    {
                        "id": contact_id
                    }
                ]
            }
        }
    ]
    requests.post(URL, data=json.dumps(sent_data), headers=headers)
