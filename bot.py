import discord
from discord.ext import commands, tasks
import time


TOKEN = ''
PREFIX = '!'
INTENTS = discord.Intents.default()
bot = commands.Bot(command_prefix=PREFIX, intents=INTENTS)
clockedIn = []
clockInChannel = 806001968682237972

@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user.name}')
    print(f'With ID: {bot.user.id}')



@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.event
async def on_message(message):
    if message.channel.id == clockInChannel:
        if message.content == "?clockin game":
            if message.author.id in clockedIn:
                print(f"{message.author} just tried to clock in twice, please check there is no errors!")
            else:
                clockedIn.append(message.author.id)
    
    if message.channel.id == clockInChannel:
        if message.content == "?clockout game":
            clockedIn.remove(message.author.id)
    print(clockedIn)
    print(len(clockedIn))
 
    

@tasks.loop(minutes=60)
async def schedule():
    channel = bot.get_channel(clockInChannel)
    print("test")
    for member in clockedIn:
        await channel.send(f"<@{member}> This is a reminder you are clocked in. Please clockout if you are not patrolling.")

    


bot.run(TOKEN)