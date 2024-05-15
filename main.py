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
    if response.status_code == 200:
        User_Id = json.loads(response.text).get('Id')
        print("Create New To Do")
        return User_Id
        

def complete_status_to_do(Id,token):
    url = f"https://app.bloomgrowth.com/api/v1/todo/{Id}/complete?status=true"
    headers = {'accept': 'application/json', 'Authorization': f'Bearer {token}'}
    response = requests.request("POST", url,headers=headers)
    if response.status_code == 200:  
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
            complete_status_to_do(check_records[0],token)
            return output
        else:
            User_Id = create_user(name, due_date, notes, token)
            complete_status_to_do(User_Id,token)
            output = {"User_Id":User_Id}


def main(input_data):
    asana_name = input_data.get('Name')
    due_date = input_data.get('dueDate')
    notes = input_data.get('notes')
    token = get_token()
    if token != "Token Error":
        get_to_do(asana_name, due_date, notes, token)
    else:
        print("Token retrieval failed")
input_data = {"Name":"jack test new 15 mays","due_date":"2024-05-16","notes":""}
output = main(input_data)
