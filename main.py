import discord
from discord.ext import commands
import requests
#from replit import db
import json
import os
import time
import io
import asyncio
import aiohttp
import bs4
#from kahoot import client
import threading
import website
import sys
import random
from PIL import Image


#kahoot_bot = client()

bot = commands.Bot(command_prefix='lol ')
TOKEN = os.getenv("TOKEN")
      


@bot.event
async def on_ready():
    print(f'{bot.user} has logged into discord')
    print("Bot is ready")
    await bot.change_presence(activity=discord.Game(name='Bot is ready'))
    time.sleep(5)
    await bot.change_presence(activity=discord.Game(name='lol helpme'))


@bot.command(name='uid')
async def getuid(ctx, username):

    response = requests.get(
        f"https://api.roblox.com/users/get-by-username?username={username}")
    jsonresponse = response.json()
    await ctx.send(
        f'The Roblox userid of the user {username} is {jsonresponse["Id"]}')
    await ctx.message.add_reaction('✅')


@bot.command(name='alive?')
async def isAlive(ctx):
    await ctx.send("AlexBot is alive")
    await ctx.message.add_reaction('✅')


@bot.command(name='rbxusername')
async def rbxUsername(ctx, ping, type):
    try:
        if type == "id":
            try:
                if len(ping) == 0:
                    await ctx.send("You have to provide the userid argument")
                
                response = requests.get(
                    f"https://verify.eryn.io/api/user/{ping}")
                jsonresponse = response.json()
                status = jsonresponse['status']
                username = jsonresponse['robloxUsername']
                robloxid = jsonresponse['robloxId']

                await ctx.send(
                    f'STATUS  :{status}: The **Roblox** username of the person with the **Discord** id **{ping}** is **{username}** with the **Roblox** userid of **{robloxid}**'
                )
                await ctx.message.add_reaction('✅')
            except:
                await ctx.send(
                    f"That User probably doesent exist. Status: {status}")
                await ctx.message.add_reaction('❌')

        if type == "mention":
            try:

                if len(ping) <= 5:
                    await ctx.send("You have to provide the mention/ping")
                
                response = requests.get(
                    f"https://verify.eryn.io/api/user/{ping[3:-1]}")
                jsonresponse = response.json()
                status = jsonresponse['status']
                username = jsonresponse['robloxUsername']
                robloxid = jsonresponse['robloxId']

                await ctx.send(
                    f'STATUS  :{status}: The **Roblox** username of the person with the **Discord** id **{ping[3:-1]}** is **{username}** with the **Roblox** userid of **{robloxid}**'
                )
                await ctx.message.add_reaction('✅')
            except:
                await ctx.send(
                    f"That User probably doesent exist. Status: {status}")
                await ctx.message.add_reaction('❌')
    except:
        await ctx.send("A error has occurred")
        await ctx.message.add_reaction('❌')
    


@bot.command(name='e')
async def e(ctx):
    await ctx.message.add_reaction('🇪')
    await ctx.send("e")


@bot.command(name='helpme', aliases=['sendhelp', 'gethelp', 'ineedhelp'])
async def help(ctx):
    embed = discord.Embed(
        title='AlexBot Help', description='Help for AlexBot', color=3394815)
    embed.add_field(
        name="How to get help?",
        value='Go to the bot\'s website for help',
        inline=True)
    embed.add_field(
        name='Website Link',
        value='https://alexbot-discord.herokuapp.com',
        inline=True)

    message = await ctx.send(embed=embed)
    await ctx.message.add_reaction('✅')


@bot.command(name='nothing')
async def nothing(ctx):
    await ctx.message.delete()


@bot.command(name='latency')
async def latency(ctx):
    await ctx.send("The bot's latency is " + str(bot.latency) + " seconds")
    await ctx.message.add_reaction('📶')


@bot.command(name='spamping')
async def spamping(ctx, user, times, *args):
    if int(times) >= 50:
        await ctx.send("Hey, thats too much")
        await ctx.message.add_reaction("❌")
    elif int(times) < 50:

        for i in range(int(times)):
            await ctx.send(user + "=>" + ' '.join(args))
        await ctx.message.add_reaction('✅')


@bot.command(name='piglatin')
async def piglatin(ctx, *args):
    input = ' '.join(args)

    params = {'source': input}
    response = requests.get(
        'http://pigletapi.mkajzer.hostingasp.pl/api/translate', params=params)
    jsonresponse = response.json()
    print(jsonresponse)
    translated = jsonresponse["target"]

    if response.status_code <= 200:
        await ctx.message.add_reaction('✅')
        await ctx.send(translated)
    else:
        await ctx.send(
            f":( Sadly the api reqest has failed.This is likely due to rate limits. Status Code: {response.status_code}"
        )
        await ctx.message.add_reaction('❌')
    
    ################################################################################

    #vowel = ['A','E','I','O','U']
    #consonants = set("bcdfghjklmnpqrstvwxyz")


@bot.command(name='iss')
async def iss(ctx):
    response = requests.get("http://api.open-notify.org/iss-now.json")

    jsonresponse = response.json()

    latitude = jsonresponse["iss_position"]["latitude"]
    longitude = jsonresponse["iss_position"]["longitude"]
    await ctx.send(
        f"The international space station is at latitude {latitude} and longitude {longitude}"
    )
    await ctx.message.add_reaction('🚀')





@bot.command(name='numberinfo')
async def numberinfo(ctx, number):

    response = requests.get(f"http://numbersapi.com/{number}/math")
    if response.status_code > 200:
        await ctx.send(
            f"That is not a number (api request has failed. status code: {response.status_code})"
        )
    else:
        await ctx.send(response.text)
    await ctx.message.add_reaction('🔢')


@bot.command(name='github')
async def github(ctx, *args):
    search = ' '.join(args)
    params = {"q": search}
    response = requests.get(
        "https://api.github.com/search/repositories", params=params)
    jsonresponse = response.json()
    if jsonresponse["total_count"] >= 1:
        name = jsonresponse["items"][0]["full_name"]
        avatar = jsonresponse["items"][0]["owner"]["avatar_url"]
        embed = discord.Embed(
            title=name, description='Github Repository Found', color=3394815)
        embed.add_field(
            name="Repository Link",
            value=jsonresponse["items"][0]["html_url"],
            inline=True)
        embed.set_thumbnail(url=avatar)
        await ctx.send(embed=embed)
    else:
        await ctx.send("No results found")


@bot.command(name='bitcoin')
async def bitcoin(ctx):
    res = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
    jsonres = res.json()
    price = jsonres["bpi"]["USD"]["rate"]
    await ctx.send(
        f"The current Bitcoin price in Us dollars is {price}. Data from coinbase"
    )


@bot.command(name='spam')
async def spam(ctx, times, *args):
    message = ' '.join(args)
    if int(times) >= 50:
        await ctx.send("Hey, thats too much")
        await ctx.message.add_reaction("❌")
    elif int(times) < 50:
        for i in range(int(times)):
            await ctx.send(message)

@bot.command(name='restart')
async def restartbot(ctx):
    website.shutdownasync()
    requests.get(f"http://kahoot-spammer-api.alexairbus380.repl.co/restart")
    await bot.change_presence(activity=discord.Game(name='Restarting...'))
    await ctx.send("Restarting... please wait")
    os.system("python3 main.py")
    sys.exit();


@bot.command(name='load') #weird thing just ignore it for now
async def load(ctx, delay):
    message = await ctx.send("[          ]")
    await asyncio.sleep(float(delay))
    await message.edit(content='[==        ]')
    await asyncio.sleep(float(delay))
    await message.edit(content='[===       ]')
    await asyncio.sleep(float(delay))
    await message.edit(content='[=====     ]')
    await asyncio.sleep(float(delay))
    await message.edit(content='[======    ]')
    await asyncio.sleep(float(delay))
    await message.edit(content='[=======   ]')
    await asyncio.sleep(float(delay))
    await message.edit(content='[========  ]')
    await asyncio.sleep(float(delay))
    await message.edit(content='[========= ]')
    await asyncio.sleep(float(delay))
    await message.edit(content='[==========]')
    await ctx.send("Loading Done")


@bot.command(name='info')
async def info(ctx):
    embed = discord.Embed(title='AlexBot', description='''Programmed by: TheEpicProgrammer in Python
    Hosted on: repl.it
    Library: Discord.py
    Website: http://alexbot-discord.herokuapp.com
    Website Github Repo: https://github.com/TheEpicProgrammer/AlexBot-Website''', color=3394815)
    await ctx.send(embed=embed)


@bot.command(name='botkahoot')
async def kahoot(ctx, code):
    game_code = int(code)
    
    await ctx.send(f"Nuking Kahoot game {code} with bots")
    await ctx.send("Remember to run `lol restart` before using the kahoot botter")
    def thread1(): 
        
        for i in range(100000):
            name = "lol " + str(i)
            kahoot_bot.join(game_code, name)


    def thread2():
        for i in range(100001, 200000):
            name = "lol " + str(i)
            kahoot_bot.join(game_code, name)
    
    
    def thread3():
        for i in range(200001, 300000):
            name = "lol " + str(i)
            kahoot_bot.join(game_code, name)
    

    def thread4():
        for i in range(300001, 400000):
            name = "lol " + str(i)
            kahoot_bot.join(game_code, name)
    
    def thread5():
        for i in range(400001, 500000):
            name = "lol " + str(i)
            kahoot_bot.join(game_code, name)
    
    
    def thread6():
        for i in range(500001, 600000):
            name = "lol " + str(i)
            kahoot_bot.join(game_code, name)


    def thread7():
        for i in range(600001, 700000):
            name = "lol " + str(i)
            kahoot_bot.join(game_code, name)


    def thread8():
        for i in range(700001, 800000):
            name = "lol " + str(i)
            kahoot_bot.join(game_code, name)



    a = threading.Thread(target=thread1)
    b = threading.Thread(target=thread2)
    c = threading.Thread(target=thread3)
    d = threading.Thread(target=thread4)
    e = threading.Thread(target=thread5)
    f = threading.Thread(target=thread6)
    g = threading.Thread(target=thread7)
    h = threading.Thread(target=thread8)


    a.start()
    b.start()
    c.start()
    d.start()
    e.start()
    f.start()
    g.start()
    h.start()

    requests.get(f"http://kahoot-spammer-api.alexairbus380.repl.co/spam?code={game_code}")


@bot.command(name='broadcast')
async def broadcast(ctx, *message):
    message = ' '.join(message)
    if ctx.message.author.id == 662366683884814347:
        await ctx.send("Broadcasting")

        for guild in bot.guilds:
            for channel in guild.channels:
                if channel.name == 'general' or 'chat':
                    await channel.send(message)
    else:
        await ctx.send("NO PERMISSION!")

@bot.command(name='sbroadcast')
async def sbroadcast(ctx, *message):
    message = ' '.join(message)
    if ctx.message.author.id == 662366683884814347:
        await ctx.send("Broadcasting")

        for channel in ctx.guild.channels:
            channel = bot.get_channel(channel.id)
            await channel.send(message)

    else:
        await ctx.send("NO PERMISSION!")


@bot.command(name="getmsg") # credits to supercolbat
async def getmsg(ctx, channel: discord.TextChannel):
    loadingmsg = await ctx.send("<a:discord_loading:779085179657781251>")
    start = time.time()
    
    messages = await channel.history(limit=None).flatten()
    length = len(messages)
    chosenmsg = random.choice(messages)
    
    embed=discord.Embed(color=0xa80000)
    embed.set_thumbnail(url=chosenmsg.author.avatar_url)
    embed.add_field(name=f"Typed by {chosenmsg.author}", value=f"{chosenmsg.content}\n\n{chosenmsg.jump_url}", inline=False)
    await loadingmsg.edit(content=f"||{ctx.message.author.mention}||\n\nTime: **{time.time()-start} seconds**\nChose from {length} message{'s' if length else ''}", embed=embed)
    
    
@bot.command(name="msgquery") # original code by supercolbat, changes by me
async def msgquery(ctx, channel: discord.TextChannel, *args):
    args = ' '.join(args)

    start = time.time()
    embed=discord.Embed(color=0xa80000)
    
    # loadingmsg = await ctx.send("<a:loading:778279344346234941>")
    loadingmsg = await ctx.send("<a:discord_loading:779085179657781251>")
    messages = await channel.history(limit=None).flatten()
    length = len(messages)
    counter = 0
    # chosenmsg = []

    for i in messages:
        if args in i.content:
            embed.add_field(name=f"{i.author.display_name}", value=i.content)
            # chosenmsg.append(i.content)
            counter += 1
        
    # {chosenmsg.content}\n{chosenmsg.jump_url}", inline=False)
    await loadingmsg.edit(content=f"\n\nTime: **{time.time()-start} seconds**\nLooked through {length} message{'s' if length else ''}\nFound {counter} occurances of {args}", embed=embed)
    
@bot.command(name='pp')
async def pp(ctx, user: discord.Member):
    with requests.get(user.avatar_url) as r:
        img_data = r.content
    with open('piccys/pp.jpg', 'wb') as handler:
        handler.write(img_data)
    im = Image.open("piccys/pp.jpg")
    im = im.convert("RGB")
    im.resize((256,256))
    im.save("piccys/pp.jpg")
    file = discord.File("piccys/pp.jpg")
    await ctx.send(file=file)

website.start()
bot.run(TOKEN)

