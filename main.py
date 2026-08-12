import os
import discord
from discord.ext import commands
from threading import Thread
from flask import Flask

# =======================================
# 1. نظام الـ Keep Alive عشان الاستضافة
# =======================================
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running successfully!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# =======================================
# 2. إعدادات البوت الأساسية والصلاحيات
# =======================================
intents = discord.Intents.default()
intents.message_content = True
# رجعنا البادئة لـ c عشان يشتغل بـ cc
client = commands.Bot(command_prefix="c", intents=intents)

# قاموس لتخزين رصيد المستخدمين
user_balances = {}

@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}")

# =======================================
# 3. أمر إضافة فلوس (مخصص للإدارة فقط)
# الاستخدام: cadd @الشخص المبلغ
# =======================================
@client.command(name="add")
@commands.has_permissions(administrator=True)
async def add_money(ctx, member: discord.Member = None, amount: int = None):
    if member is None or amount is None:
        await ctx.send("❌ الاستخدام: cadd @الشخص المبلغ")
        return
        
    user_id = member.id
    if user_id not in user_balances:
        user_balances[user_id] = 1000
        
    user_balances[user_id] += amount
    await ctx.send(f"💰 تم إضافة {amount} لحساب {member.mention}")

@add_money.error
async def add_money_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ الأمر مخصص للإدارة فقط!")

# =======================================
# 4. أوامر الرصيد (الآن يشتغل بـ cc أو cرصيد)
# =======================================
@client.command(name="c")
async def check_balance_c(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
        
    user_id = member.id
    if user_id not in user_balances:
        user_balances[user_id] = 1000 # رصيد ابتدائي لأول مرة
        
    balance = user_balances[user_id]
    await ctx.send(f"💳 رصيد {member.mention}: {balance} عملة.")

@client.command(name="رصيد")
async def check_balance_arabic(ctx, member: discord.Member = None):
    await ctx.invoke(client.get_command('c'), member=member)

# =======================================
# 5. تشغيل السيرفر الداخلي والبوت
# =======================================
keep_alive()

TOKEN = os.getenv('DISCORD_TOKEN')
client.run(TOKEN)
