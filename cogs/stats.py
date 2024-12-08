from discord.ext import commands

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
        signup_data, title = SignupNames().get_signup_data(f'https://raid-helper.dev/api/v2/events/{event_id}')
        if signup_data:
            if self.members:
                # # Mitglieder, die sich nicht angemeldet haben (Namen extrahieren)
                # notsignup = [
                #     signup_data[member_id]["name"]
                #     for member_id in self.members
                #     if member_id in signup_data  # Sicherstellen, dass die ID im Dictionary existiert
                
                member_status = self.create_member_status_dict(signup_data)
                
                not_in_dic = [id_ for id_ in self.members if id_ and id_ not in member_status]
                print(not_in_dic)
                
                # Embed-Nachricht mit Ergebnissen erstellen
                embed = Messages().signup(ctx, not_in_dic, title, len(self.members), 70)
                await ctx.respond(embed=embed, ephemeral=False)
            else:
                await ctx.respond("Es sind keine Member bekannt", ephemeral=True)
        else:
            await ctx.respond("Das Raid-Helper Event wurde **nicht gefunden**!", ephemeral=True)


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