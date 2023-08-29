import requests

url = "http://localhost:8000/tictactoe_game/check-auth/usuario_uno/"

payload = {}
headers = {
  'Authorization': 'Bearer 548d4c42965cb063c6f2f7b0abdff3f895f7d21b',
  'Cookie': 'csrftoken=LPCUtHTGBwSvwPQkDXB6uT1lIDW468y8; sessionid=i2x7y6l8obc4bgtifsw62v10jhkmthdw'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)