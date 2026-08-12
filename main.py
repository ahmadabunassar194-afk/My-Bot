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
@bot.command(name="تحويل")
async def transfer(ctx, user_id: str, amount: int):
    # 2. تنظيف الآيدي لو المستخدم وضع منشن بالخطأ
    user_id = user_id.replace("<@", "").replace(">", "").replace("!", "")

    # 3. منع التحويل للنفس
    if user_id == str(ctx.author.id):
        await ctx.send("❌ ما تقدر تحول فلوس لنفسك يا غالي")
        return

    # 4. التحقق من أن المبلغ أكبر من صفر
    if amount <= 0:
        await ctx.send("❌ لازم تحول مبلغ أكبر من صفر!")
        return

    try:
        # تحويل الآيدي إلى رقم للتعامل مع الدالة والقاموس
        target_id = int(user_id)
        
        # 5. جلب الرصيد والتحقق منه
        author_bal = get_balance(ctx.author.id)

        if author_bal < amount:
            await ctx.send("❌ رصيدك غير كافي عشان تعمل هالتحويل")
            return

        # 6. الخصم والإضافة بالخلفية
        user_balances[ctx.author.id] -= amount
        user_balances[target_id] = user_balances.get(target_id, 0) + amount

        # 7 و 8. رسائل النجاح في الشات العام مباشرة
        await ctx.send(f"💸 تم تحويل {amount} بنجاح من {ctx.author.mention} إلى <@{target_id}>")
        await ctx.send(f"💰 نقد استلمت **{amount}** يا <@{target_id}>")

    except ValueError:
        await ctx.send("❌ يرجى إدخال آيدي مستخدم صحيح أو عمل منشن صحيح.")
    except Exception as e:
        pass


# =======================================
# 6. تشغيل السيرفر الداخلي والبوت
# =======================================
keep_alive()

TOKEN = os.getenv('DISCORD_TOKEN')
client.run(TOKEN)
