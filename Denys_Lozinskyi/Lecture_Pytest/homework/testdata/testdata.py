### STATIC DATA ###

url = 'http://0.0.0.0:5002/'

correct_credentials = (
    {'user_name': 'test', 'password': 'test'},
    {'user_name': 'test', 'password': 'test'},
    {'user_name': 'test', 'password': 'test'},
)

incorrect_credentials = (
    {'user_name': 'test', 'password': ''},
    {'user_name': '', 'password': 'test'},
    {'user_name': 'tets', 'password': 'test'},
)

resources = (
    {'name': 'Tesla'},
    {'name': 'Falcon9'},
)


### DYNAMIC DATA ###

access_token = ''
resource_id = []
