import math
from discord.ext import commands
from discord.ext.commands import *

class ErrorHandler(commands.Cog):
    def __init__(self, client): self.client = client
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'): return
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None: return
        ignored = commands.CommandNotFound
        error = getattr(error, 'original', error)
        if isinstance(error, ignored): return
        if isinstance(error, commands.MissingRequiredArgument): await ctx.send('Missing required argument(s).')
        if isinstance(error, commands.MissingPermissions): await ctx.send("You dont have the permission to do that. :eyes:")
        if isinstance(error, BotMissingPermissions): await ctx.send('I don\'t have the required permissions to use this.')
        if isinstance(error, BadArgument): await ctx.send('Invalid argument')
        if isinstance(error, commands.CommandOnCooldown):
            if math.ceil(error.retry_after) < 60: await ctx.reply(f'This command is on cooldown. Please try after {math.ceil(error.retry_after)} seconds')
            elif math.ceil(error.retry_after) < 3600: ret = math.ceil(error.retry_after) / 60; await ctx.reply(f'This command is on cooldown. Please try after {math.ceil(ret)} minutes')
            elif math.ceil(error.retry_after) >= 3600:
                ret = math.ceil(error.retry_after) / 3600
                if ret >= 24: r = math.ceil(ret) / 24; await ctx.reply(f"This command is on cooldown. Please try after {r} days")
                else: await ctx.reply(f'This command is on cooldown. Please try after {math.ceil(ret)}')

async def setup(client): await client.add_cog(ErrorHandler(bot))

'''
how to use cooldowns:
after @commands.command() add @commands.cooldown(1, cooldown, commands.BucketType.user)
'''



#btw i use arch