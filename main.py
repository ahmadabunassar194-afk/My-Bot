import os
import discord
from discord.ext import commands

# ==========================================
# 1. إعدادات البوت الأساسية والصلاحيات (البادئة فارغة)
# ==========================================
intents = discord.Intents.default()
intents.message_content = True
# تم إلغاء علامة التعجب وجعل البادئة فارغة تماماً
client = commands.Bot(command_prefix="", intents=intents)

# قاموس لتخزين رصيد المستخدمين
user_balances = {}

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

# ==========================================
# 2. أمر إضافة فلوس - مخصص للإدارة فقط (اضف)
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
    # عند كتابة "رصيد" يتم استدعاء أمر c تلقائياً
    await ctx.invoke(client.get_command('c'), member=member)

# ==========================================
# 5. تشغيل البوت بالتوكن المحمي
# ==========================================
TOKEN = os.getenv('DISCORD_TOKEN')
client.run(TOKEN)
