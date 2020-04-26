#! /usr/bin/python3.7
import requests
import json


response = requests.get(
    'https://api.github.com/search/repositories',
    params={'q': 'become_qa_auto'}
)

json_response = response.json()
# with open('json_response.json', 'w') as file:
#     json.dump(json_response, file, indent=3)

# eliminating the chunk that contains all info of the repository
repository = json_response['items'][0]

# accessing fields in the repository chunk
print(f'Repository name: {repository["name"]}')
print(f'Repository description: {repository["description"]}')
print(f'Repository owner\'s login: {repository["owner"]["login"]}')
