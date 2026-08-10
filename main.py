import discord
from discord.ext import commands
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

balances = {}

@bot.event
async def on_ready():
    print(f'Bot is ready: {bot.user}')

@bot.command()
async def ميزانية(ctx):
    user_id = ctx.author.id
    balance = balances.get(user_id, 1000)
    balances[user_id] = balance
    await ctx.send(f'رصيدك الحالي: {balance} عملة.')
@bot.command()
async def set_balance(ctx, amount: int):
    user_id = ctx.author.id
    balances[user_id] = amount
    await ctx.send(f'تم تعديل رصيدك بنجاح! رصيدك الحالي هو: {amount}')

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Bot is Running!")

def run_web_server():
    server = HTTPServer(('0.0.0.0', int(os.environ.get('PORT', 8080))), MyServer)
    server.serve_forever()

if __name__ == "__main__":
    threading.Thread(target=run_web_server, daemon=True).start()
    bot.run(os.environ.get('DISCORD_TOKEN'))
