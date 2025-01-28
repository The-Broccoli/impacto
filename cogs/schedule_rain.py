from discord.ext import commands, tasks
import discord
import datetime

from sheetAutomation import GoogleSheetAutomation

class Rain(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sheet_automation = GoogleSheetAutomation()
        self.spreadsheet_id = '1xFt4y2wLT8P19oEdFuDHrKtUpwWLLBYXcIXNvgpBq3k'  # Ersetze durch deine Sheet-ID
        # sheet_automation.check_and_delete_rows(spreadsheet_id, sheet_name='rain_schedule')
        self.set_activity.start()
        
    # --------------------------------
    # LOOP - Activity

    @tasks.loop(seconds=60.0)
    async def set_activity(self):
        "Listening to rain in 27 min, Watching for rain in 27 min"
        
        last_valid_time = self.sheet_automation.check_and_delete_rows(self.spreadsheet_id, sheet_name='rain_schedule')
        last_valid_time = calculate_minutes_difference(last_valid_time)
        
        l: str = f"for rain in {last_valid_time} min"
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=l))

    @set_activity.before_loop
    async def before_set_activity(self):
        await self.bot.wait_until_ready()
        
def calculate_minutes_difference(last_valid_time):
    """
    Berechnet die Minuten zwischen last_valid_time und der aktuellen Uhrzeit.

    Args:
        last_valid_time (str): Die letzte gültige Uhrzeit im Format '%Y-%m-%d %H:%M'.

    Returns:
        str: Die Differenz in Minuten als String, oder eine Fehlermeldung, falls das Format ungültig ist.
    """
    try:
        # Konvertiere last_valid_time in ein datetime-Objekt
        last_valid_dt = datetime.datetime.strptime(last_valid_time, '%Y-%m-%d %H:%M')
        # Berechne die Differenz zur aktuellen Zeit
        now = datetime.datetime.now()
        difference = now - last_valid_dt
        # Extrahiere die Minuten aus der Differenz und konvertiere sie in eine positive Zahl
        minutes = abs(int(difference.total_seconds() // 60))
        return f"{minutes}"
    except ValueError:
        print("Ungültiges Datumsformat. Erwartet: '%Y-%m-%d %H:%M'")
        return "X"
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
        return "X"

def setup(bot):
    bot.add_cog(Rain(bot))