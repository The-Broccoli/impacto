import discord
from discord.ext import commands

class messages():

    def __init__(self):
        self.botVersion = '0.2'


    def add_footer(self, ctx: commands.Context, embed: discord.Embed):
        """Adds the footer to the embed"""
        embed.set_footer(
            text=f'{ctx.author.display_name} has rolled this raid  - impacto (Discord Bot)', icon_url=ctx.author.avatar.url)
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
        embed = self.add_footer(ctx, embed)
        return embed