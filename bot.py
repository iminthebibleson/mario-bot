import os
from dotenv import load_dotenv

import discord
from discord.ext import commands

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True


bot = commands.Bot(
    command_prefix="-",
    intents=discord.Intents.all()
)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.change_presence(
        activity=discord.Game(name="testing stage")
    )


for root, _, files in os.walk("./cogs"):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":

                module = os.path.relpath(
                    os.path.join(root, file),
                    "."
                )[:-3].replace(os.sep, ".")

                bot.load_extension(module)

bot.run(TOKEN)