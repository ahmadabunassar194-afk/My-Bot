import os
import discord
from discord.ext import commands
from threading import Thread
from flask import Flask

# ==========================================
# 1. نظام الـ Keep Alive عشان البوت ما يطفي على Render
# ==========================================
app = Flask('')

@app.route('/')
def home():
    return "البوت شغال تمام وبدون مشاكل!"

def run():
    # Render بيطلب تحديد المنفذ تلقائياً أو بيعطيك 8080
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# تشغيل السيرفر الداخلي
keep_alive()

# ==========================================
# 2. إعدادات البوت الأساسية والصلاحيات (البادئة فارغة)
# ==========================================
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="", intents=intents)

# قاموس لتخزين رصيد المستخدمين
user_balances = {}

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

# ==========================================
# 3. أمر إضافة فلوس - مخصص للإدارة فقط (اضف)
# ==========================================
@client.command(name="اضف")
@commands.has_permissions(administrator=True)
async def add_money(ctx, member: discord.Member = None, amount: int = None):
    if member is None or amount is None:
        await ctx.send("❌ الاستخدام: (اضف @الشخص المبلغ)")
        return

    user_id = member.id
    
    if user_id not in user_balances:
        user_balances[user_id] = 1000

    user_balances[user_id] += amount
    await ctx.send(f"💰 تم إضافة {amount} لحساب {member.mention}")

@add_money.error
async def add_money_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ الأمر مخصص للإدارة فقط")

# ==========================================
# 4. أمر رصيد c (بدون علامة تعجب)
# ==========================================
@client.command(name="c")
async def check_balance_c(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author  # إذا لم يتم تحديد شخص، يعرض رصيد صاحب الأمر

    user_id = member.id
    if user_id not in user_balances:
        user_balances[user_id] = 1000  # رصيد ابتدائي لأول مرة

    balance = user_balances[user_id]
    await ctx.send(f"💳 رصيد {member.mention}: {balance} عملة.")

# أمر رصيد بالعربي (بدون علامة تعجب)
@client.command(name="رصيد")
async def check_balance_arabic(ctx, member: discord.Member = None):
    await ctx.invoke(client.get_command('c'), member=member)
@client.command(name="c")
async def transfer_c(ctx, member: discord.Member, amount: int):
    # التأكد من أن المستخدم لا يحول لنفسه
    if ctx.author.id == member.id:
        await ctx.send("❌ لا يمكنك تحويل الأموال لنفسك.")
        return

    # التأكد من أن المبلغ المدخل أكبر من صفر
    if amount <= 0:
        await ctx.send("❌ يرجى إدخال مبلغ صحيح أكبر من الصفر.")
        return

    author_id = ctx.author.id
    target_id = member.id

    # التأكد من وجود حساب للمرسل وتوفر الرصيد
    if author_id not in user_balances or user_balances[author_id] < amount:
        await ctx.send("❌ ليس لديك رصيد كافٍ لإتمام هذه العملية.")
        return

    # التأكد من وجود حساب للمستلم في قاعدة البيانات
    if target_id not in user_balances:
        user_balances[target_id] = 1000  # الرصيد الافتراضي للاعب الجديد

    # خصم المبلغ من المرسل وإضافته للمستلم
    user_balances[author_id] -= amount
    user_balances[target_id] += amount

    # إرسال رسالة تأكيد في السيرفر
    await ctx.send(f"✅ تم تحويل **{amount}$** بنجاح إلى {member.mention}.")

    # إرسال رسالة خاصة للمستلم في الخاص (DM)
    try:
        await member.send(f"💰 وصلتك حوالة مالية بقيمة **{amount}$** من {ctx.author.mention} في سيرفر **{ctx.guild.name}**.")
    except discord.Forbidden:
        # إذا كان خاص المستلم مغلقاً
        await ctx.send(f"⚠️ {member.mention} لقد أرسلت لك مبلغاً، لكن خاصك مغلق!")


# ==========================================
# 5. تشغيل البوت بالتوكن المحمي
# ==========================================
TOKEN = os.getenv('DISCORD_TOKEN')
client.run(TOKEN)
