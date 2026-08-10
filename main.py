import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}")

@client.command()
async def ping(ctx):
    await ctx.send("pong!")

TOKEN = os.getenv('DISCORD_TOKEN')
client.run(TOKEN)
