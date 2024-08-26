import models
from pyrogram import Client, filters
from PIL import Image 
import os
from pyrogram.types import ReplyKeyboardMarkup as Markup
from models import upload, tryon
import requests
from io import BytesIO

# bot_api = '6752497249:AAE_1UP_pVxNd3vMsKXnIA6QEbvIGRplUfU'
# bot = Client('mahdi',api_id=863373,api_hash='c9f8495ddd20615835d3fd073233a3f6')
root = 'files/'
bot = Client('mahdi')
STEP = 'home'

@bot.on_message(filters.command('test') & filters.private)
async def test_bot(client, message):
    await message.reply('im upppp')

@bot.on_message(filters.command('start') & filters.private)
async def start(client, message):
    msg = 'Hi, This is a demo for Studaio Try-on Feature, First send me a photo of the person you want to try on it.'

    await message.reply(msg)

@bot.on_message(filters.private & filters.photo)
async def image(client, message):
    chat_id = message.chat.id

    user_root = f'{root}{chat_id}/'
    file_name = ''
    
    
    if(os.path.exists(f'{user_root}person.jpg') and os.path.exists(f'{user_root}garment.jpg')):
        #both photos are sent
        await message.reply('You have submitted person and garment images before\nto submit new images, Use the commans: /edit')
    else:
        if(not os.path.isdir(user_root)):
            #first time sending photo so we create the user dir
            os.makedirs(user_root)
            file_name = 'person.jpg'
            await message.reply('Person image submitted, Now send me a upper body garment image.')

        elif(not os.path.exists(f'{user_root}person.jpg') and not os.path.exists(f'{user_root}garment.jpg')):
            #sent person photo
            file_name = 'person.jpg'
            await message.reply('Person image submitted, Now send me a upper body garment image.')

        elif(os.path.exists(f'{user_root}person.jpg') and not os.path.exists(f'{user_root}garment.jpg')):
            #sent garment
            file_name = 'garment.jpg'
            await message.reply('Ok now use the command /imagine_upper (for upperbody garment) or /imagine_lower (for lowerbody garment) or /imagine_dress (for dress garment) and describe the garment in order to generate the photo, example \n /imagine_upper black t shirt')
        
            
        file = await client.download_media(message.photo.file_id, file_name = f'{user_root}{file_name}')

@bot.on_message(filters.private & filters.regex('/edit'))
async def edit_image(client, message):
    #edit both files
    chat_id = message.chat.id
    person_img = f'{root}{chat_id}/person.jpg'
    garment_img = f'{root}{chat_id}/garment.jpg'

    if(os.path.exists(person_img)):
        os.remove(person_img)
    if(os.path.exists(garment_img)):
        os.remove(garment_img)

    await message.reply('Ok, Please me a photo of the person you want to try on it.')

@bot.on_message(filters.private & filters.regex('/imagine_'))
async def imagine(client, message):

    chat_id = message.chat.id
    person_img = f'{root}{chat_id}/person.jpg'
    garment_img = f'{root}{chat_id}/garment.jpg'
    description = ''
    garment_type = ''#upper_body lower_body dress
    
    if(message.text.startswith('/imagine_upper')): 
        garment_type = 'upper_body'
        description = message.text.replace('/imagine_upper', '')

    elif(message.text.startswith('/imagine_lower')): 
        garment_type = 'lower_body'
        description = message.text.replace('/imagine_lower', '')

    elif(message.text.startswith('/imagine_dress')): 
        garment_type = 'dress'
        description = message.text.replace('/imagine_dress', '')

    if(os.path.exists(person_img) and os.path.exists(garment_img)):
        if(description and garment_type):
            task_path = f'tasks/{chat_id}.txt'

            if(os.path.exists(task_path)):
                message.reply('You have a pending request ....')
            else:
                person_url = upload(person_img)
                garment_url = upload(garment_img)

                #adding a task
                with open(task_path, 'w') as file:

                    file.write(description)     #description
                    file.write(garment_type)    #type
                    file.write(person_url)      #person
                    file.write(garment_url)     #cloth
                    file.write(str(chat_id))    #user
                    

                # #generate image

                await message.reply(f'Generating your image**{description}**, it can take up to 1 min, Please wait')

                # img, msk = tryon(person_url, garment_url, description, garment_type)
                # downloaded_path = download_image(img, chat_id)
                # await client.send_photo(chat_id, downloaded_path, caption='You generated image')

                # resized = resize_image(person_img ,downloaded_path)
                # await client.send_photo(chat_id, resized, caption='your resized image')

            # await message.reply(img)
            # await message.reply(msk)

        else:
            await message.reply('You should send description for the garment with this format : /imagine_upper black shirt')
    else:
        await message.reply('You should submit both person and garment images, Use /images to check ')
    
@bot.on_message(filters.private & filters.regex('/images'))
async def images(client, message):
    chat_id = message.chat.id
    person_img = f'{root}{chat_id}/person.jpg'
    garment_img = f'{root}{chat_id}/garment.jpg'

    if(os.path.exists(person_img)):
        await client.send_photo(chat_id, person_img, caption='your person image')
    if(os.path.exists(garment_img)):
        await client.send_photo(chat_id, garment_img, caption='your garment image')
    if(not os.path.exists(person_img) and not os.path.exists(garment_img)):
        await message.reply('No images has been submitted, Send person image.')


@bot.on_message(filters.private & filters.regex('/save'))
async def save(client, message):
    chat_id = message.chat.id
    url = message.text.split(' ')[1]

    downloaded_path = download_image(url, chat_id)
    await client.send_photo(chat_id, downloaded_path, caption='your image')

@bot.on_message(filters.private & filters.regex('/resize'))
async def resize(client, message):
    chat_id = message.chat.id
    person_img = f'{root}{chat_id}/person.jpg'
    garment_img = f'{root}{chat_id}/garment.jpg'
    target = 'outputs/791927771-1.jpg'

    resized = resize_image(person_img, target)
    await client.send_photo(chat_id, resized, caption='resized image')

@bot.on_message(filters.private & filters.command('run_auto_on'))
def run_auto_on(client, message):
    os.environ['BACKEND_ON'] = 'True'
    message.reply('Running through tasks, now run /run_auto')

@bot.on_message(filters.private & filters.command('run_auto_off'))
def run_auto_on(client, message):
    os.environ['BACKEND_ON'] = 'False'
    message.reply('Tasks not doing enymore, to turn on /run_auto_on')

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