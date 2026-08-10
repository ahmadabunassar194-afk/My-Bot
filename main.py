import discord
from discord.ext import commands
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

intents = discord.Intents.default()
intents.message_content = True
intents.members = True          
bot = commands.Bot(command_prefix='', intents=intents)

balances = {}

@bot.event
async def on_ready():
    print(f'Bot is ready: {bot.user}')

@bot.command(name="c")
async def mizania(ctx):
    user_id = ctx.author.id
    balance = balances.get(user_id, 1000)
    balances[user_id] = balance
    await ctx.author.send(f'رصيدك الحالي: {balance} عملة.')

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Bot is Running!")

def run_server():
    port = int(os.environ.get('PORT', 8080))
    server = HTTPServer(('0.0.0.0', port), MyServer)
    server.serve_forever()

# تشغيل السيرفر بالخلفية عشان ريندر ما يطفي البوت
threading.Thread(target=run_server, daemon=True).start()

@bot.command()
async def set_balance(ctx, amount: int):
    user_id = ctx.author.id
    balances[user_id] = amount
    await ctx.send(f'تم تعديل رصيدك بنجاح! رصيدك الحالي هو {amount}')

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

@bot.command(name="give")
async def give_money(ctx, member: discord.Member, amount: int):
    # حط الآيدي تبع حسابك بالديسكورد بدل الأرقام اللي تحت
    if ctx.author.id == 123456789012345678: 
        user_id = member.id
        balances[user_id] = balances.get(user_id, 1000) + amount
        await ctx.send(f'تم إضافة {amount} عملة لحساب {member.mention} بنجاح! 💰')
    else:
        await ctx.send('ما عندك صلاحية يا غالي! ❌')

# ⚠️ السطر هاد هو الأهم وهو اللي كان ناقص وبشغل البوت 24 ساعة
# حط التوكن تبع البوت تبعك مكان كلمة YOUR_BOT_TOKEN_HERE
bot.run('70a8582c0aada46ef125adebca1fc69d4716e5bbb9e5364e63e3e9fcbc21f8e0')

