import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot acceso come {bot.user} 🟢")
    print("PRESENZA EAGLES ATTIVA 🦅")
    await bot.change_presence(activity=discord.Game(name="🦅 EAGLES | !presenza"))

@bot.command()
async def ciao(ctx):
    await ctx.send(f"Ciao {ctx.author.mention}! 🦅 Forza EAGLES!")

@bot.command()
async def presenza(ctx):
    online = 0
    total = 0
    lista = ""
    for member in ctx.guild.members:
        if not member.bot:
            total += 1
            if str(member.status) != "offline":
                online += 1
                lista += f"🟢 {member.display_name}\n"
    
    await ctx.send(f"**🦅 PRESENZA EAGLES**\n\nOnline: **{online}/{total}**\n\n{lista}")

@bot.command()
async def eagles(ctx):
    await ctx.send("🦅🦅🦅 FORZA EAGLES! 🦅🦅🦅")

TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)
