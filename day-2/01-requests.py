"""

Server examples

"""


import requests

response = requests.get('https://jsonplaceholder.typicode.com/users')
users = response.json()

email = users[0]['email']

print(email)

new_user = {
    'email': 'john@sobaka.com',
    'first_name': 'John'
}

response = requests.post('https://jsonplaceholder.typicode.com/users', new_user)
print(response.content)