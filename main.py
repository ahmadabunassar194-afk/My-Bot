import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}")

@client.command(name="c")
async def check_balance_short(ctx):
    await ctx.send(f"رصيدك الحالي: 1000 عملة.")

@client.command(name="c")
async def check_balance_long(ctx):
    await ctx.send(f"رصيدك الحالي: 1000 عملة.")

@client.command()
async def ping(ctx):
    await ctx.send("pong!")

TOKEN = os.getenv('DISCORD_TOKEN')
client.run(TOKEN)
