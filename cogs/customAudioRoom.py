import os

import discord
import dotenv
from discord import app_commands
from discord.ext import commands

dotenv.load_dotenv()


def check_editable(name, prefix, user_name):
    if name.startswith(prefix):
        return True
    if name == f"Canal de {user_name}":
        return True
    return False


class CustomAudioRoom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.category_id = int(os.getenv("VOICE_CATEGORY_ID"))
        self.prefix = "🎧"

    @app_commands.command(name="criar_sala", description="Cria uma sala de voz")
    async def criar_sala(self, interaction: discord.Interaction, nome: str):
        guild = interaction.guild
        category = discord.utils.get(guild.categories, id=self.category_id)

        if not category:
            await interaction.response.send_message(
                "Categoria de voz não encontrada.", ephemeral=True
            )
            return

        try:
            voice_channel = await guild.create_voice_channel(
                name=f"{self.prefix}-{nome}", category=category
            )
            await interaction.response.send_message(
                f"Sala de voz criada: {voice_channel.mention}", ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"Erro ao criar a sala de voz: {str(e)}", ephemeral=True
            )

    @app_commands.command(name="deletar_sala", description="Deleta uma sala de voz")
    async def deletar_sala(
        self, interaction: discord.Interaction, sala: discord.VoiceChannel
    ):
        if not check_editable(sala.name, self.prefix, interaction.user.name):
            await interaction.response.send_message(
                "Sala de voz nao pode ser deletada.", ephemeral=True
            )
            return

        name = sala.name
        try:
            await sala.delete()
            await interaction.response.send_message(
                f"Sala de voz deletada: {name}", ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"Erro ao deletar a sala de voz: {str(e)}", ephemeral=True
            )

    @app_commands.command(name="editar_sala", description="Edita uma sala de voz")
    async def editar_sala(
        self,
        interaction: discord.Interaction,
        sala: discord.VoiceChannel,
        nome: str = None,
        limite_usuarios: int = None,
        privada: bool = None,
        usuarios: str = None,  # Agora aceita uma string com nomes de usuários
    ):
        if not check_editable(sala.name, self.prefix, interaction.user.name):
            await interaction.response.send_message(
                "Sala de voz nao pode ser editada.", ephemeral=True
            )
            return
        try:
            # Atualiza o nome da sala
            if nome:
                await sala.edit(name=f"{self.prefix}-{nome}")

            # Atualiza o limite de usuários
            if limite_usuarios is not None:
                await sala.edit(user_limit=limite_usuarios)

            # Lógica para tornar a sala privada e definir permissões
            if privada is not None:
                overwrites = {
                    interaction.guild.default_role: discord.PermissionOverwrite(
                        connect=False
                    ),
                    interaction.user: discord.PermissionOverwrite(connect=True),
                }

                # Se a sala for privada, só o dono (usuário) e os selecionados podem entrar
                if privada and usuarios:
                    usuarios_nomes = [nome.strip() for nome in usuarios.split(",")]
                    for nome_usuario in usuarios_nomes:
                        # Tenta encontrar o membro no servidor com base no nome
                        user = discord.utils.get(
                            interaction.guild.members, name=nome_usuario
                        )
                        if user:
                            overwrites[user] = discord.PermissionOverwrite(connect=True)
                        else:
                            await interaction.response.send_message(
                                f"Usuário {nome_usuario} não encontrado.",
                                ephemeral=True,
                            )
                            return
                else:
                    # Se não for privada, todos podem entrar
                    overwrites[interaction.guild.default_role] = (
                        discord.PermissionOverwrite(connect=True)
                    )

                # Atualiza as permissões
                await sala.edit(overwrites=overwrites)

            # Envia uma mensagem de confirmação
            await interaction.response.send_message(
                f"Sala de voz {sala.name} foi atualizada.", ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"Erro ao editar a sala de voz: {str(e)}", ephemeral=True
            )


async def setup(bot):
    await bot.add_cog(CustomAudioRoom(bot))
