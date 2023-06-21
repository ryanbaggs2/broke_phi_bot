import os
import discord

# Login token for discord bot.
TOKEN = os.getenv('BROKE_PHI_BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

# Create the connection to discord.
client = discord.Client(intents=intents)

# Events are asynchronous and code is executed as a callback.
# Called when bot has finished logging in and setting things up.
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

# Called when bot has recieved a message.
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

# Run the bot with login token.
client.run(TOKEN)
