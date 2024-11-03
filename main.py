import discord
from discord.ext import commands
from discord import option
import asyncio

from matchmaking import group_matchmaking
from messages import messages
from constant import Constant

intents = discord.Intents.default()
intents.members = True
intents.voice_states = True
intents.message_content = True
bot = commands.Bot(intents=intents)
TOKEN = 'DISCORD_TOKEN'

channel_a_server1 = None
channel_b_server2 = None

@bot.event
async def on_ready():
    print(8 * '-' + ' IMPACT_TAL ' + 8 * '-')
    print(f'Services are now available.\nName: {bot.user}')
    print('successfully finished startup')


def is_authorized():
    async def predicate(ctx):
        allowed_roles = ["Gildenleitung", "Würfelmeister"]
        return any(role.name in allowed_roles for role in ctx.author.roles)
    return commands.check(predicate)


@bot.slash_command(description="Erfasst Rollen der Mitglieder im Stage-Kanal", guild_ids=[748795926402826260])
@is_authorized()
async def raidroll(ctx):
    await ctx.defer()

    # Finde den Stage-Kanal
    stage_channel = discord.utils.get(ctx.guild.stage_channels, name="Event")
    if stage_channel is None:
        await ctx.respond("Kein Stage-Kanal gefunden.")
        return

    # Warte kurz, um sicherzustellen, dass die aktuellsten Daten verfügbar sind
    await asyncio.sleep(2)

    # Hole alle Mitglieder im Stage-Kanal
    user_roles = {}
    for member in stage_channel.members:
        role_data = [0, 0, 0]
        for role in member.roles:
            if role.name == "Tank":
                role_data[0] = 1
            elif role.name == "Healer":
                role_data[1] = 1
            elif role.name == "DPS":
                role_data[2] = 1
        user_roles[member.display_name] = role_data

    if not user_roles:
        await ctx.respond("Keine Mitglieder im Stage-Kanal gefunden.")
        return

    # Debug-Ausgabe
    print(f"Anzahl der erfassten Mitglieder: {len(user_roles)}")
    for name, roles in user_roles.items():
        print(f"{name}: {roles}")

    gruppen = group_matchmaking(user_roles)
    embed = messages().raid_group(ctx, gruppen)

    # # Vorübergehende Ausgabe, bis die Gruppenfunktion implementiert ist
    # response = "Erfasste Mitglieder und ihre Rollen:\n\n"
    # for name, roles in user_roles.items():
    #     role_str = "Tank" if roles[0] else "Healer" if roles[1] else "DPS" if roles[2] else "Keine Rolle"
    #     response += f"{name}: {role_str}\n"

    await ctx.respond(embed=embed)


@bot.slash_command(description="Erfasst Rollen der Mitglieder im Stage-Kanal", guild_ids=[748795926402826260])
@is_authorized()
async def demoraid(ctx):
    user_roles = Constant.demo_raid_grops(4,4,16)
    gruppen = group_matchmaking(user_roles)
    embed = messages().raid_group(ctx, gruppen)
    await ctx.respond(embed=embed)

from discord.commands import option
from typing import Dict, Optional

# Store channels as a nested dictionary: server -> channel type -> channel id
channels = {
    "1": {"main": None, "secondary": None},  # Server 1 channels
    "2": {"main": None, "secondary": None},  # Server 2 channels
    "3": {"main": None, "secondary": None},  # Server 3 channels
    "4": {"main": None, "secondary": None}   # Server 4 channels
}

# List of allowed server IDs
ALLOWED_SERVERS = [748795926402826260, 480418209099546665]  # Add your other server IDs

@bot.slash_command(
    name="showmirrorchannels",
    description="Alle Spiegel Channel anzeigen.",
    guild_ids=ALLOWED_SERVERS
)
async def showmirrorchannels(ctx):
    channel_info = ""
    for server_num, server_channels in channels.items():
        channel_info += f"\nServer {server_num}:\n"
        channel_info += f"  Hauptchannel: {server_channels['main']}\n"
        channel_info += f"  Zweitchannel: {server_channels['secondary']}\n"
    await ctx.respond(f"Aktuelle Channel Konfiguration:{channel_info}")

@bot.slash_command(
    name="setmirrorchannel",
    description="Setze einen Channel für das Spiegeln.",
    guild_ids=ALLOWED_SERVERS
)
@option(
    "server_num",
    description="Wähle den Server (1-4)",
    choices=["1", "2", "3", "4"]
)
@option(
    "channel_type",
    description="Wähle den Channel-Typ",
    choices=["main", "secondary"]
)
@option("channel_id", description="Gib die ID des Channels an")
@is_authorized()
async def setmirrorchannel(ctx, server_num: str, channel_type: str, channel_id: str):
    try:
        channel_id_int = int(channel_id)
    except ValueError:
        await ctx.respond("Bitte gib eine gültige Channel-ID ein.")
        return

    channels[server_num][channel_type] = channel_id_int
    channel_type_name = "Hauptchannel" if channel_type == "main" else "Zweitchannel"
    await ctx.respond(f"{channel_type_name} für Server {server_num} wurde auf {channel_id_int} gesetzt.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Find source server and channel type
    source_server = None
    source_type = None
    
    for server_num, server_channels in channels.items():
        for channel_type, channel_id in server_channels.items():
            if channel_id == message.channel.id:
                source_server = server_num
                source_type = channel_type
                break
        if source_server:
            break

    if not source_server:
        return

    # Mirror to all other servers' corresponding channels
    for server_num, server_channels in channels.items():
        if server_num != source_server:  # Don't mirror to source server
            # Mirror to the corresponding channel type (main->main, secondary->secondary)
            target_channel_id = server_channels[source_type]
            if target_channel_id:
                target_channel = bot.get_channel(target_channel_id)
                if target_channel:
                    embed = messages().mirror_message(
                        content=message.content,
                        author=message.author,
                        guild_name=message.guild.name,
                        source_server=f"Server {source_server}",
                        channel_type=source_type
                    )
                    await target_channel.send(embed=embed)

class messages:
    def mirror_message(self, content: str, author, guild_name: str, source_server: str, channel_type: str):
        embed = discord.Embed(
            description=content,
            color=discord.Color.blue() if channel_type == "main" else discord.Color.green()
        )
        embed.set_author(
            name=f"{author.display_name} ({guild_name})",
            icon_url=author.avatar.url if author.avatar else None
        )
        return embed

bot.run(TOKEN)