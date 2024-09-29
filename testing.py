import requests



response = requests.get("http://localhost:5000/nextmed").json()


print(response)

