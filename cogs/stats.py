from discord.ext import commands
import discord

from discord.commands import slash_command
from discord import option

from signupNames import SignupNames
from messages import Messages


class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.members = []
        
    def create_member_status_dict(self, signup_data):
        member_status = {}
        
        status_mapping = {
            'Dps': 2,
            'Healer': 2,
            'Tank': 2,
            'assasine': 2,
            'Tentative': 3,
            'Absence': 3
        }
        for member_id in self.members:
            if member_id in signup_data:
                # Wenn die Member-ID in signup_data existiert, nimm den Status basierend auf className
                member_status[member_id] = {
                    'name': signup_data[member_id]['name'],
                    'status': status_mapping.get(signup_data[member_id]['className'], 0)
                }
            else:
                # Wenn die Member-ID nicht in signup_data existiert, setze Status auf 0
                member_status[member_id] = {
                    'name': 'Unknown',
                    'status': 0
                }
        return member_status

    @slash_command(name='interaction-check', description='dataTest')
    @option("Event ID", description="Event ID von Raid-Helper Event", input_type=str)
    async def interactionCheck(self, ctx, event_id: str):
        await ctx.respond("Bitte warten, Daten werden verarbeitet...", ephemeral=False)
        try:
            signup_data, title = SignupNames().get_signup_data(f'https://raid-helper.dev/api/v2/events/{event_id}')
            if signup_data:
                if self.members:
                    member_status = self.create_member_status_dict(signup_data)
                    ids_with_status_0 = [id_ for id_, details in member_status.items() if details['status'] == 0]
                    user_with_status_0 = []
                    for discord_id in ids_with_status_0:
                        try:
                            user = await self.bot.fetch_user(int(discord_id))
                            user_with_status_0.append(user.display_name)
                        except discord.NotFound:
                            user_with_status_0.append(f"Unbekannt (ID: {discord_id})")
                        except discord.HTTPException as e:
                            await ctx.edit(embed=embed)(f"Fehler beim Abrufen der ID {discord_id}: {e}")
                    embed = Messages().signup(ctx, user_with_status_0, title, len(ids_with_status_0), len(self.members))
                    await ctx.edit(embed=embed)
                else:
                    await ctx.edit(embed=embed)("Es sind keine Member bekannt", ephemeral=True)
            else:
                await ctx.edit(embed=embed)("Das Raid-Helper Event wurde **nicht gefunden**!", ephemeral=True)
        except Exception as e:
            await ctx.respond(f"Ein unerwarteter Fehler ist aufgetreten: {e}", ephemeral=True)
            raise


    @slash_command(name='setmember', description='setmember')
    async def setmembers(self, ctx, member: str):
        if member:
            member_list = member.split(' ')
            self.members = member_list
            await ctx.respond(f"Es wurden {len(member_list)} Member erkannt", ephemeral=True)
        else:
            await ctx.respond(f"Fehler?")

    @commands.Cog.listener()
    async def on_ready(self):
        print("Stats READY")
    

def setup(bot):
    bot.add_cog(Stats(bot))