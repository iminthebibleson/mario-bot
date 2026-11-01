import discord
from discord.ext import commands
import json
import os

OWNER_IDS = [607507348323434496, 842366854697189447]
PUBLIC_CHANNEL_ID = 1516158203849740288
DATA_FILE = "data.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return {"latest_release_message_id": None}

    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


class ReleaseManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = load_data()

    async def delete_previous(self, channel):
        msg_id = self.data.get("latest_release_message_id")

        if not msg_id:
            return

        try:
            msg = await channel.fetch_message(msg_id)
            await msg.delete()
        except:
            pass

    @commands.slash_command(
        name="release",
        description="Post a new version release (owners only)"
    )
    async def release(
        self,
        ctx: discord.ApplicationContext,
        version: str,
        download: str,
        description: str
    ):
        if ctx.author.id not in OWNER_IDS:
            return await ctx.respond("❌ Not allowed.", ephemeral=True)

        channel = self.bot.get_channel(PUBLIC_CHANNEL_ID)

        if not channel:
            return await ctx.respond("❌ Public channel not found.", ephemeral=True)

        await self.delete_previous(channel)

        embed = discord.Embed(
            title=f"🚀 New Release v{version}",
            description=description,
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="⬇️ Download",
            value=f"[Click here]({download})",
            inline=False
        )

        embed.set_footer(text=f"Version {version}")

        msg = await channel.send(embed=embed)

        self.data["latest_release_message_id"] = msg.id
        save_data(self.data)

        await ctx.respond(
            f"Release v{version} posted",
        )


def setup(bot):
    bot.add_cog(ReleaseManager(bot))