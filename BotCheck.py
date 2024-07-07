import os
from dotenv import load_dotenv
import discord
from discord.ext import bridge, commands, tasks

# Bot target server
serverID = 841470692070522900

description = """
Self-verification tool for linking Discord users to their Speedrun.com profiles.
"""

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = bridge.Bot(
   command_prefix="/",
   description=description,
   intents=intents,
   debug_guilds=[serverID]
)

status = [
   "Online!"
]


@client.event
async def on_ready():
   print("Bot is now online!!")
   change_status.start()
   

@client.event
async def on_command_error(error):
   if isinstance(error, commands.CommandOnCooldown):
       print("error1")
   elif isinstance(error, commands.DisabledCommand):
       print("error2")
   elif isinstance(error, commands.CommandNotFound):
       print("error3")


@tasks.loop(hours=24)
async def change_status():


   await client.change_presence(activity=discord.Game((status[0])))
   print("Changed status to " + status[0])


for filename in os.listdir("./cogs"):
   if filename.endswith("py"):
       client.load_extension("cogs." + filename[:-3])

load_dotenv()

client.run(os.getenv("DISCORD_API_KEY"))