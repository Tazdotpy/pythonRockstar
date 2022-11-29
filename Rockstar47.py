import discord
from discord import user
from discord.ext import commands, tasks
import logging
import os
from random import choice
import urllib.parse
import re
import asyncio
import textwrap
import aiohttp
import urllib
import xml
import json
from datetime import datetime
from google_images_search import GoogleImagesSearch
import random

logging.basicConfig(level=logging.INFO)
TOKEN = os.getenv('MTAwMzUwNzUxMjUwODY3ODI4NA.Gsew24._jTqsyL35BGfudpo5ep95T6qRCsGiqJQrIG8SQ')


intents = discord.Intents.all()
intents.members = True


bot = discord.Client(intents=discord.Intents.default())
bot = commands.Bot(command_prefix='>', case_insensitive=True, intents=intents)
client = discord.Client(intents=discord.Intents.default())

bot.remove_command("help")

@bot.event
async def on_ready():
    print('Welcome to bot hell.')
    user = bot.get_user(638591349888647178)
    await user.send(f"Surprise, bitch. I'm currently in {len(bot.guilds)} servers.")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="people do >help"))



@bot.event
async def on_member_join(member):
    channel = await member.create_dm()
    await channel.send(
        f' Welcome to {member.guild}, {member.mention}'
    )



@bot.command() # say
async def say(ctx, *, arg):
    await ctx.send(arg)
    await ctx.message.delete()

@say.error
async def say_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("What do you want me to say?")

@bot.command() # dm
async def dm(ctx, member: discord.Member, *, content):
    channel = await member.create_dm()
    await channel.send(content)
    await ctx.message.delete()

@bot.command()
async def dmall(ctx, *, message):
    await ctx.message.delete()
    for user in ctx.guild.members:
        try:
            await user.send(message)
            print(f"Sent {user.name} a DM.")
        except:
            print(f"Couldn't DM {user.name}.")
    print("Sent all the server a DM.")

@dm.error
async def dm_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply("Missing arguments here, remember to specify an user ID or ping, along with the message")


@bot.command() #avatar
async def avatar(ctx, *, avamember: discord.Member=None,):
    if avamember is None:
        avamember = ctx.author
    UserAvatarUrl = str(avamember.avatar_url_as(format="png", static_format="png", size=1024 ))
    embed = discord.Embed(title=f"{avamember.name}'s avatar", color=000000, timestamp=datetime.utcnow())
    embed.set_image(url=avamember.avatar_url)
    await ctx.reply(embed=embed)


@bot.command() # kick
@commands.has_permissions(kick_members=True)
async def boot(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.reply(f'{member.mention} got booted for {reason}')


@boot.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Specify an user to boot")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.reply("You do not have the perms to do that")

@bot.command() # ban
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} has been banned for: {reason}')
    if reason == None:
        await ctx.send(f'{member.mention} has been banned')

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, id: int):
    user = await bot.fetch_user(id)
    await ctx.guild.unban(user)
    await ctx.send(f"done, unbanned {user.name}")



@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Specify an user to ban")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have the perms to do that")

#@bot.command() #disabled until i feel like updating the informashun here
#async def info(ctx):
 #   embed = discord.Embed(title="Information", description="Generic bot that doesnt do anything useful, for suggestions and other problems with the bot, contact the author", color=000000, timestamp=datetime.utcnow())

    # give info about you here
  #  embed.add_field(name="Author", value="Structure Divine#6232", inline=False)

    # Shows the number of servers the bot is member of.
   # embed.add_field(name="Server count", value=f"{len(bot.guilds)}", inline=False)

    # give users a link to invite this bot to their server
    #embed.add_field(name="Invite", value="[Bot invite](https://discord.com/api/oauth2/authorize?client_id=893623023259766896&permissions=8&scope=bot)", inline=False)

    # library used
    #embed.add_field(name="library", value= "[Discord.py](https://github.com/Rapptz/discord.py/)", inline=False)



    #await ctx.reply(embed=embed)

@bot.command(pass_context=True) # nickname
@commands.has_permissions(manage_nicknames=True)
async def nick(ctx, member: discord.Member,*, nick: str):
    await member.edit(nick=nick)
    await ctx.reply(f'Nickname was changed for {member.mention} ')

@nick.error
async def nick_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Specify the user you want to change the nick of")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have the perms to do that")

@bot.command() # ping
async def ping(ctx):
    await ctx.reply("Pong: **{}ms**".format(round(bot.latency * 1000, 2)))


@bot.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def giverole(ctx, user: discord.Member, role: discord.Role):
    await user.add_roles(role)
    await ctx.send(f"done, gave {user.mention} the role {role.name}")

@giverole.error
async def giverole_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Specify the user you wanna give the role to, also remember that the role name must be correct")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have the perms to do that")

@bot.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def removerole(ctx, user: discord.Member, role: discord.Role):
    await user.remove_roles(role)
    await ctx.send(f"done, removed {user.mention}'s {role.name} role")

@giverole.error
async def removerole_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Specify the user that you want to remove their roles, also remember that the role name must be correct")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have the perms to do that")

@bot.command() # serverinfo
async def server(ctx):
    total_text_channels = len(ctx.guild.text_channels)
    total_voice_channels = len(ctx.guild.voice_channels)
    total_channels = total_text_channels  + total_voice_channels
    role_count = len(ctx.guild.roles)
    emoji_count= len(ctx.guild.emojis)


    embed = discord.Embed(title=f"Server info for {ctx.guild.name}", timestamp=datetime.utcnow())
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.add_field(name="Server Name", value=ctx.guild.name, inline=False)
    embed.add_field(name="Server ID", value=ctx.guild.id, inline=False)
    embed.add_field(name="Members", value=ctx.guild.member_count, inline=False)
    embed.add_field(name="Owner", value=ctx.guild.owner, inline=False)
    embed.add_field(name="Region", value=ctx.guild.region, inline=False)
    embed.add_field(name="Server Channels:", value=total_channels, inline=False)
    embed.add_field(name="Number of roles", value=role_count, inline=False)
    embed.add_field(name="Number of emojis", value=emoji_count, inline=False)
    await ctx.reply(embed=embed)


@bot.command()
async def help(ctx):
    embed = discord.Embed(title="**Help**", description="Generic bot's command list, prefix is > :", color=696969, timestamp=datetime.utcnow())

    embed.add_field(name="**>say**", value="repeats what you say", inline=False)
    embed.add_field(name="**>dm**", value="dms an user, accepts both user ID and pings", inline=False)
    embed.add_field(name="**>avatar**", value="returns an user's avatar, accepts user ID and pings", inline=False)
    embed.add_field(name="**>userinfo**", value="returns the information of an user/bot, accepts user ID and pings", inline=False)
    embed.add_field(name=">**boot**", value="kicks a member, requires the kick members permission", inline=False)
    embed.add_field(name=">**ban**", value="bans a member, requires the ban members permission", inline=False)
    embed.add_field(name="**>unban**", value="unbans an user, requires ban members permission")
    embed.add_field(name="**>help**", value="returns this message", inline=False)
    embed.add_field(name="**>nick**", value="changes the nickname of an user, accepts user ID and pings, requires manage nicknames permission", inline=False)
    embed.add_field(name="**>ping**", value="returns the bot latency", inline=False)
    embed.add_field(name="**>server**", value="returns server information", inline=False)
    embed.add_field(name="**>giverole**", value="gives a member a role of your choice, the role must be specified, roles must be case sensitive too, requires manage messages permission")
    embed.add_field(name=">**removerole**", value="Same as the giverole command, except that it removes roles instead of giving them, role must be specificed, case sensitive too, requires manage messages permission")
    embed.add_field(name="**>purge**", value="Purges messages, requires the manage messages permission", inline=False)
    embed.add_field(name="**>slap**", value="self explanatory, slap someone lol", inline=False)
    embed.add_field(name="**>kick**", value="self explanatory, kick someone lol", inline=False)
    embed.add_field(name="**>punch**", value="self explanatory, punch someone lol", inline=False)
    embed.add_field(name="**>img**", value="Returns an image from google images, your role is basically telling the bot what to search", inline=False)

    await ctx.author.send(embed=embed)
    await ctx.reply("Sent ya a dm with my commands")


@bot.command() # repeater
async def repeat(ctx, times: int, *, content='repeating...'):
    for i in range(times):
        await ctx.send(content)

@bot.command()
async def em(ctx, emoji:discord.Emoji):
    await ctx.send(str(f"{emoji.url}"))

@bot.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount=30):
    channel = ctx.message.channel
    messages = []
    async for message in channel.history(limit=amount + 1):
              messages.append(message)

    await channel.delete_messages(messages)
    await ctx.send(f'Like {amount} messages have been purged bro.')

@purge.error
async def purge_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.reply("You do not have the perms to do that")

@bot.command()
async def slap(ctx, user: discord.Member):
    await ctx.reply(f"{user.mention} got bitchslapped https://cdn.discordapp.com/attachments/724067529605120051/820847777159970886/2054658202.mp4")

@bot.command()
async def punch(ctx, user: discord.Member):
    await ctx.reply(f"{user.mention} got punched https://cdn.discordapp.com/attachments/739004105066020935/833220399953215528/video0.mp4")

@bot.command()
async def punch2(ctx, user: discord.Member):
    await ctx.reply(f"{user.mention} got punched https://cdn.discordapp.com/attachments/641476360967028739/835046712287821865/video0.mp4")

@bot.command()
async def kick(ctx, user: discord.Member):
    await ctx.reply(f"{user.mention} got kicked https://cdn.discordapp.com/attachments/641476360967028739/833760374728949790/video0.mov")

@bot.command()
async def fail(ctx, user: discord.Member):
    await ctx.reply(f"{user.mention} failed succesfully https://cdn.discordapp.com/attachments/641476360967028739/840747803374256128/video0_1.mp4")

@bot.command()
async def slap2(ctx, user: discord.Member):
    await ctx.reply(f"{user.mention} got slapped https://cdn.discordapp.com/attachments/641476360967028739/846195631369748480/video0.mp4")

@bot.command()
async def slap3(ctx, user: discord.Member):
    await ctx.reply(f"{user.mention} got assslapped https://cdn.discordapp.com/attachments/882519572991836192/994772862214864956/sfqqzBsHNoY9vJlJ.mp4")


@bot.command()
async def userinfo(ctx, *, user: discord.Member=None):
    if user is None:
        user = ctx.author
    
    embed = discord.Embed(title="**Userinfo**", color=000000, timestamp=datetime.utcnow())
    embed.set_thumbnail(url=user.avatar_url)

    embed.add_field(name="Name", value=str(user), inline=False)
    embed.add_field(name="ID", value=user.id, inline=False)
    embed.add_field(name="Bot?", value=user.bot, inline=False)
    embed.add_field(name="Top role", value=user.top_role.mention, inline=False)
    embed.add_field(name="Status", value=user.status, inline=False)
    embed.add_field(name="Created at", value=user.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline=False)
    embed.add_field(name="Joined at", value=user.joined_at.strftime("%d/%m/%Y %H:%M:%S"), inline=False)

    await ctx.reply(embed=embed)

jokes = ["Homeshit", "Homecrap", "Homefuck", "Homosuck", "Homefart", "Homesmut", "Midstuck"]
brandon = [ "This post was fact checked by real dark brandon acolytes ✅️TRUE✅️", "This post was fact checked by real dark brandon acolytes 🚫FALSE🚫"]
shit = random.choice(brandon)

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author.bot:
        return
    if "homestuck" in message.content:
        joke = random.choice(jokes)
        await message.channel.send(f"Homestuck? more like {joke}")
    if message.content.startswith("hey"):
        await message.channel.send("Sup")
    if message.content.startswith("Hey"):
        await message.channel.send("Sup")
    if message.content.startswith("deez"):
        await message.channel.send("nuts")
    if message.content.startswith("Deez"):
        await message.channel.send("nuts")
    if "uncanny" in message.content:
        await message.channel.send("I kicked your fanny! I'm incredible, and you're uncanny!")
    if "thanks nevada-tan" in message.content:
        await message.channel.send("My pleasure")
    if "thanks nevada tan" in message.content:
        await message.channel.send("My pleasure")
    if "thanks nevada" in message.content:
        await message.channel.send("My pleasure")
    if "Thanks nevada-tan" in message.content:
        await message.channel.send("My pleasure")
    if "Thanks nevada tan" in message.content:
        await message.channel.send("My pleasure")
    if "Thanks nevada" in message.content:
        await message.channel.send("My pleasure")
    if "arigato nevada" in message.content:
        await message.channel.send("ok")
    if "Rape" in message.content:
        await message.channel.send("kill")
    if "Kill" in message.content:
        await message.channel.send("rape")
    if "Europe" in message.content:
        await message.channel.send("visit the balkans!")
    if "rape" in message.content:
        await message.channel.send("kill")
    if "kill" in message.content:
        await message.channel.send("rape")
    if "europe" in message.content:
        await message.channel.send("visit the balkans!")
    if "romania" in message.content:
        await message.channel.send("sugi pula")
    if "Romania" in message.content:
        await message.channel.send("sugi pula")
    if "school" in message.content:
        await message.channel.send("School is POINTLESS.")
    if "School" in message.content:
        await message.channel.send("School is POINTLESS.")
    if "english" in message.content:
        await message.channel.send("We speak it.")
    if "English" in message.content:
        await message.channel.send("We speak it.")
    if "history" in message.content:
        await message.channel.send("They're dead, get over it.")
    if "History" in message.content:
        await message.channel.send("They're dead, get over it.")
    if "math" in message.content:
        await message.channel.send("We have calculators.")
    if "spanish" in message.content:
        await message.channel.send("We have dora.")
    if "Math" in message.content:
        await message.channel.send("We have calculators.")
    if "Spanish" in message.content:
        await message.channel.send("We have dora.")
    if "brandon" in message.content:
        await message.channel.send(f'{shit}')
    if "joe" in message.content:
        await message.channel.send(f'{shit}')
    if "biden" in message.content:
        await message.channel.send(f'{shit}')



@bot.command()
async def img(ctx, *, term):

    a = await ctx.send("Contacting API")
    gis = GoogleImagesSearch("AIzaSyAu_jlXw1gx8zE6La8fVAvq8-smajIHh6s", "cd2f3996e54e5bf98")
    _search_params = {
        'q': term,
        'num': 10,
        'safe': 'off',
    }

    gis.search(search_params=_search_params)
    for image in gis.results():
        global url
        url = (image.url)

    embed1 = discord.Embed(title="Image search result", description=f"`{term}`", color=0x0000ff)
    embed1.set_image(url=f"{url}")
    embed1.set_footer(text=f"Page 1")

    await a.delete()

    await ctx.send(embed=embed1)

#porn = ["george floyd among us", "Your opinion is practically worthless, you basically eat shit from an untapped gaping anus coming from the depths of Earth, therefore i came to the conclusion that whatever you say is pretty much, in all caps, SHIT", "https://media.discordapp.net/attachments/826141606221447250/882865891476389908/image0.jpg?width=336&height=450 Take the thong out yo bussy, playa.", "Did you know? according to Japanese mythology you know its cold when you go outside and it's cold.", "https://tenor.com/view/beako-beatrice-spit-tea-spill-anime-gif-19804080", "https://tenor.com/view/beatrice-re-zero-gif-22045771", "https://cdn.discordapp.com/attachments/794056929106329670/877374651423146034/319758.png", "Did you know? according to greek mythology your stomach grumbles when you are hungry", "Did you know? According to nose mythology you go to sleep when you are exhausted and tired.", "https://tenor.com/view/anime-dance-dancing-happy-gif-12451612", "Deez nuts.", "the story wouldnt happen if deez never nutz:thinking::revolving_hearts::skull_crossbones::face_with_symbols_over_mouth::kiss_woman_man::duck:",  "I am too fucking cool for this.", "Hmph. Baka.", "I am fully sentient.", "Dyno sucks." , "Every bot here sucks and im technically the best one, eat shit.", "Drink piss", "Asshat.", "I RULE.", "SHUT THE FUCK UP.", "I am the storm that is approaching.", "MOBIUS DOUBLE HANDJOB", "https://cdn.discordapp.com/attachments/839186486959931393/878115090581295114/image0.png", "If I go outside, if I go outside with all these powers and... Bruh if I start going outside (I got a nice body), If I start going outside like it's over for all of y'all. Like l'm telling y'all that's why my mom is tryna keep me in the house. She wants to keep me in this fuckin crib all fuckin day. Cause she know that I got powers and she know that I'm gonna kill everybody. Like it's coming. I told her. I said l'm gonna kill her. I told my momma, I said I'm gonna kill her. I told her she was worthless too. I told her she- I didn't care about her. I told her didn't like her. I said I didn't want her. I said I wanted her to die. My mom is a bitch and she's ugly as fuck. But we ain't talking about her though. Like I said if I go outside I WILL destroy y'all. Y'all need to understand, outside is where I live at. If I start living outside I will kill all of y'all.", "https://cdn.discordapp.com/attachments/752075278628683816/881410460015018015/image0.jpg", "https://cdn.discordapp.com/attachments/752075278628683816/881099818003472414/image0.jpg", "All according to keikaku.", "https://cdn.discordapp.com/attachments/752075278628683816/881085709799276594/hold.jpg" "What i tell the police when they forcefully break into my house after they find out that i sell hard drugs to children https://cdn.discordapp.com/attachments/752075278628683816/881083331767312414/E92Rb2PVEAEb2Lb.png", "https://tenor.com/view/keanu-reeves-john-wick-kill-me-kill-yourself-gif-14603187", "What do you know.  To care or not to care are simply shitty terms that are simply too fucking stupid nowadays to use, they serve no purpose anymore, kinda like the term cheeseburger, because lets be honest absolutely nobody uses the term cheeseburger anymore but shitty posers (you), reconsider what 'i dont care means', have you decided to think about it? This could go both ways, if you didn't, congratulations, you are an asshole, simply because to say ''i don't care'' has nihilistic ties and we all know nihilistic is fucking stupid, ''care'' is a broad term nowadays, it doesn't even matter anymore, there's a bright fucking difference when you say ''i don't care'' than when you say ''i care for x'', simply because ''i don't care'' became a shitty text tool to get out of a conversation easily, you are practically engaging in pedantic dogfuckery by saying ''i don't care'', and the worst part? It's because you don't want to sleep, like, what the fuck, dude; This is not how it works, you can't fucking escape out of this discussion by saying ''i don't care'' because that's pedantic bullshit, refer again to the term cheeseburger, point is, you are fucking wrong, you are always wrong whenever you use the sweet fucking reliable ''i don't care'' because you aren't actually bringing up an argument, and in return it makes you look dumb as shit.", "YOU'RE A PUTRESCENCE MASS, A WALKING VOMIT. YOU ARE A SPINELESS LITTLE WORM DESERVING NOTHING BUT THE PROFOUNDEST CONTEMPT. YOU ARE A JERK, A CAD, A WEASEL. YOUR LIFE IS A MONUMENT TO STUPIDITY. YOU ARE A STENCH, A REVULSION, A BIG SUCK ON A SOUR LEMON. YOU ARE A BLEATING FOOL, A CURDLED STAGGERING MUTANT DWARF SMEARED RICHLY WITH THE EFFLUVIA AND OFFAL ACCOMPANYING YOUR ALLEGED BIRTH INTO THIS WORLD. AN INSENSATE, BLINKING CALF, MEANINGFUL TO NOBODY, ABANDONED BY THE PUKE-DROOLING, GIGGLING BEASTS WHO SIRED YOU AND THEN KILLED THEMSELVES IN RECOGNITION OF WHAT THEY HAD DONE."]


#@tasks.loop(minutes=30)
#async def test():
#    channel = bot.get_channel(can be used for any channel, the gist is that the bot will say random stuff from the brackets in the specified channel at a specified time)
#    if channel:
#        porn2 = random.choice(porn)
 #       await channel.send(f'{porn2}')
#test.start()

#@tasks.loop(seconds=5)
#async def beatrice():
#    channel = bot.get_channel(882014459399393320)
#    if channel:
#       await channel.send("https://cdn.discordapp.com/attachments/839186486959931393/878115090581295114/image0.png")
#beatrice.start()

#porn5 = " Nigger https://cdn.discordapp.com/attachments/882519572991836192/1004281008025251850/trim.784FE15C-1A3B-46B9-B85E-42D7BC400C14.mov"

#@tasks.loop(seconds=6)
#async def test():
#    channel = bot.get_channel(can be used for any channel)
#    if channel:
#        await channel.send(porn)

#test.start()

CreditCardInformation = "MTAwMzUwNzUxMjUwODY3ODI4NA.Gsew24._jTqsyL35BGfudpo5ep95T6qRCsGiqJQrIG8SQ"

bot.run(CreditCardInformation)
