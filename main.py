import os
import discord
from discord.ext import commands
from threading import Thread
from flask import Flask

# إنشاء سيرفر وهمي لتخطي نظام الفحص في Render
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run_flask():
    # Render يمرر رقم المنفذ تلقائياً عبر PORT
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix="", intents=intents)

user_balances = {}

def get_balance(user_id):
    if user_id not in user_balances:
        user_balances[user_id] = 1000
    return user_balances[user_id]

@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}")

@client.command(name="c")
async def check_balance(ctx):
    balance = get_balance(ctx.author.id)
    await ctx.send(f"رصيدك الحالي: {balance} عملة.")

@client.command(name="تحويل")
async def transfer_money(ctx, member: discord.Member = None, amount: int = None):
    if member is None or amount is None or amount <= 0:
        await ctx.send("❌ الاستخدام الصحيح للأمر: تحويل @اسم_الشخص المبلغ")
        return

    sender_id = ctx.author.id
    receiver_id = member.id

    if sender_id == receiver_id:
        await ctx.send("❌ لا يمكنك التحويل لنفسك!")
        return

    sender_balance = get_balance(sender_id)

    if sender_balance < amount:
        await ctx.send("❌ رصيدك الحالي لا يكفي لإتمام هذه العملية.")
        return

    user_balances[sender_id] -= amount
    if receiver_id not in user_balances:
        user_balances[receiver_id] = 1000
    user_balances[receiver_id] += amount

    await ctx.send(f"✅ تم تحويل {amount} عملة بنجاح إلى {member.mention}.")

    try:
        await member.send(f"تم ارسل 𝑇𝑜𝑘𝑒\nوصلتك حوالة بمبلغ: {amount} عملة من {ctx.author.name}")
    except discord.Forbidden:
        await ctx.send(f"⚠️ {member.mention} لقد تم التحويل، ولكن لم أتمكن من إرسال رسالة خاصة لك لأن حسابك مغلق للخاص.")

@client.command(name="اضف")
@commands.has_permissions(administrator=True)
async def add_money(ctx, member: discord.Member = None, amount: int = None):
    if member is None or amount is None or amount <= 0:
        await ctx.send("❌ الاستخدام الصحيح للأمر: اضف @الشخص المبلغ")
        return

    user_id = member.id
    if user_id not in user_balances:
        user_balances[user_id] = 1000
        
    user_balances[user_id] += amount
    await ctx.send(f"💰 تم إضافة {amount} عملة إلى حساب {member.mention} بنجاح!")

@add_money.error
async def add_money_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ عذراً، هذا الأمر مخصص للإدارة فقط!")

# تشغيل السيرفر الوهمي قبل تشغيل البوت
keep_alive()

TOKEN = os.getenv('DISCORD_TOKEN')
client.run(TOKEN)

gunicorn main:app
