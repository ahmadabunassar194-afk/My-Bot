import discord
from discord.ext import commands
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

intents = discord.Intents.default()
intents.message_content = True
intents.members = True          # ضفنا هاي عشان المنشن بالتحويل يشتغل صح
bot = commands.Bot(command_prefix='', intents=intents)

balances = {}

@bot.event
async def on_ready():
    print(f'Bot is ready: {bot.user}')

# 1. أمر الرصيد وصار يبعت على الخاص علطول
@bot.command(name="c")
async def mizania(ctx):
    user_id = ctx.author.id
    balance = balances.get(user_id, 1000)
    balances[user_id] = balance
    await ctx.author.send(f'رصيدك الحالي: {balance} عملة.')

class MyServer(BaseHTTPRequestHandler):
    def do_GET(Toke):
        Toke.send_response(200)
        Toke.send_header("Content-type", "text/html")
        Toke.end_headers()
        Toke.wfile.write(b"Bot is Running!")

@bot.command()
async def set_balance(ctx, amount: int):
    user_id = ctx.author.id
    balances[user_id] = amount
    await ctx.send(f'تم تعديل رصيدك بنجاح! رصيدك الحالي هو {amount}')

# 2. أمر التحويل شغال بدون علامة تعجب (تكتب تالي: t @منشن 50)
@bot.command(name="t")
async def transfer(ctx, member: discord.Member, amount: int):
    sender_id = ctx.author.id
    receiver_id = member.id
    
    if amount <= 0:
        await ctx.send("المبلغ لازم يكون أكبر من صفر! ❌")
        return
        
    sender_balance = balances.get(sender_id, 1000)
    
    if sender_balance < amount:
        await ctx.send("رصيدك مش كافي للتحويل! ❌")
    else:
        balances[sender_id] = sender_balance - amount
        balances[receiver_id] = balances.get(receiver_id, 1000) + amount
        await ctx.send(f'تم تحويل {amount} عملة إلى {member.mention} بنجاح! 🎉')

# 3. أمر سري عشان أنت تعطي عملات (تكتب تالي: give @منشن 500)
@bot.command(name="give")
async def give_money(ctx, member: discord.Member, amount: int):
    # !!! حط الآيدي تبع حسابك بالديسكورد بدل الأرقام اللي تحت عشان ما حدا يسرق الأمر !!!
    if ctx.author.id == 123456789012345678: 
        user_id = member.id
        balances[user_id] = balances.get(user_id, 1000) + amount
        await ctx.send(f'تم إضافة {amount} عملة لحساب {member.mention} بنجاح! 💰')
    else:
        await ctx.send('ما عندك صلاحية يا غالي! ❌')
