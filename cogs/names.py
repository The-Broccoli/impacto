from discord.ext import commands
import discord
import re

class Names(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.nameTags = NameTags()  # NameTags-Klasse instanziieren
        self.target_guild_id = 1306942041644859413  # Ersetze durch die ID des gewünschten Servers

    @commands.Cog.listener('on_member_update')
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        # Prüfen, ob die Aktion auf dem Ziel-Server stattfindet
        if after.guild.id == self.target_guild_id:
            # Name überprüfen und anpassen
            await self.nameTags.magic(after)

def setup(bot):
    bot.add_cog(Names(bot))

class NameTags():
    def __init__(self) -> None:
        self.roleDic = {
            'Dawnbringer': [
                '[DB]',
                r'[\[][dD][bB][\]]',
                {
                    'DB': r'[dD][bB]',
                    'Dawnbringer': r'[dD][aA][wW][nN][bB][rR][iI][nN][gG][eE][rR]'
                }
            ],
            'Crimson': [
                '[CR]',
                r'[\[][cC][rR][\]]',
                {
                    'CR': r'[cC][rR]',
                    'Crimson': r'[cC][rR][iI][mM][sS][oO][nN]'
                }
            ],
            'Starlight': [
                '[SL]',
                r'[\[][sS][lL][\]]',
                {
                    'SL': r'[sS][lL]',
                    'Starlight': r'[sS][tT][aA][rR][lL][iI][gG][hH][tT]'
                }
            ],
            'Endgame': [
                '[EG]',
                r'[\[][eE][gG][\]]',
                {
                    'EG': r'[eE][gG]',
                    'Endgame': r'[eE][nN][dD][gG][aA][mM][eE]'
                }
            ]
        }

    async def magic(self, after: discord.Member):
        if not after.guild.me.guild_permissions.manage_nicknames:
            print("Bot hat nicht die Berechtigung 'Mitglieder verwalten'.")
            return
    
        role_keys = set(self.roleDic.keys())
        tactical_role = "DEMO-Taktische-Leitung"
        special_prefix = "✦"
    
        for a_role in after.roles:
            if a_role.name == tactical_role:
                if not after.display_name.startswith(special_prefix):
                    new_name = f"{special_prefix} {after.display_name}"
                    try:
                        await after.edit(nick=new_name)
                    except discord.Forbidden:
                        print(f"Keine Berechtigung, den Nickname von {after.display_name} zu ändern.")
                    return
    
            if a_role.name in role_keys:
                relist = self.roleDic[a_role.name]
                var1 = relist[1]
                var2 = relist[2]
    
                if re.search(var1, after.display_name):
                    break
    
                for key in var2.keys():
                    if re.search(var2[key], after.display_name):
                        new_name = re.sub(var2[key], '', after.display_name).replace(' ', '')
                        try:
                            await after.edit(nick=new_name)
                        except discord.Forbidden:
                            print(f"Keine Berechtigung, den Nickname von {after.display_name} zu ändern.")
                        return
    
                new_name = relist[0] + ' ' + after.display_name
                print(f"Trying to set new name: {new_name}")
                try:
                    await after.edit(nick=new_name)
                except discord.Forbidden:
                    print(f"Keine Berechtigung, den Nickname von {after.display_name} zu ändern.")
                return
