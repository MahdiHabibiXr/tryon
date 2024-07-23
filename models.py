# from pyrogram import Client, filters
import fal_client
import requests
import os

api = 'cef3f863-e20f-4a0e-93db-2ec264b2836b:11be2dd8fe29b6b8577558e4b1c4897f'
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

def tryon(person, garment, description):
    result = fal_client.run(
        "fal-ai/idm-vton",
        arguments={
            "human_image_url": person,
            "garment_image_url": garment,
            "description": description
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
    


