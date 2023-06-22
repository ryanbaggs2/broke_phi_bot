import os
import discord
from discord.ext import commands

# Login token.
TOKEN = os.getenv('BROKE_PHI_BOT_TOKEN')

# The API that the bot will need permissions for.
# Privileged intents must be configured in app settings on:
# https://discord.com/developers/applications
intents = discord.Intents.default()
intents.message_content = True

# Create a bot session and specify the prefix to commands.
bot = commands.Bot(command_prefix='$', intents=intents)

# Events are asynchronous and code is executed as a callback.
# Called when bot has finished logging in and setting things up.
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# Prints bot information as a discord message.
@bot.command()
async def info(ctx, cmd ='info'):
    await ctx.send('''I am Broke Phi Bot, I ain\'t got it.
    \nEnter the command you would like to do in the format:  $[command] [arguments]
    Example: $info info
    \nAdd quotes around multiple word arguments.
    Example: $command \"Why do I like Dead by Daylight?\"
    \nThe command $list gives a list of all commands.''')

# Run the bot with login token.
bot.run(TOKEN)
