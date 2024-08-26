from pyrogram import Client, filters
import time
import os
from datetime import datetime
import time
import models
from PIL import Image 
import requests
from io import BytesIO

admin = 791927771
bot = Client('mahdi2',api_id=863373,api_hash='c9f8495ddd20615835d3fd073233a3f6' )
# bot = Client(
#     'mahdi'
#     # plugins=plugins
#     )
tasks_path = 'tasks'


@bot.on_message(filters.private & filters.command('run_auto'))
async def task_run(client,message):
    # await message.reply('AutoPilot ON')
    print('Going to run tasks : ')

    while(True):

        tasks = [os.path.join(tasks_path, f) for f in os.listdir(tasks_path) if os.path.isfile(os.path.join(tasks_path, f))]
        
        for task in tasks :
            with open(task, 'r') as file:
                content = file.read()
                lines = content.splitlines()

                description = lines[0]
                type = lines[1]
                person_url = lines[2]
                garment_url = lines[3]
                user = lines[4]
                person_img = f'files/{user}/person.jpg'

                if(type and task and description): #make sure the task is valid
                    print(f'Doing the task for {user} type {type} desc {description}')

                    try :
                        img, msk = models.tryon(person_url, garment_url, description, type)
                        downloaded_path = download_image(img, user)
                        resized = resize_image(person_img ,downloaded_path)
                        await client.send_photo(int(user) , photo=resized, caption='Your Generated Image')
                        await client.send_photo(admin, photo=resized, caption = f'Task Done {user}')

                    except Exception as error:
                        print(error)
                        await message.reply(f'ERROR \n{user}:\n{error}')
                        await client.send_message(int(user), 'An error occured')

                

            print('=-=-=-=-=-=-=-=-=')
            print('sleep for 20 sec')
            time.sleep(20)
            await message.reply('done task ' + task)
            os.remove(f'tasks/{user}.txt')


def download_image(url, id):
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))

    count = len(os.listdir('outputs/')) + 1
    filename = f"outputs/{id}-{count}.jpg"

    image.save(filename)
    print(f'Image successfully downloaded and saved as {filename}')

    return filename

def resize_image(target, source):
    # Open the target image and the source image
    target_image = Image.open(target)
    source_image = Image.open(source)

    # Get the size of the target image
    target_size = target_image.size

    # Resize the source image to match the size of the target image
    resized_source_image = source_image.resize(target_size)

    # Save the resized image (optional)
    resized_source_image.save(source)

    # Display the resized image (optional)
    resized_source_image.show()

    return(source)

bot.run()