"""
Created on Dec 05 2021

@author: Seung Won Joeng
"""


# pip install flask
from flask import Flask, request
import os
from google.cloud import translate_v2 as translate
import translator  # For google cloud translator basic
import trends

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World'


@app.route('/location', methods=['POST'])
def search_location():
    param = request.get_json()
    return translator.response_location(param['place'])


@app.route('/trends', methods=['POST'])
def search_trends():
    param = request.get_json()

    translated = translator.translate_input(param['place'])  # translate to English
    response = ""

    if isinstance(translated, tuple):
        response = trends.response_trends(translated[1])
    else:
        response = trends.response_trends(translated)

    return response


@app.route('/images', methods=['POST'])
def search_images():
    return -1


if __name__ == '__main__':
    app.run(debug=True)  # true mode: restart
