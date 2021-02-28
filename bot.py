import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, MissingPermissions
from discord import Member
import time
import json


TOKEN = ''
PREFIX = '!'
INTENTS = discord.Intents.default()
bot = commands.Bot(command_prefix=PREFIX, intents=INTENTS)
clockedIn = []
printClockedIn = []
clockInChannel = 707774381652181092

@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user.name}')
    print(f'With ID: {bot.user.id}')
    schedule.start()
    autosave.start()
    try:
        with open("F:\downloads pt 2\discord\clockedIn.json", 'r') as listfile:
            clockedIn = json.load(listfile)
    except Exception:
            clockedIn = []
    return clockedIn





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
    await bot.process_commands(message)

@bot.command(pass_context=True)
@has_permissions(manage_roles=True)
async def add(ctx, member: Member):
    await ctx.send("hi")
    if member.id in clockedIn:
        await ctx.send("That user is already clocked in.")
    else:
        clockedIn.append(member.id)

@bot.command(pass_context=True)
@has_permissions(manage_roles=True)
async def remove(ctx, member: Member):
    if member.id in clockedIn:
        clockedIn.remove(member.id)
    else:
        await ctx.send("That user is not clocked in currently, sorry!")
    

@tasks.loop(minutes=60)
async def schedule():
    channel = bot.get_channel(clockInChannel)
    for member in clockedIn:
        await channel.send(f"<@{member}> This is a reminder you are clocked in. Please clockout if you are not patrolling.")

@tasks.loop(seconds=30)
async def autosave():
    try:
        with open("F:\downloads pt 2\discord\clockedIn.json", 'w') as listfile:
            json.dump(clockedIn, listfile)
    except Exception:
        print("Oh, no! List wasn't saved! It'll be empty tomorrow...")


bot.run(TOKEN)