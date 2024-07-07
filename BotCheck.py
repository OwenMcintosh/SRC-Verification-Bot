import os
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks

description = """
Self-verification tool for linking Discord users to their Speedrun.com profiles.
"""

bot = discord.Bot()

status = [
   "Online!"
]


@bot.event
async def on_ready():
   print("Bot is now online!!")
   change_status.start()
   

@bot.event
async def on_command_error(error):
   if isinstance(error, commands.CommandOnCooldown):
       print("Cooldown Error")
   elif isinstance(error, commands.DisabledCommand):
       print("Disabled Command")
   elif isinstance(error, commands.CommandNotFound):
       print("Not Found")


@tasks.loop(hours=24)
async def change_status():

   await bot.change_presence(activity=discord.Game((status[0])))
   print("Changed status to " + status[0])


load_dotenv()

bot.load_extensions("cogs")

bot.run(os.getenv("DISCORD_API_KEY"))