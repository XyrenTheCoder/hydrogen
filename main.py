import discord, interactions, os, traceback, asyncio, math, cmath
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
    elif command == 'calculator':
        embed.add_field(name='Command name: calculator', value="Description: Open complex calculator\nUsage: `/calculator`", inline=False)
        embed.set_footer(text='1 1 2 6 24 120 720 5040 40320...')
    else:
        embed.add_field(name='General:', value="help, ping, calculator", inline=False)
        embed.add_field(name='Moderation (Server moderating permission required):', value="kick, ban", inline=False)
        embed.add_field(name='Administration (Bot owner commands):', value="load, unload, reload", inline=False)
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

### start of calculator cmd ###
e = cmath.e
pi = cmath.pi
ans = float()
def sqrt(x): return cmath.sqrt(x)
def fact(x): return math.gamma(x + 1)
def log(x, y): return cmath.log(x, y)
def nPr(n, r): return math.gamma(n + 1) / math.gamma(n - r + 1)
def nCr(n, r): return math.gamma(n + 1) / math.gamma(n - r + 1) / math.gamma(r + 1)
def sin(x): return cmath.sin(x)
def sinh(x): return cmath.sinh(x)
def arcsin(x): return cmath.asin(x)
def arcsinh(x): return cmath.asinh(x)
def cos(x): return cmath.cos(x)
def cosh(x): return cmath.cosh(x)
def arccos(x): return cmath.acos(x)
def arccosh(x): return cmath.acosh(x)
def tan(x): return cmath.tan(x)
def tanh(x): return cmath.tanh(x)
def arctan(x): return cmath.atan(x)
def arctanh(x): return cmath.atanh(x)
def sum(*args): return eval(' + '.join([str(value) for value in args]))
def sd(*args): # standard deviation population
    mean = eval(' + '.join([str(value) for value in args])) / len(args)
    g = []
    for i in args: groups = (i - mean) ** 2; g.append(groups)
    sd = sqrt(eval(' + '.join([str(value) for value in args])) / len(args) - 1)
    return sd
def sx(*args): # standard deviation sample
    mean = eval(' + '.join([str(value) for value in args])) / len(args)
    g = []
    for i in args: groups = (i - mean) ** 2; g.append(groups)
    sx = sqrt(eval(' + '.join([str(value) for value in args])) / len(args))
    return sx
def ss(data: float, mean: float, sd: float):
    z = (data - mean) / sd
    return z

button0 = [
    interactions.ActionRow(
        components=[
            interactions.Button(
                style=interactions.ButtonStyle.SUCCESS,
                label="shift",
                custom_id="inv"
            ),
            interactions.Button(
                style=interactions.ButtonStyle.SUCCESS,
                label="mode",
                custom_id="mode"
            ),
            interactions.Button(
                style=interactions.ButtonStyle.SUCCESS,
                label="hyp",
                custom_id="hyp"
            ),
        ]
    ),
    interactions.ActionRow(
        components=[
            interactions.Button(
                style=interactions.ButtonStyle.SECONDARY,
                label="7",
                custom_id="7"
            ),
            interactions.Button(
                style=interactions.ButtonStyle.SECONDARY,
                label="8",
                custom_id="8"
            ),
            interactions.Button(
                style=interactions.ButtonStyle.SECONDARY,
                label="9",
                custom_id="9"
            ),
            interactions.Button(
                style=interactions.ButtonStyle.DANGER,
                label="DEL",
                custom_id="backspace"
            ),
            interactions.Button(
                style=interactions.ButtonStyle.DANGER,
                label="AC",
                custom_id="clearall"
            )
        ]
    ),
    interactions.ActionRow(
        components=[
            interactions.Button(
                style=interactions.ButtonStyle.SECONDARY,
                label="4",
                custom_id="4"
            ),
            interactions.Button(
                style=interactions.ButtonStyle.SECONDARY,
                label="5",
                custom_id="5"
            ),
            interactions.Button(
                style=interactions.ButtonStyle.SECONDARY,
                label="6",
                custom_id="6"
            ),
            interactions.Button(
                style=interactions.ButtonStyle.PRIMARY,
                label="×",
                custom_id="multiply"
            ),
            interactions.Button(
                style=interactions.ButtonStyle.PRIMARY,
                label="÷",
                custom_id="divide"
            )
        ]
    ),
    interactions.ActionRow(
        components=[
            interactions.Button(
                style=interactions.ButtonStyle.SECONDARY,
                label="1",
                custom_id="1"
            ),
            interactions.Button(
                style=interactions.ButtonStyle.SECONDARY,
                label="2",
                custom_id="2"
            ),
            interactions.Button(
                style=interactions.ButtonStyle.SECONDARY,
                label="3",
                custom_id="3"
            ),
            interactions.Button(
                style=interactions.ButtonStyle.PRIMARY,
                label="+",
                custom_id="plus"
            ),
            interactions.Button(
                style=interactions.ButtonStyle.PRIMARY,
                label="-",
                custom_id="minus"
            )
        ]
    ),
    interactions.ActionRow(
        components=[
            interactions.Button(
                style=interactions.ButtonStyle.SECONDARY,
                label="0",
                custom_id="0"
            ),
            interactions.Button(
                style=interactions.ButtonStyle.SUCCESS,
                label=".",
                custom_id="dot"
            ),
            interactions.Button(
                style=interactions.ButtonStyle.PRIMARY,
                label="EXP",
                custom_id="exp"
            ),
            interactions.Button(
                style=interactions.ButtonStyle.PRIMARY,
                label="ANS",
                custom_id="answer"
            ),
            interactions.Button(
                style=interactions.ButtonStyle.SUCCESS,
                label="=",
                custom_id="equal"
            )
        ]
    )
]
button1 = [
    interactions.ActionRow(
        components=[
            interactions.Button(
                style=interactions.ButtonStyle.PRIMARY,
                label="√",
                custom_id="sqrt"
            ),
            interactions.Button(
                style=interactions.ButtonStyle.PRIMARY,
                label="aᵇ",
                custom_id="power"
            ),
            interactions.Button(
                style=interactions.ButtonStyle.PRIMARY,
                label="log",
                custom_id="log"
            ),
            interactions.Button(
                style=interactions.ButtonStyle.SECONDARY,
                label="(",
                custom_id="oparen"
            ),
            interactions.Button(
                style=interactions.ButtonStyle.SECONDARY,
                label=")",
                custom_id="cparen"
            )
        ]
    ),
    interactions.ActionRow(
        components=[
            interactions.Button(
                style=interactions.ButtonStyle.PRIMARY,
                label="sin",
                custom_id="sin"
            ),
            interactions.Button(
                style=interactions.ButtonStyle.PRIMARY,
                label="cos",
                custom_id="cos"
            ),
            interactions.Button(
                style=interactions.ButtonStyle.PRIMARY,
                label="tan",
                custom_id="tan"
            ),
            interactions.Button(
                style=interactions.ButtonStyle.SECONDARY,
                label="e",
                custom_id="e"
            ),
            interactions.Button(
                style=interactions.ButtonStyle.SECONDARY,
                label="π",
                custom_id="pi"
            )
        ]
    ),
    interactions.ActionRow(
        components=[
            interactions.Button(
                style=interactions.ButtonStyle.SUCCESS,
                label="+/-",
                custom_id="sign"
            ),
            interactions.Button(
                style=interactions.ButtonStyle.SECONDARY,
                label="|x|",
                custom_id="abs"
            ),
            interactions.Button(
                style=interactions.ButtonStyle.PRIMARY,
                label="%",
                custom_id="percent"
            ),
            interactions.Button(
                style=interactions.ButtonStyle.PRIMARY,
                label="n!",
                custom_id="factorial"
            ),
            interactions.Button(
                style=interactions.ButtonStyle.SECONDARY,
                label=",",
                custom_id="comma"
            )
        ]
    ),
    interactions.ActionRow(
        components=[
            interactions.Button(
                style=interactions.ButtonStyle.SUCCESS,
                label="nPr",
                custom_id="npr"
            ),
            interactions.Button(
                style=interactions.ButtonStyle.SUCCESS,
                label="nCr",
                custom_id="ncr"
            ),
            interactions.Button(
                style=interactions.ButtonStyle.PRIMARY,
                label="Σx",
                custom_id="sum"
            ),
            interactions.Button(
                style=interactions.ButtonStyle.PRIMARY,
                label="σ/s",
                custom_id="sd"
            ),
            interactions.Button(
                style=interactions.ButtonStyle.PRIMARY,
                label="z",
                custom_id="ss"
            )
        ]
    )
]
row = []
history = []
async def getans(): global ans; ans = history[-1]; print(ans); return ans
async def chyp(c: bool): global hyperbolic; hyperbolic = c
async def carc(d: bool): global inverse; inverse = d
async def display(a, arg):
    #embed = interactions.Embed(title=''.join(arg))
    await a.edit(''.join(arg), components=button0)
async def final(a, arg):
    #embed = interactions.Embed(title=arg)
    await a.edit(str(arg), components=button0)
    await gethistory(arg)
async def gethistory(arg): history.append(arg)

@bot.command(name='calculator', description='Summon calculator')
async def _5(ctx: interactions.CommandContext):
    #embed = interactions.Embed(title='h')
    await chyp(False); await carc(False)
    global a
    a = await ctx.send(components=button0); await ctx.send(components=button1)

@bot.component("0")
async def _zero(ctx: interactions.ComponentContext): row.append('0'); await display(a, row)
@bot.component("1")
async def _one(ctx: interactions.ComponentContext): row.append('1'); await display(a, row)
@bot.component("2")
async def _two(ctx: interactions.ComponentContext): row.append('2'); await display(a, row)
@bot.component("3")
async def _three(ctx: interactions.ComponentContext): row.append('3'); await display(a, row)
@bot.component("4")
async def _four(ctx: interactions.ComponentContext): row.append('4'); await display(a, row)
@bot.component("5")
async def _five(ctx: interactions.ComponentContext): row.append('5'); await display(a, row)
@bot.component("6")
async def _six(ctx: interactions.ComponentContext): row.append('6'); await display(a, row)
@bot.component("7")
async def _seven(ctx: interactions.ComponentContext): row.append('7'); await display(a, row)
@bot.component("8")
async def _eight(ctx: interactions.ComponentContext): row.append('8'); await display(a, row)
@bot.component("9")
async def _nine(ctx: interactions.ComponentContext): row.append('9'); await display(a, row)
@bot.component("plus")
async def _plus(ctx: interactions.ComponentContext): row.append(' + '); await display(a, row)
@bot.component("minus")
async def _minus(ctx: interactions.ComponentContext): row.append(' - '); await display(a, row)
@bot.component("multiply")
async def _multiply(ctx: interactions.ComponentContext): row.append(' * '); await display(a, row)
@bot.component("divide")
async def _divide(ctx: interactions.ComponentContext): row.append(' / '); await display(a, row)
@bot.component("power")
async def _power(ctx: interactions.ComponentContext): row.append(' ** '); await display(a, row)
@bot.component("sqrt")
async def _sqrt(ctx: interactions.ComponentContext): row.append('sqrt('); await display(a, row)
@bot.component("percent")
async def _percent(ctx: interactions.ComponentContext): row.append(' / 100'); await display(a, row)
@bot.component("oparen")
async def _oparen(ctx: interactions.ComponentContext): row.append('('); await display(a, row)
@bot.component("cparen")
async def _cparen(ctx: interactions.ComponentContext): row.append(')'); await display(a, row)
@bot.component("comma")
async def _comma(ctx: interactions.ComponentContext): row.append(', '); await display(a, row)
@bot.component("e")
async def _e(ctx: interactions.ComponentContext): row.append('e'); await display(a, row)
@bot.component("pi")
async def _pi(ctx: interactions.ComponentContext): row.append('pi'); await display(a, row)
@bot.component("factorial")
async def _factorial(ctx: interactions.ComponentContext): row.append('fact('); await display(a, row)
@bot.component("npr")
async def _npr(ctx: interactions.ComponentContext): row.append('nPr('); await display(a, row)
@bot.component("ncr")
async def _ncr(ctx: interactions.ComponentContext): row.append('nCr('); await display(a, row)
@bot.component("log")
async def _log(ctx: interactions.ComponentContext): row.append('log('); await display(a, row)
@bot.component("dot")
async def _dot(ctx: interactions.ComponentContext): row.append('.'); await display(a, row)
@bot.component("sign")
async def _sign(ctx: interactions.ComponentContext): row.append('-'); await display(a, row)
@bot.component("hyp")
async def _hyperbolic(ctx: interactions.ComponentContext): await chyp(True); await ctx.send('[Hyperbolic enabled]', ephemeral=True)
@bot.component("inv")
async def _shift(ctx: interactions.ComponentContext):
    await carc(True); await ctx.send('[Shift enabled]', ephemeral=True)
@bot.component("sin")
async def _sine(ctx: interactions.ComponentContext):
    global hyperbolic, inverse
    if hyperbolic and not inverse: row.append('sinh(')
    elif inverse and not hyperbolic: row.append('arcsin(')
    elif inverse and hyperbolic: row.append('arcsinh(')
    else: row.append('sin(')
    await display(a, row)
    await chyp(False); await carc(False)
@bot.component("cos")
async def _cosine(ctx: interactions.ComponentContext):
    global hyperbolic, inverse
    if hyperbolic and not inverse: row.append('cosh(')
    elif inverse and not hyperbolic: row.append('arccos(')
    elif inverse and hyperbolic: row.append('arccosh(')
    else: row.append('cos(')
    await display(a, row)
    await chyp(False); await carc(False)
@bot.component("tan")
async def _tangent(ctx: interactions.ComponentContext):
    global hyperbolic, inverse
    if hyperbolic and not inverse: row.append('tanh(')
    elif inverse and not hyperbolic: row.append('arctan(')
    elif inverse and hyperbolic: row.append('arctanh(')
    else: row.append('tan(')
    await display(a, row)
    await chyp(False); await carc(False)
@bot.component("sum")
async def _sum(ctx: interactions.ComponentContext): row.append('sum('); await display(a, row)
@bot.component("sd")
async def _sd(ctx: interactions.ComponentContext):
    global inverse
    if inverse: row.append('sx(')
    else: row.append('sd(')
    await display(a, row); await carc(False)
@bot.component("ss")
async def _ss(ctx: interactions.ComponentContext): row.append('ss('); await display(a, row)
@bot.component("exp")
async def _exp(ctx: interactions.ComponentContext): row.append(' * (10 ** '); await display(a, row)
@bot.component("abs")
async def _abs(ctx: interactions.ComponentContext): row.append('abs('); await display(a, row)
@bot.component("answer")
async def _answer(ctx: interactions.ComponentContext):
    global ans; ans = await getans()
    row.append('ans'); await display(a, row); return ans
@bot.component("equal")
async def _equal(ctx: interactions.ComponentContext): await final(a, eval(''.join(row))); row.clear()
@bot.component("clearall")
async def _clearall(ctx: interactions.ComponentContext): row.clear(); await display(a, row)
@bot.component("backspace")
async def _backspace(ctx: interactions.ComponentContext): row.pop(); await display(a, row)

### end of calculator cmd###

# end of commands #

if __name__ != __file__: keep_alive(); bot.start()
