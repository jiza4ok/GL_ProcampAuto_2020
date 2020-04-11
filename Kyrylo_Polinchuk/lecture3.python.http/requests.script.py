import requests
url0='http://localhost:5002/'
response=requests.get(url0)
print(response.status_code)
response2=requests.get(url0)
print(response2.status_code)
response3=requests.get(url0)
print(response3.status_code)
print(response.json())

url='https://github.com/SergiiButenko/GL_ProcampAuto_2020'
response4=requests.get(url)
print(response4.status_code)

url1='https://api.github.com/search/repositories'

response5=requests.get(url1,params={'q':'GL_ProcampAuto_2020'})
json_response5=response5.json()
repository=json_response5['items'][0]
print(f'Repository name: {repository["name"]}')
print(f'Repository description: {repository["description"]}')

response6=requests.post(url0,json={'serbut':'value'})
print((response6))
json_response6=response6.json()
print(f'Response: {json_response6}')

from requests.auth import HTTPBasicAuth
response7=requests.get(url0+"basic_auth", auth=HTTPBasicAuth('sergii','hello'))
print(response7.text)
response8=requests.post(url0+'login', json={'username': 'test', 'password':'test'})
print(response8.json())
token=response8.json()['access_token']
print(f'token: {token}\n')
print("Send not authoraized request")
response9=requests.get(url0+"protected")
print(response9.text)

print("Send authoraized request")
response10=requests.get(url0+"protected",headers={'Authorization':f'Bearer {token}'})
print(response10.text)

