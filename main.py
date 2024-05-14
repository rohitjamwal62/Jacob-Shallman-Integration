import requests,json
Asana_Name = input_data.get('Name')
url = "https://app.bloomgrowth.com/Token"
payload = 'grant_type=password&userName=jshallman%40srdent.com&password=password'
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
response = requests.request("POST", url, headers=headers, data=payload)
if response.status_code == 200:
    Token = json.loads(response.text).get('access_token')
    # Get All todo list here
    url = "https://app.bloomgrowth.com/api/v1/todo/users/mine"
    headers = {
    'accept': 'text/plain',
    'Authorization': f'Bearer {Token}',
    }
    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        Records = json.loads(response.text)
        for rec in Records:
            Name = rec.get('Name')
            Id = rec.get('Id')
            if str(Name).lower() == str(Asana_Name).lower():
                output = {"Name":Name,"Id":Id}
                print(output,">>>>>>>>>")
