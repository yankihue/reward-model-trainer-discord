import discord
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()
token = os.getenv("token")
data = pd.read_csv("unranked_outputs.csv")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot_state = False
async def display_message(message):
    global bot_state
    index = int(open('pos', 'r').read())
    if index < len(data):
        to_send = 'index: {0}\nOutput 1: {1}{2}\nOutput 2:{1}{3} \n\nWhich one seems more positive to you? Respond with the number 1 or 2. \n If neither of them is positive, type 3.'.format(index, data.loc[index, "prompt"], data.loc[index, "chosen"],data.loc[index, "rejected"])
    else:
        to_send = 'All of the output has been ranked!\n'\
                  '----------END----------'
    await message.channel.send(to_send)


client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    global bot_state

    if message.author == client.user:
        return

    _content = message.clean_content.lower()
    if _content.find('start trainer') > -1:
        await message.channel.send('----------------START--------------')
        await display_message(message)

    elif(_content=="1" or _content=="2" or _content=="3"):
        print("here")
        index = int(open('pos', 'r').read())
        open('pos', 'w').write(str(index + 1))
        data.loc[index, "marked"] = 1
        if (_content=="1"):
            print("chosen")
        if (_content=="2"):
            data.loc[index, "chosen"], data.loc[index,"rejected"] = data.loc[index, "rejected"], data.loc[index,"chosen"]
        elif (_content=="3"):
            data.loc[index, "marked"] = 2 # 2 means neither of them is positive, 1 means its been selected correctly
        data.to_csv("unranked_outputs.csv", index=False)
        await display_message(message)
    elif(_content=="undo"):
        index = int(open('pos', 'r').read())
        open('pos', 'w').write(str(index - 1))
        data.loc[index-1, "marked"] = 0
        data.to_csv("unranked_outputs.csv", index=False)
        await message.channel.send('Last feedback deleted from dataset. Go again:\n\n')
        await display_message(message)
    elif(_content=="end trainer"):
        await message.channel.send('Pausing trainer for now. Type "start trainer" to start again.')
        await message.channel.send('Thank you for your help!')

client.run(token)