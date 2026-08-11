from flask import Flask
from threading import Thread
import os
import discord
from discord.ext import commands

# 1. تشغيل السيرفر الوهمي لتخطي نظام الفحص في Render
app = Flask('')

@app.route('/')
def home():
    return "البوت شغال تمام!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

# 2. كود البوت الأساسي تبعك
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

@client.command(name="اضف")
@commands.has_permissions(administrator=True)
async def add_money(ctx, member: discord.Member = None, amount: int = None):
    if member is None or amount is None:
        await ctx.send("❌ اضف @الشخص المبلغ")
        return
        
    user_id = member.id
    # هنا يفترض وجود قاموس الـ user_balances معرّف بكودك، يمكنك تعديله لاحقاً
    if 'user_balances' not in globals():
        global user_balances
        user_balances = {}
        
    if user_id not in user_balances:
        user_balances[user_id] = 1000
        
    user_balances[user_id] += amount
    await ctx.send(f"💰 تم إضافة {amount} لحساب {member.mention}")

@add_money.error
async def add_money_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ الأمر مخصص للإدارة فقط")

# 3. تشغيل البوت باستخدام التوكن من متغيرات البيئة
TOKEN = os.getenv('DISCORD_TOKEN')
client.run(TOKEN)
