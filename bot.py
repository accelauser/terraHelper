import os

from discord import Client, Intents
from dotenv import load_dotenv

from responses import Handler
#https://github.com/indently/discord_tutorial_2024

#NOQA

intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)
handler = Handler()

async def sendMessage( message, userMessage):
    if not userMessage:
        print('Message was empty, lack of intent')
        return
    if is_private := userMessage[0] == '?':
        userMessage = userMessage[1::]
    try: 
        response = handler.handle_responses(userMessage)
        if is_private:
            await message.author.send(response)
        else:
            await message.channel.send(response)
    except Exception as e:
        print(e)    

@client.event
async def on_ready():
    print(f'{client.user} is on running!')

@client.event   
async def on_message(message):
    if message.author == client.user:
        return
    userName = str(message.author)
    userMessage = str(message.content)
    channel = str(message.channel)

    print(f'\nOn {channel}, by {userName}: {userMessage}')
    await sendMessage(message, userMessage)

def main():
    load_dotenv()
    TOKEN = (os.getenv('DISCORD_TOKEN'))  
    client.run(TOKEN)#NOQA

if __name__ == "__main__":
    #runs the bot 
    main()