# treedweller.py
import os
import random
import sqlite3
import string

import discord
from discord.ext import commands
from dotenv import load_dotenv

# LOAD ENVIRONMENT VARIABLES FROM LOCAL .ENV FILE
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# connect to db
con = sqlite3.connect('treedweller.db')
cur = con.cursor()

# SET COMMAND PREFIX
bot = commands.Bot(command_prefix='!')


# BOT COMMANDS
@bot.command(pass_context=True, name='sponsor')
async def sponsor(ctx):
    user = ctx.message.author
    code = uniquecode()
    cur.execute(f'''INSERT INTO invites VALUES ('{code}','{ctx.message.author.id}',CURRENT_TIMESTAMP)''')
    con.commit()
    await user.send(f'This is a one-use invite to Requiem that will last for one hour. Please send it to the person '
                    f'you wish to invite.\r\n {await ctx.channel.create_invite(max_age=86400, max_uses=1)}\r\n\r\n'
                    f'Here is the temporary code the user will need to register on the server: **`{code}`**')


@bot.command(pass_context=True, name='verify')
async def verify(ctx, code):
    cur.execute(f"SELECT code, user_id FROM invites WHERE code=?", (code,))
    exists = cur.fetchall()
    if not exists:
        await ctx.message.author.send(f'{code} is not a valid registration code, please check with your sponsor and try'
                                      f' again.')
    else:
        sponsor = exists[0][1]
        cur.execute(f'INSERT INTO members VALUES ("{ctx.message.author.id}","{sponsor}")')
        cur.execute(f"DELETE FROM invites WHERE code=?", (code,))
        con.commit()
        await ctx.message.author.add_roles(discord.utils.get(bot.get_guild(ctx.guild.id).roles, name="Verified"))

    await ctx.message.delete()


@bot.command(pass_context=True, name='rate')
async def rate(ctx, target: discord.User):
    rater = ctx.message.author.id
    ratee = ctx.message.mentions[0].id
    cur.execute(f"SELECT rated_id FROM ratings WHERE rated_id=? AND user_id=?", (ratee, rater))
    exists = cur.fetchall()
    if not exists:
        cur.execute(f'''INSERT INTO ratings VALUES ('{ratee}','{rater}')''')
        con.commit()
        await ctx.message.author.send(f'You just positively rated {ratee}')
    else:
        await ctx.message.author.send(f'You\'ve already rated that user, or they don\'t exist in the server.')


# UTILITY FUNCTIONS
def uniquecode():
    regcode = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    cur.execute(f'''SELECT code FROM invites WHERE code="{regcode}"''')

    exists = cur.fetchall()
    if not exists:
        return regcode
    else:
        return uniquecode()


# if yes, generate new code


bot.run(TOKEN)
