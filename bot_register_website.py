import time
import random
import string
import requests

#Define the URL of the registration page
registration_url = ''

#Define the list of proxies as IP addresses
proxy_list = [
    #' ',
    #Add more proxies as needed
]

def generate_random_string(length=8):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))

def register_user_with_proxy(proxy):
    #Generate random username and password
    #Add fields here if you need other registration details e.g. YOB, Address etc.
    random_username = generate_random_string(8)
    random_password = generate_random_string(10)
    
    #Fill out the registration form data
    registration_data = {
        'username': random_username,
        'password': random_password,
        #Add other registration fields as needed
    }

    try:
        response = requests.post(registration_url, data=registration_data, proxies={'http': proxy, 'https': proxy})
        if response.status_code == 200:
            print(f"User '{random_username}' registered successfully using proxy {proxy}")
        else:
            print(f"Failed to register user using proxy {proxy}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Failed to register user using proxy {proxy}: {e}")

#Iterate over the list of proxies
for proxy in proxy_list:
    #Register a user using the current proxy
    register_user_with_proxy(proxy)
    
    #Add a delay before switching to the next proxy (optional)
    time.sleep(random.randint(3, 5))