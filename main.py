import discord, interactions, os, traceback, asyncio
from discord.ext import commands
from discord.ext.commands import *
from keep_alive import keep_alive

oid = ['705462972415213588', '706697300872921088']
with open('token.txt', 'r') as f: token = f.readline()
bot = interactions.Client(token=token)
client = commands.Bot(command_prefix='.', intents=discord.Intents.all())
# command prefix remains unused, all commands are slash commands currently
# note: 'client' for discord.py related code, 'bot' for interactions.py related code

@bot.event
async def on_start():
    os.system('cls') if os.name == 'nt' else 'clear'
    print('Reminder: remember to run /load errorHandler to enable error handler as cogs are not preloaded.')

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
    else: await ctx.send(f'{ctx.author}, confirm shutdown?', components=button, ephemeral=True)
@bot.component("yes")
async def _yes(ctx: interactions.ComponentContext):
    await ctx.send('Halting...\nPlease dismiss previous messages to avoid misclicking.', ephemeral=True); await asyncio.sleep(5)
    raise SystemExit('Shutdown triggered')
@bot.component("no")
async def _no(ctx: interactions.ComponentContext): await ctx.send("Action cancelled.\nPlease dismiss previous messages to avoid misclicking.", ephemeral=True)

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
async def _0(ctx: interactions.CommandContext): await ctx.send(f"Client latency: {round(bot.latency * 1000)}ms", ephemeral=True)

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
    elif command == 'kick':
        embed.add_field(name='Command name: kick', value="Description: Kick a member from server\nUsage: `/kick <member: user> [reason: reason]`", inline=False)
        embed.set_footer(text='I wonder what they did wrong, hmmm...')
    elif command == 'ban':
        embed.add_field(name='Command name: ban', value="Description: Ban a member from server\nUsage: `/ban <member: user> <reason: reason>`", inline=False)
        embed.set_footer(text='The ban hammer has spoken.')

    else:
        embed.add_field(name='General:', value="help, ping", inline=False)
        embed.add_field(name='Moderation:', value="kick, ban", inline=False)
        embed.add_field(name='Administration:', value="load, unload, reload", inline=False)
        embed.set_footer(text='Specify a command to get further information.')
    await ctx.send(embeds=embed, ephemeral=True)

@bot.command(name='kick', description='Kick a user', options=[
    interactions.Option(
        name='member',
        description='Target user',
        type=interactions.OptionType.USER,
        required=True
    ),
    interactions.Option(
        name='reason',
        description='Reason of kick',
        type=interactions.OptionType.STRING,
        required=False
    )
])
@commands.cooldown(1, 5, commands.BucketType.user)
@commands.has_permissions(kick_members=True)
@commands.guild_only()
async def _2(ctx: interactions.CommandContext, member: interactions.Member, *, reason=None):
    await member.kick(int(ctx.guild_id), reason=reason)
    embed = interactions.Embed(title=f'User {member} has kicked successfully.')
    embed.set_footer(text=f'Action by {ctx.author} | {ctx.author.id}')
    if reason == None: embed.add_field(name='Reason:', value='Not provided')
    else: embed.add_field(name='Reason:', value=reason)
    await ctx.send(embeds=embed)

@bot.command(name='ban', description='Ban a user', options=[
    interactions.Option(
        name='member',
        description='Target user',
        type=interactions.OptionType.USER,
        required=True
    ),
    interactions.Option(
        name='reason',
        description='Reason of ban',
        type=interactions.OptionType.STRING,
        required=True
    )
])
@commands.cooldown(1, 5, commands.BucketType.user)
@commands.has_permissions(ban_members = True)
@commands.guild_only()
async def _3(ctx: interactions.CommandContext, member: interactions.Member, *, reason: str):
    await member.ban(int(ctx.guild_id), reason=reason)
    embed = interactions.Embed(title=f'User {member} has banned successfully.')
    embed.add_field(name='Reason:', value=reason)
    embed.set_footer(text=f'Action by {ctx.author} | {ctx.author.id}')
    await ctx.send(embeds=embed)

'''
@bot.command(name='mute', description='Mute a user', options=[
    interactions.Option(
        name='member',
        description='Target user',
        type=interactions.OptionType.USER,
        required=True
    ),
    interactions.Option(
        name='reason',
        description='Reason of mute',
        type=interactions.OptionType.STRING,
        required=False
    )
])
@commands.has_permissions(mute_members=True)
@commands.cooldown(1, 5, commands.BucketType.user)
@commands.guild_only()
async def _4(ctx: interactions.CommandContext, member: interactions.Member, reason=None):
    all = await interactions.Guild.get_all_roles(self=interactions.Guild())
    if 'Mute' in all: role = discord.utils.get(all, name='Muted')
    else:
        role = await ctx.guild.create_role(name="Muted")
        for channel in ctx.guild.channels: await channel.set_permissions(role, speak=False, send_messages=False, read_message_history=True, read_messages=False)
    embed = interactions.Embed(title=f"User {member.mention} was muted successfully.")
    if reason == None: embed.add_field(name='Reason:', value='Not provided')
    else: embed.add_field(name="Reason:", value=reason, inline=False)
    embed.set_footer(text=f'Action by {ctx.author} | {ctx.author.id}')
    await ctx.send(embeds=embed)
    await member.add_role(role, int(ctx.guild_id), reason=reason)
    await member.send(f"You have been muted from: {ctx.guild.name}\nreason: {reason}")
'''

# end of commands #

if __name__ != __file__: keep_alive(); bot.start()