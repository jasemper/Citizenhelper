from discord.ext import commands
from datetime import datetime, time, timedelta
import discord, random, subprocess, sys, os, re, asyncio
#Infos from https://realpython.com/python-web-scraping-practical-introduction/
from urllib.request import urlopen

intents = discord.Intents.all()
intents.message_content = True
intents.members = True

botlog_id = 1180072277681901588
admin = [639572239821570063,398896577315602442]

client = discord.Client(intents=intents)

coin = ['Heads', 'Tails']
table = []

@client.event
async def on_ready():
    print(f'citizen-helper ready!')

@client.event
async def on_message(message):
    global table

    if message.author == client.user:
        return
    if message.content.lower().startswith('!help'):
        #await message.channel.send("My Commands are: \n - !help\n- !invite\n- throw a coin\n - !sc update\n - !sc all print\n - !sc ship\n - !sc cheaper\n - !sc manufacturer \n - !sc price auec\n - !sc price usd\n - !sc \n\n")
        await message.channel.send("My Commands are: \n - !help\n- !invite\n- throw a coin\n - !sc \n\n")

    if message.content.lower().startswith('!invite'):
        await message.channel.send("Use this [invite link](https://discord.com/oauth2/authorize?client_id=1184110223477182485&permissions=8&scope=bot%20applications.commands) to add me to your servers.")

#Star Citizen Star Citizen Star Citizen Star Citizen Star Citizen Star Citizen Star Citizen Star Citizen Star Citizen Star Citizen Star Citizen Star Citizen Star Citizen Star Citizen Star Citizen Star Citizen Star Citizen Star Citizen
#Star Citizen Star Citizen Star Citizen Star Citizen Star Citizen Star Citizen Star Citizen Star Citizen Star Citizen Star Citizen Star Citizen Star Citizen Star Citizen Star Citizen Star Citizen Star Citizen Star Citizen Star Citizen

    if message.content.lower().startswith('!sc update'):
        await updater()
        await message.channel.send("Table has been updated")
        await message.channel.send("You can now access the new table")

    if message.content.lower().startswith('!sc all'):
        content = message.content.lower()[:]
        await gettable()
        if "print" in content:
            for i in range(len(table[0])):
                output = ""
                for j in range(len(table)):
                     output = output + table[j][i] + "\t"
                await message.channel.send(output)

    if message.content.lower().startswith('!sc ships '):
        content = message.content.lower()[10:]
        await gettable()
        output = " "
        for i in range(len(table[0])):
            if content in table[0][i].lower():
                output = ""
                for j in range(len(table)):
                    output = output + table[j][i] + "\t"
                await message.channel.send(output)

    if message.content.lower().startswith('!sc manufacturer '):
        content = message.content.lower()[10:]
        await gettable()
        output = " "
        for i in range(len(table[0])):
            if content in table[1][i].lower():
                output = ""
                for j in range(len(table)):
                    output = output + table[j][i] + "\t"
                await message.channel.send(output)

    if message.content.lower().startswith('!sc price auec'):
        content = int(message.content.lower()[14:])
        await gettable()
        output = " "
        for i in range(len(table[0])):
            if table[7][i].lower() != '':
                if content >= int(table[7][i].lower()):
                    output = ""
                    for j in range(len(table)):
                        output = output + table[j][i] + "\t"
                    await message.channel.send(output)

    if message.content.lower().startswith('!sc price usd'):
        content = int(message.content.lower()[10:])
        await gettable()
        output = " "
        for i in range(len(table[0])):
            if content >= table[6][i].lower():
                output = ""
                for j in range(len(table)):
                    output = output + table[j][i] + "\t"
                await message.channel.send(output)


#Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown
#Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown Shutdown

    if message.author.id in admin:
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

async def updater():
    await client.wait_until_ready()
    if True:
        column_names = ["name","manufacturer","role","scu","crew","in_game_rent","price_usd_std","price_auec_buy","store_url"]
        url = "https://uexcorp.space/ships"
        page = urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")
        title_index = html.find("<!-- Ships table -->")
        start_index = title_index + len("<!-- Ships table -->")
        end_index = html.find("<!-- Footer -->")
        text_table = html[start_index:end_index]
        with open("text_uex", 'w') as file:
            file.write(text_table)
            file.close()
        name = []            #Done
        manufacturer = []   #Done
        role = []            #Done
        scu = []            #Done
        crew = []           #Done
        in_game_rent = []    #Done
        price_usd_std = []    #Done
        price_auec_buy = []    #Done
        store_url =  []        #Done
        with open ("text_uex", 'r') as file:
            lines = file.readlines()
            file.close()
        #Name
        for i in range(len(lines)):
            #manufacturer main
            if "<i class=\"fa fa-caret-down\">" in lines[i]:
                line = lines[i]
                start = line.find("</i>") + len("</i>")
                end = line.find("</span>")
                x = line[start:end]            
                x = x.replace("\t", "")
                manu = x
            #name
            if "onmouseout" in lines[i]:
                line = lines[i]
                start = line.find("title=\"") + len("title=\"")
                end = line.find("\">")
                x = line[start:end]
                name.append(x)
            if "cell-role" in lines[i]:
                #manufacturer
                manufacturer.append(manu)
                #role
                j = i+1
                line = lines[j]
                start = line.find("<span>") + len("<span>")
                end = line.find("</span>")
                x = line[start:end]
                role.append(x)
                #scu
                line = lines[j+6]
                if "<span" in line:
                    start = line.find("<span class=\"text-bold\">") + len("<span class=\"text-bold\">")
                    end = line.find("</span>")
                    x = line[start:end]
                    if "opaque" in x:
                        x = x[:len(x)-1]
                        x = x[9:]
                    if x == "":
                        x = " "
                    scu.append(x)
                #crew
                line = lines[j+3]
                start = line.find("<span>") + len("<span>")
                end = line.find("</span>")
                x = line[start:end]
                crew.append(x)
            #rent
            if "class=\"dialog-open\" rel=\".tbl-ships-rent[code=" in lines[i]:
                line = lines[i+1]
                start = line.find(",")-9
                end = line.find(",")+9
                x = line[start:end]
                x = x.replace("\t", "")
                x = x.replace(" ", "")
                x = x.replace(",", "")
                in_game_rent.append(x)
            #price ingame buy
            if "class=\"dialog-open\" rel=\".tbl-ships-sell[code=" in lines[i]:
                line = lines[i+1]
                start = line.find(",")-9
                end = line.find(",")+9
                x = line[start:end]
                x = x.replace("\t", "")
                x = x.replace(" ", "")
                x = x.replace(",", "")
                price_auec_buy.append(x)
            #price USD
            if "fa-shopping-cart" in lines[i]:
                line = lines[i+3]
                start = line.find(" $")-6
                end = line.find(" $")
                x = line[start:end]
                x = x.replace("\t", "")
                x = x.replace(" ", "")
                x = x.replace(",", "")
                price_usd_std.append(x)
            #url
            if "onmouseover" in lines[i]:
                line = lines[i]
                start = line.find("https://robertsspaceindustries.com")
                end = line.find("\" target")
                x = line[start:end]
                store_url.append(x)
        #in price_usd the first entry is 'ayed">'. This has to be deleted
        price_usd_std.pop(0)
        table = "<--colums-->\n"
        for i in column_names:
            table = table + "\"" + i + "\","
        table = table[:-1]
        table = table + "\n<--name-->\n"
        for i in name:
            table = table + "\"" + i + "\","
        table = table[:-1]
        table = table + "\n<--manufacturer-->\n"
        for i in manufacturer:
            table = table + "\"" + i + "\","
        table = table[:-1]
        table = table + "\n<--role-->\n"
        for i in role:
            table = table + "\"" + i + "\","
        table = table[:-1]
        table = table + "\n<--scu-->\n"
        for i in scu:
            table = table + "\"" + i + "\","
        table = table[:-1]
        table = table + "\n<--crew-->\n"
        for i in crew:
            table = table + "\"" + i + "\","
        table = table[:-1]
        table = table + "\n<--in_game_rent-->\n"
        for i in in_game_rent:
            table = table + "\"" + i + "\","
        table = table[:-1]
        table = table + "\n<--price_usd_std-->\n"
        for i in price_usd_std:
            table = table + "\"" + i + "\","
        table = table[:-1]
        table = table + "\n<--price_auec_buy-->\n"
        for i in price_auec_buy:
            table = table + "\"" + i + "\","
        table = table[:-1]
        table = table + "\n<--store_url-->\n"
        for i in store_url:
            table = table + "\"" + i + "\","
        table = table[:-1]
        #print(table)
        #Write everything in a comprehensive file
        with open("table", 'w') as file:
            file.write(table)
            file.close()

async def gettable():
    global table
    await client.wait_until_ready()
    #Open File
    with open ("table", 'r') as file:
        lines = file.readlines()
        file.close()
    for i in range(len(lines)):
        #names
        if "<--name-->" in lines[i]:
            names = lines[i+1][1:-2].split("\",\"")
        if "<--manufacturer-->"in lines[i]:
            manufacturer = lines[i+1][1:-2].split("\",\"")
        if "<--role-->" in lines[i]:
            role = lines[i+1][1:-2].split("\",\"")
        if "<--scu-->" in lines[i]:
            scu = lines[i+1][1:-2].split("\",\"")
        if "<--crew-->" in lines[i]:
            crew = lines[i+1][1:-2].split("\",\"")
        if "<--in_game_rent-->" in lines[i]:
            rent = lines[i+1][1:-2].split("\",\"")
        if "<--price_usd_std-->" in lines[i]:
            price_usd = lines[i+1][1:-2].split("\",\"")
        if "<--price_auec_buy-->" in lines[i]:
            price_auec = lines[i+1][1:-2].split("\",\"")
        if "<--store_url-->" in lines[i]:
            url = lines[i+1][1:-2].split("\",\"")
    table = [names, manufacturer, role, scu, crew, rent, price_usd, price_auec, url]

with open('token', 'r') as t:
    token = t.read()
client.run(token)
