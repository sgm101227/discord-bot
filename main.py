import discord
from discord import app_commands
import random
import os

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

data = {}  # {주제: [목록들]}

@tree.command(name="주제추가", description="주제를 추가합니다")
async def 주제추가(interaction: discord.Interaction, 주제: str):
    if 주제 in data:
        await interaction.response.send_message("이미 있는 주제입니다", ephemeral=True)
    else:
        data[주제] = []
        await interaction.response.send_message(f"주제 '{주제}' 추가됨")

@tree.command(name="주제제거", description="주제를 제거합니다")
async def 주제제거(interaction: discord.Interaction, 주제: str):
    if 주제 not in data:
        await interaction.response.send_message("없는 주제야", ephemeral=True)
    else:
        del data[주제]
        await interaction.response.send_message(f"주제 '{주제}' 제거됨")

@tree.command(name="목록추가", description="주제에 목록을 추가합니다")
async def 목록추가(interaction: discord.Interaction, 주제: str, 목록: str):
    if 주제 not in data:
        await interaction.response.send_message("주제가 없어", ephemeral=True)
    else:
        data[주제].append(목록)
        await interaction.response.send_message(f"'{목록}' 추가됨")

@tree.command(name="목록제거", description="주제의 목록을 제거합니다")
async def 목록제거(interaction: discord.Interaction, 주제: str, 목록: str):
    if 주제 not in data or 목록 not in data[주제]:
        await interaction.response.send_message("없어", ephemeral=True)
    else:
        data[주제].remove(목록)
        await interaction.response.send_message(f"'{목록}' 제거됨")

@tree.command(name="주제보기", description="주제 목록을 봅니다")
async def 주제보기(interaction: discord.Interaction):
    if not data:
        await interaction.response.send_message("주제가 없습니다")
    else:
        await interaction.response.send_message(", ".join(data.keys()))

@tree.command(name="목록보기", description="주제의 목록을 봅니다")
async def 목록보기(interaction: discord.Interaction, 주제: str):
    if 주제 not in data or not data[주제]:
        await interaction.response.send_message("목록이 없습니다")
    else:
        await interaction.response.send_message(", ".join(data[주제]))

@tree.command(name="추첨", description="주제에서 하나 뽑기")
async def 추첨(interaction: discord.Interaction, 주제: str):
    if 주제 not in data or not data[주제]:
        await interaction.response.send_message("뽑을 게 없습니다")
    else:
        await interaction.response.send_message(random.choice(data[주제]))

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=1319606110973460490))
    print("봇 준비완료")

client.run(os.environ["DISCORD_TOKEN"])

