import subprocess

import discord
from discord.ext import commands
from discord import app_commands



class Minecraft(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @app_commands.command(name="ligar",description="Ligar servidor")
    async def ligar(self, interaction: discord.Interaction):
        result = subprocess.run(["docker","start","minecraft"],capture_output=True, text=True)
        if result.returncode == 0:
            await interaction.response.send_message("Servidor ligado",ephemeral=True)
        else:
            await interaction.response.send_message(f"Erro ao iniciar: {result.stderr}", ephemeral=True) 
    @app_commands.command(name="desligar",description="Desligar servidor")
    async def desligar (self, interaction: discord.Interaction):
        result = subprocess.run(["docker","stop","minecraft"],capture_output=True, text=True)
        if result.returncode == 0:
            await interaction.response.send_message("Servidor desligado",ephemeral=True)
        else:
            await interaction.response.send_message(f"Erro ao iniciar: {result.stderr}", ephemeral=True)

async def setup(bot):  
    await bot.add_cog(Minecraft(bot))
