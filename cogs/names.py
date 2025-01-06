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
            'Aura': [
                '[A]',
                r'[\[][aA][\]]',
                {
                    'A': r'[aA]',
                    'Aura': r'[aA][uU][rR][aA]'
                }
            ],
            'KrawallKommando': [
                '[KK]',
                r'[\[][kK][kK][\]]',
                {
                    'KK': r'[kK][kK]',
                    'KrawallKommando': r'[kK][rR][aA][wW][aA][lL][lL][kK][oO][mM][mM][aA][nN][dD][oO]'
                }
            ],
            'Hakuna Matata': [
                '[HM]',
                r'[\[][hH][mM][\]]',
                {
                    'HM': r'[hH][mM]',
                    'Hakuna Matata': r'[hH][aA][kK][uU][nN][aA][mM][aA][tT][aA][tT][aA]'
                }
            ]
        }

    async def magic(self, after: discord.ClientUser):
        role_keys = set(self.roleDic.keys())
        for a_role in after.roles:
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
                try:
                    await after.edit(nick=new_name)
                except discord.Forbidden:
                    print(f"Keine Berechtigung, den Nickname von {after.display_name} zu ändern.")
                return
    
        rollen = [role for role in after.roles if role.name != "@everyone"]
        if not any(roll.name in role_keys for roll in rollen):
            for key, relist in self.roleDic.items():
                if re.search(relist[1], after.display_name):
                    new_name = re.sub(relist[1], '', after.display_name)
                    try:
                        await after.edit(nick=new_name)
                    except discord.Forbidden:
                        print(f"Keine Berechtigung, den Nickname von {after.display_name} zu ändern.")
                    return