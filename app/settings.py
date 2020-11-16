import os

TIMEOUT = 30

URLS = {
    'alib': 'https://alib.com.ua/'
}

BASE_URL = os.getenv('ENV') if os.getenv('ENV') else URLS.get('alib')

USER_EMAIL = ''
