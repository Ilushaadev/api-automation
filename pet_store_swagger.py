import requests


url = f"https://petstore.swagger.io/v2/pet/12"
resp = requests.get(url)
print(resp.json())