# + 'by user:' + (['data'][x]['from']['username'])

from paralleldots.config import set_api_key, get_api_key
import json
import requests

PD_URL = 'https://apis.paralleldots.com/'

API_KEY = '1I4xTjI50WTBqxFDGiY8QxB3tZdH9v3IejZI7PSrqRk'

set_api_key('1I4xTjI50WTBqxFDGiY8QxB3tZdH9v3IejZI7PSrqRk')


input = raw_input('Enter Text:')

request_url = PD_URL + 'sentiment?sentence1=%s&apikey=%s' % (input,API_KEY)
response = requests.get(request_url, verify = False ).json()

print response
