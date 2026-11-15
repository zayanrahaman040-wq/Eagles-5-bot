import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Qui salviamo chi preme il bottone
presenti = set()
presenza_attiva = False

class BottonePresenza(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="✅ Sono Presente", style=discord.ButtonStyle.success, custom_id="bottone_presenza")
    async def presente(self, interaction: discord.Interaction, button: discord.ui.Button):
        global presenti, presenza_attiva
        if not presenza_attiva:
            await interaction.response.send_message("❌ Presenza chiusa!", ephemeral=True)
            return
        
        if interaction.user.id in presenti:
            await interaction.response.send_message("Hai già messo presenza! 🦅", ephemeral=True)
        else:
            presenti.add(interaction.user.id)
            await interaction.response.send_message(f"{interaction.user.mention} registrato! 🦅✅", ephemeral=True)

@bot.event
async def on_ready():
    print(f"Bot acceso come {bot.user} 🟢")
    bot.add_view(BottonePresenza())
    await bot.change_presence(activity=discord.Game(name="🦅 EAGLES | !presenza"))

@bot.command()
async def presenza(ctx):
    global presenti, presenza_attiva
    presenti = set()
    presenza_attiva = True
    view = BottonePresenza()
    await ctx.send("🦅 **PRESENZA EAGLES - PREMI IL BOTTONE!** 🦅\n\nPremi ✅ sotto per segnare la presenza!", view=view)

@bot.command()
async def stop(ctx):
    global presenza_attiva
    presenza_attiva = False
    if not presenti:
        await ctx.send("❌ **PRESENZA DISATTIVATA**\n\nNessuno ha partecipato 😢")
        return

    lista = ""
    for user_id in presenti:
        membro = ctx.guild.get_member(user_id)
        if membro:
            lista += f"✅ {membro.display_name}\n"

    await ctx.send(f"❌ **PRESENZA DISATTIVATA**\n\n🦅 **CHI HA PARTECIPATO ({len(presenti)}):**\n\n{lista}")

@bot.command()
async def lista(ctx):
    if not presenti:
        await ctx.send("Nessuno ha ancora premuto! 😢")
        return
    lista = ""
    for user_id in presenti:
        membro = ctx.guild.get_member(user_id)
        if membro:
            lista += f"✅ {membro.display_name}\n"
    await ctx.send(f"🦅 **PRESENTI ORA ({len(presenti)}):**\n\n{lista}")

TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)
