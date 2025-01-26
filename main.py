import os

import discord
import dotenv
from discord import app_commands
from discord.ext import commands

dotenv.load_dotenv()


permissoes = discord.Intents.default()
permissoes.message_content = True
permissoes.members = True
permissoes.voice_states = True
permissoes.guilds = True
bot = commands.Bot(command_prefix=".", intents=permissoes)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


async def loadCogs():
    cogs_path = os.path.join(BASE_DIR, "cogs")
    for arquivos in os.listdir(cogs_path):
        if arquivos.endswith(".py"):
            await bot.load_extension(f"cogs.{arquivos[:-3]}")


@bot.event
async def on_ready():
    print(os.getcwd())
    await loadCogs()
    print("estou conectado")


@bot.command()
async def Sync(ctx: commands.Context):
    if ctx.author.id == os.getenv("AUTHOR"):
        syncs = await bot.tree.sync()
        print("comandos syncs")
        await ctx.reply(f"comandos atualizados {syncs}")
    else:
        await ctx.reply("somente meu dono pode atualizar")


bot.run(os.getenv("TOKEN"))
