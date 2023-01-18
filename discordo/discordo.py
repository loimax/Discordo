import datetime
import os
import time
import asyncio
from idk import LeagueApi
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands.errors import MissingPermissions
class MyBot(commands.Bot):

    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='/', intents=intents)
        self.remove_command("help")
        self.uptime = time.time()

    async def on_ready(self):
        await self.wait_until_ready()
        log_channel = self.get_channel(1054858473071972473)
        print("------------------------------")
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print("------------------------------")
        await log_channel.send("I'm now online on " + str(datetime.datetime.now().strftime("%A, %B %d, %Y %I:%M %p")))
        num_servers = len(self.guilds)
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{num_servers} servers"))
        

    async def on_disconnect(self):
        print('Disconnected from the Discord server!')

    async def on_guild_join(self, guild):
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(self.guilds)} servers"))
        
    async def setup_hook(self):
        # bot.tree.clear_commands(guild=bot.get_guild(614873170318459048))
        # await asyncio.sleep(3)
        nb = await self.tree.sync()
        print(f"{len(nb)} commands synced on " + str(datetime.datetime.now().strftime("%A, %B %d, %Y %I:%M %p")))
        with open(os.path.join(os.path.dirname(__file__),"avatar.png"), "rb") as f:
            avatar = f.read()
        await self.user.edit(username="LePétageDeCable", avatar=avatar)
        # await log_channel.send("Commands synced on " + str(datetime.datetime.now().strftime("%A, %B %d, %Y %I:%M %p")))
    
    async def on_command_error(self, ctx, error):
        await ctx.send(error, ephemeral=True, delete_after=5)

bot = MyBot()
@bot.hybrid_command(name="hello", with_app_command=True, description="Says hello to the user.", aliases=["hi", "hey"])
# @commands.has_permissions(manage_messages=True)
async def hello(ctx:commands.Context):
    await ctx.reply(f"Hello, {ctx.message.author.name}!")

@bot.hybrid_command(name="help", description="Shows this list of available commands.")
async def help(ctx:commands.Context):
    commands = "\n".join(["/hello\tSay hello to the bot \n",\
        "/help\tShows this list of available commands\n", \
        "/clear\tIf you have permissions, clear the channels message ; add an argument to precise how many messages to delete\n", \
        "/goodbye\tSay bye bye to the bot\n", \
        "/run\tInteract with Riot's API\n", \
        "/uptime\tShows the bot's uptime\n", \
        "/register\tRegister your summoner name to the bot"])
    embed = discord.Embed()
    embed.color = discord.Color.red()
    embed.add_field(name="**Help !**", value=f"""*Available commands !* :\n{commands}""")
    await ctx.send(embed=embed, ephemeral=False)

@bot.hybrid_command(name="goodbye", with_app_command=True, description="Says goodbye to the user.", aliases=["bye", "cya"])
async def goodbye(ctx:commands.Context):
    await ctx.reply(f"Goodbye, {ctx.message.author.name}!", )

@bot.hybrid_command(name="uptime", with_app_command=True, description="Shows the bot's uptime.", aliases=["up"])
async def uptime(ctx):
    elapsed_time = time.time() - bot.uptime
    # Calculate the elapsed time in minutes and seconds
    minutes, seconds = divmod(elapsed_time, 60)
    # Calculate the elapsed time in hours, minutes, and seconds
    hours, minutes = divmod(minutes, 60)
    # Format the elapsed time as a string in the format HH:MM:SS
    elapsed_time_str = "{:02d} hours {:02d} minutes and {:02d} seconds".format(int(hours), int(minutes), int(seconds))
    # Print the elapsed time
    await ctx.defer(ephemeral=True)
    await ctx.reply(f"I've been summoned for **{elapsed_time_str}** !", ephemeral=True, delete_after=5)



@bot.hybrid_command(name="clear", with_app_command=True, description="Clears the channel's messages.", aliases=["purge"])
@commands.has_permissions(manage_messages=True)
@commands.cooldown(1, 5, commands.BucketType.user)
@app_commands.describe(amount="The amount of messages to delete. If not specified, all messages will be deleted.")
async def clear(ctx, amount:int=999):
    await ctx.defer()
    if amount != 999:
        nb = await ctx.message.channel.purge(limit=amount+1)
        await asyncio.sleep(1)
        await ctx.message.channel.send(f"{len(nb)} messages deleted !", delete_after=5)
    else:
        await ctx.channel.purge(limit=None)
        await asyncio.sleep(1)
        await ctx.message.channel.send(f"All messages deleted for channel **{ctx.message.channel.name}**!", delete_after=5)
@clear.error
async def clear_error(ctx:commands.Context, error):
    if isinstance(error, MissingPermissions):
        await ctx.message.channel.send("You don't have the permission to do that !")
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.message.channel.send("You are on cooldown !")
    else:
        raise error

@bot.hybrid_command(name="disconnect", with_app_command=True, description="Disconnect the bot. Only the owner can use this command.")
@commands.is_owner()
async def disconnect(ctx:commands.Context):
    await ctx.reply(f"Disconnecting **{bot.user.name}**", delete_after=5)
    log_channel = bot.get_channel(1054858473071972473)
    await log_channel.purge(limit=None)
    await log_channel.send(f"""I'm now offline | Time : {str(datetime.datetime.now().strftime("%A, %B %d, %Y %I:%M %p"))}""", delete_after=5)
    await asyncio.sleep(6)
    await bot.close()
@disconnect.error
async def disconnect_error(ctx:commands.Context, error):
    if isinstance(error, commands.NotOwner):
        await ctx.message.channel.send("You must be the bot owner to use this command !")
    else:
        raise error
@bot.hybrid_command(name="register", with_app_command=True, description="Register your summoner name to the bot.")
async def register(ctx:commands.Context, summoner_name:str):
    """Registers the user's summoner name with the bot."""
    with open(os.path.join(os.path.dirname(__file__),'register.txt'), 'r') as f:
        if str(ctx.message.author) in f.read():
            await ctx.reply("Your summoner name is already registered.", ephemeral=True, delete_after=10)
            return
        if summoner_name == "":
            await ctx.reply("Please add your summoner name : /register <summoner_name>\ne.g. : /register yall r bad", ephemeral=True, delete_after=20)
            return
    with open(os.path.join(os.path.dirname(__file__),'register.txt'), 'a') as f:
        f.write(f"{ctx.message.author}:{summoner_name}\n")
    await ctx.reply("Your summoner name has been registered.", ephemeral=True, delete_after=10)

@bot.hybrid_command(name="lol_info", with_app_command=True, description="Get your infos")
async def lol_info(ctx:commands.Context): #, args:discord.app_commands.Choice[int]):
    name = await check_register(ctx)
    # print(name)
    if name:
        instance = LeagueApi(name)
        instance.my_infos(str(ctx.message.author))
        await print_tmp(ctx)
        await ctx.reply("Here are your infos!")
        os.remove(os.path.join(os.path.dirname(__file__),f'tmp_{ctx.message.author}.txt'))

@bot.hybrid_command(name="lol_ranked_stats", with_app_command=True, description="Get a your ranked stats")
async def lol_stats(ctx:commands.Context):
    name = await check_register(ctx)
    # print(name)
    if name:
        instance = LeagueApi(name)
        instance.ranked_stats(str(ctx.message.author))
        await ctx.reply("Here are your ranked stats!")
        await print_tmp(ctx)
        os.remove(os.path.join(os.path.dirname(__file__),f'tmp_{ctx.message.author}.txt'))
@bot.hybrid_command(name="lol_champ_info", with_app_command=True, description="Get a champion's stats")
async def lol_champ_info(ctx:commands.Context, champ_name:str):
    name = await check_register(ctx)
    # print(name)
    if name:
        instance = LeagueApi(name)
        instance.print_one_champion_infos(champ_name.capitalize(), str(ctx.message.author))
        await ctx.reply(f"Here are {champ_name.capitalize()} champion's infos!")
        await print_tmp(ctx)
        os.remove(os.path.join(os.path.dirname(__file__),f'tmp_{ctx.message.author}.txt'))
@bot.hybrid_command(name="lol_match_stats", with_app_command=True, description="Get one of your match's stats")
@app_commands.describe(match_number="The match number you want to see (0-9, 0 being the latest)", args="The stats you don't want to see ; learn more in /help", file="True : the bot sends you the stats in a file | False : stats sent as raw text")
async def lol_match_stats(ctx:commands.Context, match_number:int, args:str, file=True):
    name = await check_register(ctx)
    if not 0<=match_number<=9:
        await ctx.reply("Please enter a valid match number (0-9)", ephemeral=True, delete_after=10)
        return
    elif name:
        instance = LeagueApi(name)
        stats_choice = []
        args = args.replace(" ", "")
        args = " ".join(args)
        stats_choice = args.split()
        # instance.print_a_match_stats(match_number, stats_choice)
        instance.new_print(match_number, stats_choice, str(ctx.message.author), file)
        await ctx.reply("Here are your stats!", ephemeral=True, delete_after=10)
        if file:
            #rename the file
            os.rename(os.path.join(os.path.dirname(__file__),f'tmp_{ctx.message.author}.txt'), os.path.join(os.path.dirname(__file__),f'{ctx.message.author}_stats.txt'))
            await ctx.send(file=discord.File(os.path.join(os.path.dirname(__file__),f'{ctx.message.author}_stats.txt')))
            os.remove(os.path.join(os.path.dirname(__file__),f'{ctx.message.author}_stats.txt'))
        else:
            await print_tmp(ctx)
            os.remove(os.path.join(os.path.dirname(__file__),f'tmp_{ctx.message.author}.txt'))
        return
    
    
async def check_register(ctx:commands.Context):
    with open(os.path.join(os.path.dirname(__file__), "register.txt"), "r") as f:
        register = f.read()
        name = ""
        for line in register.splitlines():
            if str(ctx.message.author) in line:
                name = line.split(":")[1]
                return name
    if name == "":
        await ctx.reply("You need to register your summoner name first ! Use /register <summoner_name>", ephemeral=True, delete_after=5)
        return None

async def print_tmp(ctx:commands.Context):
    if (os.stat(os.path.join(os.path.dirname(__file__),f'tmp_{ctx.message.author}.txt')).st_size) < 2000:
        with open(os.path.join(os.path.dirname(__file__),f'tmp_{ctx.message.author}.txt'), 'r') as f:
            file_content = f.read()
            await ctx.message.channel.send(file_content)
    elif 2000 < (os.stat(os.path.join(os.path.dirname(__file__),f'tmp_{ctx.message.author}.txt')).st_size):
        with open(os.path.join(os.path.dirname(__file__),f'tmp_{ctx.message.author}.txt'), 'r') as f:
            buf = ""
            count = 0
            for line in f:
                buf += line
                count+=1
                if count == 10:
                    # print(buf)
                    await ctx.message.channel.send(buf)
                    buf = ""
                    count = 0
            # print(buf)
            await ctx.message.channel.send(buf)
            
with open(os.path.join(os.path.dirname(__file__),'data.sec'), 'r') as f:
    token = f.readlines()[1]
bot.run(token)

"""
Ancient print :
            # buf = ""
            # count = 0
            # for line in f:
            #     buf += line
            #     if line.startswith("-"):
            #         if count == 1:
            #             await ctx.message.channel.send(buf)
            #             buf = ""
            #             count = 0
            #             continue
            #         count += 1
            #     elif len(buf) >= 1500:
            #         if not line.isspace() and line != "":
            #             await ctx.message.channel.send(buf)
            #         else :
            #             await ctx.message.channel.send("\u200B")
            #         buf = ""
            #         count = 0 """