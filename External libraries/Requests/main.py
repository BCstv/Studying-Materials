import requests
r = requests.get('http://127.0.0.1:8000/items', {'item_id': 124114,
                                                           'q': 12})
print(r.json())