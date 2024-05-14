import requests
import json

def get_token():
    url = "https://app.bloomgrowth.com/Token"
    payload = 'grant_type=password&userName=jshallman%40srdent.com&password=password'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        token = json.loads(response.text).get('access_token')
        return token
    else:
        return "Token Error"

def create_user(name, due_date, notes, token):
    url = "https://app.bloomgrowth.com/api/v1/todo/create"
    headers = {'accept': 'application/json', 'Authorization': f'Bearer {token}'}
    payload = {
        "title": name,
        "notes": notes,
        "dueDate": due_date
    }
    response = requests.post(url, headers=headers, json=payload)
    print("Create New To Do")

def complete_status_to_do(Id):
    url = f"https://app.bloomgrowth.com/api/v1/todo/{Id}/complete?status=true"
    response = requests.request("POST", url)
    print("Complete Status True")

def get_to_do(name, due_date, notes, token):
    url = "https://app.bloomgrowth.com/api/v1/todo/users/mine"
    headers = {'accept': 'application/json', 'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        records = json.loads(response.text)
        check_records = [rec.get('Id') for rec in records if (rec.get('Name')).lower() == str(name).lower()]
        if check_records != []:
            output = {"Name": name, "Id": check_records[0]}
            print("user is already Exists")
        else:
            create_user(name, due_date, notes, token)


def main(input_data):
    asana_name = input_data.get('Name')
    due_date = input_data.get('dueDate')
    notes = input_data.get('notes')
    token = get_token()
    if token != "Token Error":
        get_to_do(asana_name, due_date, notes, token)
    else:
        print("Token retrieval failed")

# This is just for testing purpose, replace it with actual input_data when using in Zapier
input_data = {'Name': 'Sample Task1', 'dueDate': '2024-05-14', 'notes': 'Sample notes'}

main(input_data)
