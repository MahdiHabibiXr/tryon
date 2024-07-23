# from pyrogram import Client, filters
import fal_client
import requests
import os

api = '3f51e6d3-95fc-4e05-92be-7d8af9ec4847:b5dead8944d8f01002aff2f0e195b1c1'

os.environ['FAL_KEY'] = api

def upload(image_address):
    file = open(image_address, 'rb')
    file_bytes = file.read()

    file: bytes = file_bytes
    url = fal_client.upload(file, "image/jpeg")

    return url


def sdxl(prompt):
    result = fal_client.run(
        "fal-ai/fast-lightning-sdxl",
        arguments={
            "prompt": f'{prompt}',
        },
    )

    return result['images'][0]['url']


def swap(base, face):
    result = fal_client.run(
        "fal-ai/face-swap",
        arguments={
            "base_image_url": base,
            "swap_image_url": face
        },
    )

    return result

def tryon(person, garment, description, type):
    result = fal_client.run(
        "fal-ai/idm-vton",
        arguments={
            "human_image_url": person,
            "garment_image_url": garment,
            "description": description,
            "garment_type" : type
        },
    )

    export = [
        result['image']['url'],
        result['mask']['url']
    ]
    
    return export

def change_api(key):
    os.environ['FAL_KEY'] = api

#TODO: I should get the remaining credit of any api
#def get_credit(key):
    


