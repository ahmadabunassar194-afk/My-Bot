from flask import Flask
from threading import Thread
import os
import discord
from discord.ext import commands

# =========================================================
# 1. نظام الـ keep_alive لتخطي فحص البورتات في Render
# =========================================================
app = Flask('')

@app.route('/')
def home():
    return "البوت شغال 24 ساعة تمام!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# تشغيل السيرفر الوهمي بالخلفية
keep_alive()

# =========================================================
# 2. إعدادات البوت والـ Intents الأساسية
# =========================================================
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)

# قاموس حفظ أرصدة المستخدمين
user_balances = {}

@client.event
async def on_ready():
    print(f'تم تشغيل البوت بنجاح باسم: {client.user.name}')

# =========================================================
# 3. أمر إضافة رصيد (للإدارة فقط)
# =========================================================
@client.command(name="اضف")
@commands.has_permissions(administrator=True)
async def add_money(ctx, member: discord.Member = None, amount: int = None):
    if member is None or amount is None:
        await ctx.send("❌ طريقة الاستخدام الصحيحة: !اضف @الشخص المبلغ")
        return
        
    user_id = member.id
    if user_id not in user_balances:
        user_balances[user_id] = 1000  # الرصيد الافتراضي البدائي
        
    user_balances[user_id] += amount
    await ctx.send(f"💰 تم إضافة {amount} لحساب {member.mention}")

@add_money.error
async def add_money_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ هاد الأمر مخصص للإدارة فقط!")

# =========================================================
# 4. أمر معرفة الرصيد (أمر c أو رصيد)
# =========================================================
@client.command(name="c")
async def check_balance_c(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author  # إذا لم يحدد شخص، يعرض رصيد صاحب الأمر
        
    user_id = member.id
    if user_id not in user_balances:
        user_balances[user_id] = 1000  # رصيد بدائي إذا كان أول مرة
        
    balance = user_balances[user_id]
    await ctx.send(f"💳 رصيد {member.mention} الحالي هو: **{balance}**")

@client.command(name="رصيد")
async def check_balance_arabic(ctx, member: discord.Member = None):
    # تشغيل نفس الأمر عند كتابة "رصيد" بالعربي لراحة المستخدمين
    await ctx.invoke(client.get_command('c'), member=member)

# =========================================================
# 5. تشغيل البوت بالتوكن المحمي
# =========================================================
TOKEN = os.getenv('DISCORD_TOKEN')
client.run(TOKEN)
