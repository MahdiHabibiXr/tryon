from pyrogram import Client, filters
import time
import os
from datetime import datetime

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
        running_status = os.environ['BACKEND_ON']

        if(running_status == 'False') :
            print('BREAKING LOOP') 
            break

        tasks = [os.path.join(tasks_path, f) for f in os.listdir(tasks_path) if os.path.isfile(os.path.join(tasks_path, f))]
        
        for task in tasks :
            print(task)

        # if(task != None):

        #     task = task.split(':')
        #     style = task[2]
        #     user = task[1]
        #     photo = task[3]
        #     # if(len(task) == 4) :
        #     # photo = task[3] +':'+ task[4]

        #     gender = query.hget(user,'gender')

        #     if(gender == 'man'): prompt_index = 0
        #     else : prompt_index = 1

        #     print(f'doing task : USER[{user}], STYLE[{style}], PHOTO[{photo}], GENDER[{gender}]')
        #     prmpt = styles[int(style) - 1][prompt_index]

        #     try:
        #         r = generate_image(
        #             styles[int(style) -1][prompt_index], #prompte
        #             image_input = photo,
        #             negative_prompt = 'no face, half face, invisible face, crop face, nsfw',
        #             output_folder= f'outputdata/{user}/',
        #             batch_size= int(query.get('batch')),
        #             enable_roop= True,
        #             enable_upscale= False,
        #             step=25
        #             )
        #         # await client.send_photo(user, r[0], caption = '0')
        #         # client.send_photo(user, r[1], caption = '1')
        #         # await message.reply(f'Dont the tasks, this is the photo : {r[0]}')

        #         for i in r :
        #             # query.hset('images', 'user', user)
        #             # query.hset('images', 'photo', i)
        #             query.lpush('outputs',f'{user}:{style}:{photo}:{gender}:{i}')
        #             print('Done Task, this is photo: ' + i)
        #             await client.send_photo(int(user) , photo=i, caption='ساخته شده با @studaiobot')
        #             await client.send_photo(admin, photo=i, caption=f'Done task => {user}:{style}:{photo}:{gender}')

        #             # await client.send_photo(user, i)

        #         query.hset(user,'progress', 'False')

        #     except Exception as error:
        #         print(error)
        #         await message.reply(f'ERROR \n{user}:{style}:{photo}:{gender}\n{error}')

        #     print('=-=-=-=-=-=-=-=-=')
        #     # print('sleep for 5 sec')
        #     # time.sleep(5)
        #     # await message.reply('done task ' + task)

@bot.on_message(filters.private & filters.command('run_auto_on'))
def run_auto_on(client, message):
    os.environ['BACKEND_ON'] = 'True'
    message.reply('Running through tasks, now run /run_auto')

@bot.on_message(filters.private & filters.command('run_auto_off'))
def run_auto_on(client, message):
    os.environ['BACKEND_ON'] = 'False'
    message.reply('Tasks not doing enymore, to turn on /run_auto_on')

bot.run()