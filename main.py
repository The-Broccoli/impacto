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


@bot.slash_command(name="showmirrorchannel", description="Spiegel Channel anzeigen.", guild_ids=[748795926402826260, 480418209099546665])
async def showmirrorchannel(ctx):
    global channel_a_server1, channel_b_server2
    await ctx.respond(f"\n'Channel: 1 -> {channel_a_server1}\nChannel: 2 -> {channel_b_server2}")


@bot.slash_command(name="setmirrorchannel", description="Setze entweder Channel A oder Channel B für das Spiegeln.", guild_ids=[748795926402826260, 480418209099546665])
@option("channel_type", description="Wähle Channel A (Server 1) oder Channel B (Server 2)", choices=["A", "B"])
@option("channel_id", description="Gib die ID des Channels an")
@is_authorized()
async def setmirrorchannel(ctx, channel_type: str, channel_id: str):
    global channel_a_server1, channel_b_server2
    try:
        channel_id_int = int(channel_id)
    except ValueError:
        await ctx.respond("Bitte gib eine gültige Channel-ID ein.")
        return

    if channel_type == "A":
        channel_a_server1 = channel_id_int
        await ctx.respond(f"Channel A (Server 1) gesetzt: {channel_a_server1}")
    elif channel_type == "B":
        channel_b_server2 = channel_id_int
        await ctx.respond(f"Channel B (Server 2) gesetzt: {channel_b_server2}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if not channel_a_server1 or not channel_b_server2:
        return
    content_to_mirror = f"{message.author.display_name} sagte: {message.content}" if message.content else None
    if message.channel.id == channel_a_server1:
        target_channel = bot.get_channel(channel_b_server2)
        if target_channel:
            if content_to_mirror:
                embed = messages().mirror_message(message.content, message.author)
                await target_channel.send(content_to_mirror)
                await target_channel.send(embed=embed)

    elif message.channel.id == channel_b_server2:
        target_channel = bot.get_channel(channel_a_server1)
        if target_channel:
            if content_to_mirror:
                embed = messages().mirror_message(message.content, message.author)
                await target_channel.send(content_to_mirror)
                await target_channel.send(embed=embed)

bot.run(TOKEN)