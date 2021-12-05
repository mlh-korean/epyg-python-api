"""
Created on Dec 04 2021

@author: Seung Won Joeng
"""


# pip install google-cloud-translate==2.0.1
# pip install geopy

## Here: google cloud translate and google cloud maps

import os
import six
import requests
import urllib.parse
import json
from dotenv import load_dotenv
from google.cloud import translate_v2 as translate
from geopy.geocoders import Nominatim
from lib import countryToLanguageMapping as mapping

load_dotenv(verbose=True)
# Global Variables
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_JSON')
# target_lang = 'EN'  # default = EN
translate_client = translate.Client()
LIST_LANGUAGES = translate_client.get_languages()  # Get all supported languages


#
# client = translate.Client()
# result = client.translate('안녕하세요', target_language='ja')
# print(result['translatedText'])

def get_location(user_input):
    query = urllib.parse.quote(user_input)
    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=" + query + "&inputtype=textquery&fields=formatted_address%2Cname%2Crating%2Copening_hours%2Cgeometry&key=" + os.getenv(
        'GOOGLE_KEY')
    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.json()

    lat = response['candidates'][0]['geometry']['location']['lat']
    lng = response['candidates'][0]['geometry']['location']['lng']

    return lat, lng


def response_location(user_input):
    t = get_location(user_input)
    d = {"lat": t[0], "lng": t[1]}
    return json.dumps(d)


def get_code(user_input):
    # Using geopy to get country
    lat, lng = get_location(user_input)
    geolocator = Nominatim(user_agent='geoapi-tester')
    location = geolocator.reverse(str(lat) + "," + str(lng), language='en')
    add = location.raw['address']
    country = add.get('country_code', '')

    code = mapping.countryToLanguageMapping.get(country)

    try:
        code = code.split(',')[0]
    except:
        print("No multi-languages")

    # print(code)

    return code


def translate_input(user_input):
    if isinstance(user_input, six.binary_type):
        user_input = user_input.decode('utf-8')
    result = translate_client.translate(user_input)

    language_code = get_code(user_input)

    if language_code == 'en':
        return result['translatedText']

    else:
        another_result = translate_client.translate(user_input, target_language=language_code)
        return result['translatedText'], another_result['translatedText']
