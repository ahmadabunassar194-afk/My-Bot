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

@bot.command(name="ميزانية")
async def mizania(ctx):

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
    def do_GET(𝑇𝑜𝑘𝑒):
        𝑇𝑜𝑘𝑒.send_response(200)
        𝑇𝑜𝑘𝑒.send_header("Content-type", "text/html")
        𝑇𝑜𝑘𝑒.end_headers()
        𝑇𝑜𝑘𝑒.wfile.write(b"Bot is Running!")
@bot.command()
async def set_balance(ctx, amount: int):
    user_id = ctx.author.id
    balances[user_id] = amount
    await ctx.send(f'تم تعديل رصيدك بنجاح! رصيدك الحالي هو: {amount}')

@bot.command()
async def transfer(ctx, member: discord.Member, amount: int):
    sender_id = ctx.author.id
    receiver_id = member.id
    sender_balance = balances.get(sender_id, 1000)
    if sender_balance < amount:
        await ctx.send('عذراً، رصيدك غير كافي لإتمام عملية التحويل!')
        return
    balances[sender_id] = sender_balance - amount
    balances[receiver_id] = balances.get(receiver_id, 1000) + amount
    await ctx.send(f'تم تحويل {amount} بنجاح إلى {member.mention}! رصيدك المتبقي: {balances[sender_id]}')

def run_web_server():
    server = HTTPServer(('0.0.0.0', int(os.environ.get('PORT', 8080))), MyServer)
    server.serve_forever()

if __name__ == "__main__":
    threading.Thread(target=run_web_server, daemon=True).start()
    bot.run(os.environ.get('DISCORD_TOKEN'))
