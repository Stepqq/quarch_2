import discord
from discord.ext import commands, tasks
import os
import asyncio
import random
import datetime
from discord.ext.commands import Bot
import json

def get_server_prefix(client, message):
    with open("prefixes.json", "r") as f:
       prefix = json.load(f)
        
    return prefix[str(message.guild.id)]

client = commands.Bot(command_prefix=get_server_prefix, intents=discord.Intents.all())
#bot_status = cycle(["Stat. one", "Stat. two", "Stat. Three", "Stat. Four"])

client.remove_command("help")

#connected to network check    
@client.event
async def on_ready():
    await client.tree.sync()
    print("Success: Bot is connected to Discord")

#Ping
@client.tree.command(name="ping", description="shows the bot`s latency in ms")
async def ping(interaction: discord.Interaction):
    bot_latency = round(client.latency * 1000)
    conf_embed = discord.Embed(title="successfully Pinged!", color=discord.Color.blue())
    conf_embed.add_field(name="Ping", value=f"Pong! | {bot_latency} ms.", inline=False)
    
    await interaction.response.send_message(embed=conf_embed)
    

#cogs
async def load(): 
    for filename in os.listdir("./cogs"): 
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")
            
#Prefix_add
@client.event
async def on_guild_join(guild):
    with open("prefixes.json", "r") as f:
        prefix = json.load(f)
    
    prefix[str(guild.id)] = "%"
    
    with open("prefixes.json", "w") as f:
        json.dump(prefix, f, indent=4)
 
#Prefix_delete 
@client.event
async def on_guild_remove(guild):
    with open("prefixes.json", "r") as f:
        prefix = json.load(f)
    
    prefix.pop(str(guild.id))
    
    with open("prefixes.json", "w") as f:
        json.dump(prefix, f, indent=4)          
#setprefix    
@client.command()
async def setprefix(ctx, *, newprefix: str,):
    with open("prefixes.json", "r") as f:
        prefix = json.load(f)
    
    prefix[str(ctx.guild.id)] = newprefix
    
    with open("prefixes.json", "w") as f:
        json.dump(prefix, f, indent=4)
    await ctx.channel.send("Prefix Changed")
            
#8ball
@client.tree.command(name="magic_8ball", description="getting a random response to a message") 
async def magic_8ball(interaction: discord.Interaction):
    with open("responses.txt", "r") as f: 
        random_responses = f.readlines()
        response = random.choice(random_responses)
    
    await interaction.response.send_message(f"bot say: {response}")
#avatar
@client.command(aliases=["av"]) 
async def avatar(ctx, *, member: discord.Member = None): 
    if not member:
        member = ctx.message.author
    em = discord.Embed(title=f'Аватар пользователя: ```{member}```', description= f'[Ссылка на изображение]({member.avatar})', color=member.color)
    em.set_image(url=member.avatar)
    em.set_footer(text= f'Вызвано: {ctx.message.author}', icon_url= str(ctx.message.author.avatar))
    em.timestamp = datetime.datetime.utcnow()
    await ctx.reply(embed=em, mention_author=False)
    

#mute_guild_join 
@client.event
async def on_guild_join(guild):
    with open("cogs/jsonfiles/mutes.json", "r") as f:
        mute_role = json.load(f)
        
        mute_role[str(guild.id)] = None
    
    with open("cogs/jsonfiles/mutes.json", "w") as f:
        json.dump(mute_role, f, indent=4)
#mute_remove_guild
@client.event
async def on_guild_remove(guild):
    with open("cogs/jsonfiles/mutes.json", "r") as f:
        mute_role = json.load(f)
        
        mute_role.pop(str(guild.id))
    
    with open("cogs/jsonfiles/mutes.json", "w") as f:
        json.dump(mute_role, f, indent=4)
 
 

    
#join_role
"""@client.event
async def on_guild_join(guild):
    with open("cogs/jsonfiles/autorole.json", "r") as f: 
        auto_role = json.load(f)
    
    auto_role[str(guild.id)] = None
    
    with open("cogs/jsonfiles/autorole.json", "w") as f:
        json.dump(auto_role, f, indent=4)
 
#remove_autorole_from_json 
@client.event
async def on_guild_remove(guild):
    with open("cogs/jsonfiles/autorole.json", "r") as f: 
        auto_role = json.load(f)
    
    auto_role.pop(str(guild.id))
    
    with open("cogs/jsonfiles/autorole.json", "w") as f:
        json.dump(auto_role, f, indent=4)
 """
 
#жакфреско
@client.event
async def jackfresko(self, ctx,):
        help_embed = discord.Embed(title="Secret Panel", description="???", color=discord.Color.red())

        help_embed.add_field(name="Вы активировали секретный режим", value="[ПОКАЗАТЬ СЕКРЕТ](https://www.meme-arsenal.com/memes/cef9d2a9b531d3d01ae3240eccca8194.jpg)", inline=False)
        help_embed.set_footer(text=f"еблан: {ctx.author}", icon_url=ctx.author.avatar)
        help_embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=help_embed)
 
 
 
@client.event
async def on_guild_join(guild):
    with open("cogs\jsonfiles\welcome.json", "r") as f:
        data = json.load(f)
        
    data[str(guild.id)] = {}
    data[str(guild.id)]["Channel"] = None
    data[str(guild.id)]["Message"] = None
    data[str(guild.id)]["AutoRole"] = None
    data[str(guild.id)]["ImageUrl"] = None

    with open("cogs\jsonfiles\welcome.json", "w") as f:
        json.dump(data, f, indent=4)

@client.event
async def on_guild_remove(guild):
    with open("cogs\jsonfiles\welcome.json", "r") as f:
        data = json.load(f)
        
    data.pop(str[guild.id])

    with open("cogs\jsonfiles\welcome.json", "w") as f:
        json.dump(data, f, indent=4)



    
#run client
async def main():
    async with client:
        await load()
        await client.start("MTA1MzM5NjU0NDA5NjgzMzU3Ng.GPqCd5.MD8YspaqHl2uuaJXxdRx9t8Y1kwhBvmpICLo40")

asyncio.run(main())

