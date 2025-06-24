from discord.ext import commands
from datetime import datetime, time, timedelta
import discord, random, subprocess, sys, os, re, asyncio

intents = discord.Intents.all()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)

admin = [639572239821570063,398896577315602442,398896577315602442]

coin = ['Heads', 'Tails']

fulllist = []
keylist = []
dolist = []

@client.event
async def on_ready():
    await readkeys()
    await client.change_presence(activity=discord.Game(name="!help"))
    print(f'citizen-helper ready!')

@client.event
async def on_message(message):

    if message.author == client.user:
        return
    if message.content.lower().startswith('!help'):
        await message.channel.send("My Commands are: \n - !help\n- !invite\n- throwacoin\n- !keybind [hint]\n\n")

    if message.content.lower().startswith('!invite'):
        await message.channel.send("Use this [invite link](https://discord.com/oauth2/authorize?client_id=1184110223477182485&permissions=8&scope=bot%20applications.commands) to add me to your servers.")

    if message.content.lower().startswith('throwacoin'):
        side = coin[random.randint(0,1)]
        await message.channel.send(side)

#Keybinds Keybinds Keybinds Keybinds Keybinds Keybinds Keybinds Keybinds Keybinds Keybinds Keybinds Keybinds Keybinds Keybinds Keybinds Keybinds Keybinds Keybinds Keybinds Keybinds Keybinds Keybinds Keybinds Keybinds Keybinds Keybinds
#Keybinds Keybinds Keybinds Keybinds Keybinds Keybinds Keybinds Keybinds Keybinds Keybinds Keybinds Keybinds Keybinds Keybinds Keybinds Keybinds Keybinds Keybinds Keybinds Keybinds Keybinds Keybinds Keybinds Keybinds Keybinds Keybinds

    if message.content.lower().startswith('!keybind '):
        search = message.content.lower()[9:]
        found = []
        output = ""
        for i in dolist:
            if search in i:
                num = dolist.index(i)
                x = keylist[num] + ": " + i
                found.append(x)
        if len(found) == 0:
            output = "Sorry. There were no entries found in my Database. Perhaps the archives are in complete.\nIf you think there's something missing, write a message after the command \"!missing\""
        else:
            for i in range(len(found)):
                output = output + found[i]
        await message.channel.send(output)

#Interaction Interaction Interaction Interaction Interaction Interaction Interaction Interaction Interaction Interaction Interaction Interaction Interaction Interaction Interaction Interaction Interaction Interaction Interaction
#Interaction Interaction Interaction Interaction Interaction Interaction Interaction Interaction Interaction Interaction Interaction Interaction Interaction Interaction Interaction Interaction Interaction Interaction Interaction

    if message.content.lower().startswith('!missing'):
        new = message.content[9:]
        with open('complaints', 'r') as note:
            stuff = note.read() + "\n" + new
        with open('complaints', 'w') as note:
            note.write(stuff)
        await message.channel.send("Message recieved. Staff will check it out soon.")
        
#Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown
#Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown

    if message.author.id in admin:
        if message.content.lower().startswith('happy birthday'):
            splits = message.content.split()
            congrats = splits[0] + ' ' + splits[1] + ' ' + splits[2] + "\nI wish you the very best and hope you'll have a fantastic year ahead."
            mes = await message.channel.send(congrats)
            await mes.add_reaction('🥳')
            await mes.add_reaction('🎂')
        if message.content.lower().startswith('!shutdown'):
            await message.channel.send('shutting down')
            await shutdown()
        if message.content.lower().startswith('!restart'):
            await message.channel.send('restarting')
            await restart_program()

async def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)

async def shutdown():
    sys.exit()
     
#Other Functions Other Functions Other Functions Other Functions Other Functions Other Functions Other Functions Other Functions Other Functions Other Functions Other Functions Other Functions Other Functions Other Functions
#Other Functions Other Functions Other Functions Other Functions Other Functions Other Functions Other Functions Other Functions Other Functions Other Functions Other Functions Other Functions Other Functions Other Functions

async def readkeys():
    with open ("keys", 'r') as keys:
        fulllist = keys.readlines()
        keys.close()
    for i in fulllist:
        tmp = i.split(" : ")
        keylist.append(tmp[0])
        try:
            dolist.append(tmp[1])
        except:
            dolist.append("")

with open('token', 'r') as t:
    token = t.read()
client.run(token)
