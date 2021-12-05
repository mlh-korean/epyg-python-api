"""
Created on Dec 04 2021

@author: Seung Won Joeng
"""


# pip install --upgrade google-cloud-vision
# pip install python-dotenv
import os
import json
from dotenv import load_dotenv
from google.cloud import vision
import image_crawler

load_dotenv(verbose=True)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_JSON')


def detect_faces_uri(uri):
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = uri

    response = client.face_detection(image=image)
    faces = response.face_annotations

    for face in faces:
        vertices = (['({},{})'.format(vertex.x, vertex.y)
                     for vertex in face.bounding_poly.vertices])

        print('face bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    return faces


def localize_objects_uri(uri):
    client = vision.ImageAnnotatorClient()

    image = vision.Image()
    image.source.image_uri = uri

    objects = client.object_localization(
        image=image).localized_object_annotations

    print('Number of objects found: {}'.format(len(objects)))
    for object_ in objects:
        print('\n{} (confidence: {})'.format(object_.name, object_.score))
        print('Normalized bounding polygon vertices: ')
        for vertex in object_.bounding_poly.normalized_vertices:
            print(' - ({}, {})'.format(vertex.x, vertex.y))


    return objects


def extract_person(uri):
    objects = localize_objects_uri(uri)
    # extract person object only
    # print(objects)
    return [object_ for object_ in objects if object_.name == 'Person']

#
# def get_images(uri_dict, num):
#     result = {}
#
#     for k, v in uri_dict.items():
#         people = extract_person(k)
#         if len(people) >= num:
#             result[k] = v
#
#     return result


def get_images(uris, num):
    result = []
    i = 1
    for uri in uris:
        print(i)
        people = extract_person(uri)
        if len(people) >= num:
            print(uri)
            result.append(uri)
        i = i + 1
    return result


def response_images(user_input):
    # user_input = user_input.replace(' ', '').lower()
    # lst = image_crawler.image_crawler(user_input)
    # print(user_input, lst)
    # lst = get_images(lst, 0)
    lst = []
    print(lst)
    return json.dumps(lst)



# detect_faces_uri("https://d3hwaim9vs2gfj.cloudfront.net/263_20130718144847.jpg")

# localize_objects_uri("https://d3hwaim9vs2gfj.cloudfront.net/263_20130718144847.jpg")


# print(response_images("time square"))