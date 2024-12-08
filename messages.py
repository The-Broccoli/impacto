import discord
from discord.ext import commands

class Messages():

    def __init__(self):
        self.botVersion = '0.2'

    def add_footer_raid(self, ctx: commands.Context, embed: discord.Embed):
        """Adds the footer to the embed"""
        embed.set_footer(
            text=f'{ctx.author.display_name} has rolled this raid  - impacto (Discord Bot)', icon_url=ctx.author.avatar.url)
        return embed
        
    def add_footer_mirror(self, author, embed: discord.Embed, serverName):
        """Adds the footer to the embed"""
        embed.set_footer(
            text=f'{author.display_name} - {serverName}', icon_url=author.avatar.url)
        return embed

    def raid_group(self, ctx, user_list):
        """Returns an embed for raidroll"""
        g = 0
        embed = discord.Embed(title='Gildenraid Gruppen',
                            color=discord.Color.dark_orange(),
                            description='Die Gruppenanführer (⭐️) erstellen jetzt eine Gruppe und posten den Gruppenlink im Gilden-Chat')
        for group in user_list:
            g += 1
            group[0] = group[0] + ' ⭐'
            string = "\n".join([str(element) for element in group])
            embed.add_field(name=f'Gruppe {g}',
                            value=f"```{string}```",
                            inline=False)
        embed.add_field(name=f'',
                        value=f"Die Gruppenanführer (⭐️) erstellen jetzt eine Gruppe und posten den Gruppenlink im Gilden-Chat",
                        inline=False)
        embed.set_thumbnail(url="https://iili.io/2J5yYeS.png")
        embed.set_author(name="Impact Würfel", icon_url="https://iili.io/2J5yYeS.png")
        embed = self.add_footer_raid(ctx, embed)
        return embed

    # def mirror_message(self, content, author, serverName):
    #     embed = discord.Embed(title='',
    #                         color=discord.Color.dark_grey(),
    #                         description=content)
    #     embed = self.add_footer_mirror(author, embed, serverName)
    #     return embed

    def signup(self, ctx, notsignup, eID, var1, var2):
        embed = discord.Embed(
            title=f'Nicht registriert?\n{eID}',
            color=discord.Color.random(),
            description='Diese Member haben nicht mit dem Event interagiert oder stehen nicht als eingetragenes Mitglied in der Member-Datenbank.'
        )
        # Namen in Gruppen von 10 aufteilen
        for i in range(0, len(notsignup), 10):
            # Namen in der aktuellen Gruppe als Zeichenkette zusammenfügen
            group = '\n'.join(notsignup[i:i + 10])
            embed.add_field(name=f"", value=group, inline=True)
            embed.set_footer(text=f'{var1 - var2} ({var2} von {var1})')
        return embed