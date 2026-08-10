import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix="", intents=intents)

# قاعدة بيانات وهمية لتجربة الأوامر برصيد مبدئي 1000 عملة لكل مستخدم
user_balances = {}

def get_balance(user_id):
    if user_id not in user_balances:
        user_balances[user_id] = 1000
    return user_balances[user_id]

@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}")

@client.command(name="c")
async def check_balance_short(ctx):
    balance = get_balance(ctx.author.id)
    await ctx.send(f"رصيدك الحالي: {balance} عملة.")

@client.command(name="c")
async def check_balance_long(ctx):
    balance = get_balance(ctx.author.id)
    await ctx.send(f"رصيدك الحالي: {balance} عملة.")

@client.command(name="تحويل")
async def transfer_money(ctx, member: discord.Member = None, amount: int = None):
    # التأكد من كتابة الأمر بشكل صحيح
    if member is None or amount is None or amount <= 0:
        await ctx.send("❌ الاستخدام الصحيح للأمر: !تحويل @اسم_الشخص المبلغ")
        return

    sender_id = ctx.author.id
    receiver_id = member.id

    # منع الشخص من التحويل لنفسه
    if sender_id == receiver_id:
        await ctx.send("❌ لا يمكنك التحويل لنفسك!")
        return

    sender_balance = get_balance(sender_id)

    # التأكد من توفر الرصيد الكافي
    if sender_balance < amount:
        await ctx.send("❌ رصيدك الحالي لا يكفي لإتمام هذه العملية.")
        return

    # الخصم والإضافة من وإلى الأرصدة
    user_balances[sender_id] -= amount
    if receiver_id not in user_balances:
        user_balances[receiver_id] = 1000
    user_balances[receiver_id] += amount

    # إرسال الرسالة العامة في الشات الأساسي
    await ctx.send(f"✅ تم تحويل {amount} عملة بنجاح إلى {member.mention}.")

    # إرسال الرسالة الخاصة للشخص المحول له
    try:
        await member.send(f"تم ارسل 𝑇𝑜𝑘𝑒\nوصلتك حوالة بمبلغ: {amount} عملة من {ctx.author.name}")
    except discord.Forbidden:
        # في حال كان الشخص مغلقاً للرسائل الخاصة من الغرباء
        await ctx.send(f"⚠️ {member.mention} لقد تم التحويل، ولكن لم أتمكن من إرسال رسالة خاصة لك لأن حسابك مغلق للخاص.")

TOKEN = os.getenv('DISCORD_TOKEN')
client.run(TOKEN)
