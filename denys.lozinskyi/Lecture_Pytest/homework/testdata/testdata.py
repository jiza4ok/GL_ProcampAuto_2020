### STATIC DATA ###

# Credentials
correct_credentials = (
    {'user_name': 'test', 'password': 'test'},
    {'user_name': 'test', 'password': 'test'},
)

incorrect_credentials = (
    {'user_name': 'test', 'password': ''},
    {'user_name': '', 'password': 'test'},
    {'user_name': 'tets', 'password': 'test'},
)

# Tokens
empty_tokens = (None, '', ' ')

# Resources
resource = {'name': 'Tesla'}
