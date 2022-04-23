# treedweller.py
import os
import random

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.command(pass_context=True, name='sponsor')
async def sponsor(ctx):
    user = ctx.message.author
    await user.send(f'This is a one-use invite to Requiem that will last for one hour. Please send it to the person '
                    f'you wish to invite.\r\n{await ctx.channel.create_invite(max_age = 86400, max_uses = 1)}')

@bot.command(name='roll')
async def roll(ctx, numdice: int, numside: int):
    dice = [
        str(random.choice(range(1,numside+1)))
        for _ in range (numdice)
    ]
    await ctx.send(', '.join(dice))
bot.run(TOKEN)
