import discord
from discord.ext import commands
from discord import app_commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)

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
    try:
        synced = await bot.tree.sync()
        print(f"Comandi / sincronizzati: {len(synced)}")
    except Exception as e:
        print(f"Errore sync: {e}")
    await bot.change_presence(activity=discord.Game(name="🦅 EAGLES | /presenza"))

@bot.tree.command(name="ciao", description="Saluta gli Eagles")
async def ciao(interaction: discord.Interaction):
    await interaction.response.send_message(f"Ciao {interaction.user.mention}! 🦅 Forza EAGLES!")

@bot.tree.command(name="eagles", description="Forza Eagles")
async def eagles(interaction: discord.Interaction):
    await interaction.response.send_message("🦅🦅🦅 FORZA EAGLES! 🦅🦅🦅")

@bot.tree.command(name="presenza", description="Avvia la presenza con bottone")
async def presenza(interaction: discord.Interaction):
    global presenti, presenza_attiva
    presenti = set()
    presenza_attiva = True
    view = BottonePresenza()
    await interaction.response.send_message("🦅 **PRESENZA EAGLES - PREMI IL BOTTONE!** 🦅\n\nPremi ✅ sotto per segnare la presenza!", view=view)

@bot.tree.command(name="lista", description="Vedi chi ha messo presenza")
async def lista(interaction: discord.Interaction):
    if not presenti:
        await interaction.response.send_message("Nessuno ha ancora premuto! 😢")
        return
    lista_txt = ""
    for user_id in presenti:
        membro = interaction.guild.get_member(user_id)
        if membro:
            lista_txt += f"✅ {membro.display_name}\n"
    await interaction.response.send_message(f"🦅 **PRESENTI ORA ({len(presenti)}):**\n\n{lista_txt}")

@bot.tree.command(name="stop", description="Chiudi la presenza e mostra chi ha partecipato")
async def stop(interaction: discord.Interaction):
    global presenza_attiva
    presenza_attiva = False
    if not presenti:
        await interaction.response.send_message("❌ **PRESENZA DISATTIVATA**\n\nNessuno ha partecipato 😢")
        return
    lista_txt = ""
    for user_id in presenti:
        membro = interaction.guild.get_member(user_id)
        if membro:
            lista_txt += f"✅ {membro.display_name}\n"
    await interaction.response.send_message(f"❌ **PRESENZA DISATTIVATA**\n\n🦅 **CHI HA PARTECIPATO ({len(presenti)}):**\n\n{lista_txt}")

TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)
