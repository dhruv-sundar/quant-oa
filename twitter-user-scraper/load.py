import json
from user import User

with open('output.json') as json_file:
    data = json.load(json_file)

user = User(data, load=True)
print("Loaded " + user.user + " in")