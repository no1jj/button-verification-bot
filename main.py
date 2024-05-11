import discord
from discord.ui import Button, View
from discord import app_commands, Interaction, ButtonStyle
import json

CONFIG = 'config.json'

def load_config():
    with open(CONFIG, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config

def save_config(config):
    with open(CONFIG, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)

config = load_config()
TOKEN = config['token']
ROLE_ID = config['role_id']

class MyClient(discord.Client):
    async def on_ready(self):
        load_config()
        await self.wait_until_ready()
        await tree.sync()
        print(f"{self.user} 에 로그인하였습니다!")

intents = discord.Intents.all()
client = MyClient(intents=intents)
tree = app_commands.CommandTree(client)
class VerificationView(View):

    def __init__(self):
        super().__init__()
        self.add_item(Button(style=ButtonStyle.primary, label="인증", custom_id="verification_button"))

@client.event
async def on_interaction(interaction: discord.Interaction):
    t = "인증"
    d = "인증이 완료되었습니다."
    embed = discord.Embed(title=t, description=d, color=0x00ff00)

    if interaction.type == discord.InteractionType.component:
        custom_id = interaction.data["custom_id"]

        if custom_id == "verification_button":
            role_id = load_config()['role_id']
            role = interaction.guild.get_role(role_id)
            if role:
                member = interaction.guild.get_member(interaction.user.id)
                if member:
                    try:
                        await member.add_roles(role)
                    except discord.Forbidden:
                        t = "오류 발생"
                        d = "역할을 부여할 권한이 없습니다."
                        embed = discord.Embed(title=t, description=d, color=discord.Color.red())
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                    else:
                        await interaction.response.send_message(embed=embed, ephemeral=True)

                        if role_id != role.id:
                            config = load_config()
                            config['role_id'] = role.id
                            save_config(config)
                else:
                    t = "오류 발생"
                    d = "사용자를 찾을 수 없습니다."
                    embed = discord.Embed(title=t, description=d, color=discord.Color.red())
                    await interaction.response.send_message(embed==embed, ephemeral=True)
            else:
                t = "오류 발생"
                d = "역할을 찾을 수 없습니다."
                embed = discord.Embed(title=t, description=d, color=discord.Color.red())
                await interaction.response.send_message(embed=embed, ephemeral=True)

@tree.command(name="인증", description="인증버튼을 출력합니다.")
@app_commands.checks.has_permissions(administrator=True)
async def verification(interaction: discord.Interaction):
    view = VerificationView()
    t = "인증"
    d = "버튼을눌러 권한을 받으세요"
    embed = discord.Embed(title=t, description=d, color=0x00ff00)
    await interaction.response.send_message(embed=embed, view=view)

@tree.command(name="역할설정", description="인증시 부여할 역할을 설정합니다.")
@app_commands.checks.has_permissions(administrator=True)
async def set_role(interaction: discord.Interaction, role: discord.Role):
    if role is None:
        t = "오류 발생"
        d = "역할을 입력해주세요."
        embed = discord.Embed(title=t, description=d, color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    if role.id == ROLE_ID:
        t = "오류 발생"
        d = f"이미 <@&{ROLE_ID}> 역할로 설정되어 있습니다."
        embed = discord.Embed(title=t, description=d, color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    t = "역할설정 성공"
    d = f"**역할이 {role.mention}로 설정되었습니다.**"
    embed = discord.Embed(title=t, description=d, color=discord.Color.green())
    config = load_config()
    config['role_id'] = role.id
    save_config(config)
    await interaction.response.send_message(embed=embed, ephemeral=True)


@tree.command(name="역할확인", description="설정한역할을 확인합니다.")
@app_commands.checks.has_permissions(administrator=True)
async def checks_role(interaction: discord.Interaction):
    load_config
    config = load_config()
    role_id = config['role_id']
    role = interaction.guild.get_role(role_id)
    if role:
        t = "역할 확인"
        d = f"역할이 <@&{role_id}>로 설정되어있습니다."
        embed = discord.Embed(title=t, description=d, color=discord.Color.green())
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        t = "오류 발생"
        d = f"역할이 설정되어있지 않습니다."
        embed = discord.Embed(title=t, description=d, color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)

client.run(TOKEN)
