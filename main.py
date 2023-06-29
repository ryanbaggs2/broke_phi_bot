import os
import discord
from discord.ext import commands
import requests
import json
import re

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
    global content
    with open('appdata', mode='w+') as f:
        r = requests.get('https://api.steampowered.com/ISteamApps/GetAppList/v2/')
        content = r.json()
        f.write(json.dumps(content))
    
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

# Sets a notification for when a game reaches a specific price point.
@bot.command()
async def notify(ctx, game_name, price):
    apps = content['applist']

    results = search(game_name, apps)
    
    game_info = await verify_result(ctx, results)

    result_name = game_info['name']

    print(f'{result_name}')

# Searches for possible matches in the list of apps using regular expressions.
def search(game_name, apps):
    pattern = re.compile(re.escape(game_name), re.IGNORECASE)

    results = []
    for app in apps['apps']:
        name = app['name']
        if re.search(pattern, name):
            results.append(app)

    return results

# Get the user requested result.
async def verify_result(ctx, results):
    if len(results) == 0:
        return None
    if len(results) == 1:
        return results[0]
    
    await ctx.send('''Multiple matches, enter the number that matches 
    \nthe game you\'re looking for''')

    for index, result in enumerate(results, start=1):
        name = result['name']
        if index <= 5:
            await ctx.send(f'{index}. {name}')

    msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)

    return results[int(msg.content) - 1]

# Run the bot with login token.
bot.run(TOKEN)
