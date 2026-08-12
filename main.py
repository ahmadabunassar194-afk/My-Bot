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
client = commands.Bot(command_prefix="c", intents=intents)

# قاموس لتخزين رصيد المستخدمين
user_balances = {}

@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}")

# دالة مساعدة عشان تعطي رصيد مبدئي لأي عضو جديد
def get_balance(user_id):
    if user_id not in user_balances:
        user_balances[user_id] = 1000
    return user_balances[user_id]

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
    get_balance(user_id) # للتأكد إنه معرف في القاموس
        
    user_balances[user_id] += amount
    await ctx.send(f"💰 تم إضافة {amount} لحساب {member.mention}")

@add_money.error
async def add_money_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ الأمر مخصص للإدارة فقط!")

# =======================================
# 4. أوامر الرصيد (يشتغل بـ cc أو cرصيد)
# =======================================
@client.command(name="c")
async def check_balance_c(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
        
    balance = get_balance(member.id)
    await ctx.send(f"💳 رصيد {member.mention}: {balance} عملة.")

@client.command(name="رصيد")
async def check_balance_arabic(ctx, member: discord.Member = None):
    await ctx.invoke(client.get_command('c'), member=member)

# =======================================
# 5. أمر تحويل الفلوس (ومراسلة المستلم في الخاص)
# الاستخدام: ctransfer @الشخص المبلغ
# =======================================
@client.command(name="transfer")
async def transfer_money(ctx, member: discord.Member = None, amount: int = None):
    # 1. فحص المدخلات
    if member is None or amount is None:
        await ctx.send("❌ **الاستخدام الصحيح:**\n`ctransfer @الشخص المبلغ`")
        return

    # 2. منع الشخص يحول لنفسه
    if member.id == ctx.author.id:
        await ctx.send("❌ **يا غالي ما بتقدر تحول فلوس لنفسك!**")
        return

    # 3. فحص إن المبلغ أكبر من صفر
    if amount <= 0:
        await ctx.send("❌ **لازم تحدد مبلغ أكبر من صفر يا ورد.**")
        return

    author_id = ctx.author.id
    member_id = member.id

    if author_id not in user_balances:
        user_balances[author_id] = 0
    if member_id not in user_balances:
        user_balances[member_id] = 0

    # 4. فحص إذا الرصيد بيكفي
    if user_balances[author_id] < amount:
        await ctx.send(f"❌ **رصيدك ما بيكفي!** رصيدك الحالي هو: {user_balances[author_id]}")
        return

    # 5. عملية الخصم والإضافة
    user_balances[author_id] -= amount
    user_balances[member_id] += amount

    # 6. رسالة الشات العام (تأكيد التحويل)
    await ctx.send(f"✅ **تم التحويل بنجاح!**\nالمبلغ: `{amount}` من: {ctx.author.mention} إلى: {member.mention}")

    # 7. إرسال الخاص للمحوِّل (الشخص اللي كتب الأمر)
    try:
        await ctx.author.send(f"💸 **تأكيد عملية الحوالة:**\nتم تحويل مبلغ `{amount}` بنجاح من حسابك إلى حساب {member.name}.")
    except discord.Forbidden:
        pass

    # 8. إرسال الخاص للمستلم
    try:
        await member.send(f"💰 **وصلتك حوالة مالية!**\nلقد استلمت مبلغ `{amount}` من {ctx.author.name}!")
    except discord.Forbidden:
        await ctx.send(f"⚠️ {member.mention}، الحوالة وصلتك بس ما قدرت أرسلك خاص لأنك مقفله!")




# =======================================
# 6. تشغيل السيرفر الداخلي والبوت
# =======================================
keep_alive()

TOKEN = os.getenv('DISCORD_TOKEN')
client.run(TOKEN)
