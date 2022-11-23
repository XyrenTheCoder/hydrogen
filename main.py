import discord, interactions, os, traceback, asyncio
from discord.ext import commands
from discord.ext.commands import *
from keep_alive import keep_alive

oid = ['705462972415213588', '706697300872921088']
client = commands.Bot(command_prefix='.', intents=discord.Intents.all())
with open('token.txt', 'r') as f: token = f.readline()
bot = interactions.Client(token=token)
# note: 'client' for discord.py related code, 'bot' for interactions.py related code

@bot.event
async def on_ready():
    os.system('cls') if os.name == 'nt' else 'clear'
    print('Reminder: remember to run /load errorHandler to enable error handler.')

### config ###
button = [
    interactions.ActionRow(
        components=[
            interactions.Button(
                style=interactions.ButtonStyle.PRIMARY,
                label="Confirm",
                custom_id="yes"
            ),
            interactions.Button(
                style=interactions.ButtonStyle.DANGER,
                label="Cancel",
                custom_id="no"
            )
        ]
    )
]
@bot.command(name='halt', description='Shutdown bot')
async def halt(ctx: interactions.CommandContext):
    if ctx.author.id not in oid: await ctx.send('You can\'t use this command.')
    else: await ctx.send(f'{ctx.author}, confirm shutdown?', components=button)

@bot.component("yes")
async def _yes(ctx: interactions.ComponentContext):
    await ctx.send('Halting...'); await asyncio.sleep(5)
    raise SystemExit('Shutdown triggered')

@bot.component("no")
async def _no(ctx: interactions.ComponentContext): await ctx.send("Action cancelled.")

@bot.command(name='load', description='Load cog', options=[
    interactions.Option(
        name="arg1",
        description="Cog name",
        type=interactions.OptionType.STRING,
        required=True
    )
])
async def load(ctx: interactions.CommandContext, arg1: str):
    if ctx.author.id in oid:
        try: await client.load_extension(f'cogs.{arg1}'); await ctx.send("Loaded cog"); return
        except Exception: await ctx.send(f'Cog could not be loaded.\nDue to:\n```{traceback.format_exc()}```')
    else: await ctx.send(f"You can\'t use this command"); return


@bot.command(name='unload', description='Unload cog', options=[
    interactions.Option(
        name="arg1",
        description="Cog name",
        type=interactions.OptionType.STRING,
        required=True
    )
])
async def unload(ctx: interactions.CommandContext, arg1: str):
    if ctx.author.id in oid:
        try: await client.unload_extension(f'cogs.{arg1}'); await ctx.send("Unloaded cog"); return
        except Exception: await ctx.send(f'Cog could not be unloaded.\nDue to:\n```{traceback.format_exc()}```')
    else: await ctx.send(f"You can\'t use this command"); return

@bot.command(name='reload', description='Reload cog', options=[
    interactions.Option(
        name="arg1",
        description="Cog name",
        type=interactions.OptionType.STRING,
        required=True
    )
])
async def reload(ctx: interactions.CommandContext, arg1: str):
    if ctx.author.id in oid:
        try: await client.unload_extension(f'cogs.{arg1}'); await client.load_extension(f'cogs.{arg1}'); await ctx.send("Reloaded Cog"); return
        except Exception: await ctx.send(f'Cog could not be reloaded.\nDue to:\n```{traceback.format_exc()}```')
    else: await ctx.send(f"You can\'t use this command"); return
### end of config ###

# commands #
@bot.command(name="ping", description="Get client latency")
@commands.cooldown(1, 5, commands.BucketType.user)
async def _0(ctx: interactions.CommandContext): await ctx.send(f"Client latency: {round(bot.latency * 1000)}ms")

@bot.command(name='help', description='Helps', options=[
    interactions.Option(
        name='command',
        description='Command name for query, default None',
        type=interactions.OptionType.STRING,
        required=False
    )
])
@commands.cooldown(1, 5, commands.BucketType.user)
async def _1(ctx: interactions.CommandContext, command=None):
    embed = interactions.Embed(title="**-- Commands --**")
    if command == 'help':
        embed.add_field(name='Command name: help', value="Description: Helps\nUsage: `/help [command: command name]`", inline=False)
        embed.set_footer(text='Why do you even need help for this? ._.')
    elif command == 'ping':
        embed.add_field(name='Command name: ping', value="Description: Gets client latency\nUsage: `/ping`", inline=False)
        embed.set_footer(text='Ping is kinda high...')
    else:
        embed.add_field(name='Category0:', value="help, ping", inline=False)
        embed.add_field(name='Administration:', value="load, unload, reload", inline=False)
        embed.set_footer(text='Specify a command to get further information.')
    await ctx.send(embeds=embed)
# end of commands #

if __name__ != __file__: keep_alive(); bot.start()