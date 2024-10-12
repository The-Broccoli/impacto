import discord
from discord.ext import commands
import asyncio

import os
# from dotenv import load_dotenv

from matchmaking import group_matchmaking
from messages import messages

intents = discord.Intents.default()
intents.members = True
intents.voice_states = True

# load_dotenv()

bot = commands.Bot(intents=intents)
TOKEN = os.getenv("DISCORD_TOKEN")

@bot.event
async def on_ready():
    print(8 * '-' + ' IMPACT_TAL ' + 8 * '-')
    print(f'Services are now available.\nName: {bot.user}')
    
def is_authorized():
    async def predicate(ctx):
        allowed_roles = ["Impact Leader", "Impact Berater"]
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
    embed = messages().raid_group(gruppen)

    # # Vorübergehende Ausgabe, bis die Gruppenfunktion implementiert ist
    # response = "Erfasste Mitglieder und ihre Rollen:\n\n"
    # for name, roles in user_roles.items():
    #     role_str = "Tank" if roles[0] else "Healer" if roles[1] else "DPS" if roles[2] else "Keine Rolle"
    #     response += f"{name}: {role_str}\n"

    await ctx.respond(embed=embed)

# Stellen Sie sicher, dass Sie den Bot mit dem korrekten Token starten
bot.run(TOKEN)