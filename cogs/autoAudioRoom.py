import os

import discord
import dotenv
from discord import app_commands
from discord.ext import commands

dotenv.load_dotenv()


class AudioRoom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @commands.Cog.listener("on_voice_state_update")
    async def on_voice_state_update(self, member, before, after):
        entrada_canal_id = int(os.getenv("LOBBY_AUTO_ROOM"))
        guild = member.guild

        # Checa se o usuário entrou no canal específico
        if after.channel and after.channel.id == entrada_canal_id:
            # Cria um novo canal de voz com o nome do usuário
            novo_canal = await guild.create_voice_channel(
                name=f"Canal de {member.display_name}",
                overwrites={
                    guild.default_role: discord.PermissionOverwrite(view_channel=True),
                    member: discord.PermissionOverwrite(
                        view_channel=True, connect=True, manage_permissions=True
                    ),
                },
                category=after.channel.category,
            )
            await member.move_to(novo_canal)  # Move o usuário para o novo canal

            # Aguarda o usuário sair do canal
            def check_voice_state(mem, bef, aft):
                return (
                    mem == member
                    and bef.channel == novo_canal
                    and aft.channel != novo_canal
                )

            await self.bot.wait_for("voice_state_update", check=check_voice_state)
            await novo_canal.delete()


async def setup(bot):
    await bot.add_cog(AudioRoom(bot))
