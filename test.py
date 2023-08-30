import requests

url = "http://localhost:8000/tictactoe_game/api/user_details/"
headers = {
    "Authorization": "Token 06f30aa82755cec7b35014de5e145f24fb91d792"
}

response = requests.get(url, headers=headers)
data = response.json()
print(data)