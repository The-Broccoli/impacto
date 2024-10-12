import discord
from discord.ext import commands

class messages():

    def raid_group(self, user_list):
        """Returns an embed for raidroll"""
        g = 0
        embed = discord.Embed(title='Gildenraid Gruppen',
                            color=discord.Color.dark_orange(),
                            description='Bitte schreibt eure Gruppenanführer (⭐) Mit einem **+** an ')
        for group in user_list:
            g += 1
            group[0] = group[0] + ' ⭐'
            string = "\n".join([str(element) for element in group])
            embed.add_field(name=f'Gruppe {g}',
                            value=f"```{string}```",
                            inline=False)
        return embed