import os
from dotenv import load_dotenv

import discord


def main():
    load_dotenv()
    TOKEN = os.environ['TOKEN']
    
    bot = discord.Bot()
    GUILD_ID = [1293665024665059420] # DEMO SERVER
    
    @bot.event
    async def on_ready():
        print(8 * '-' + ' IMPACT_TAL ' + 8 * '-')
        print(f'Services are now available.\nName: {bot.user}')
    
    @bot.command(description="Sends the bot's latency.", guild_ids=GUILD_ID)
    async def pingo(ctx):
        await ctx.respond(f"Pong! Latency is {bot.latency}")
    
    bot.run(TOKEN)
    
if __name__ == '__main__':
    main()