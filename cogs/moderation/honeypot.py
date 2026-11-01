import discord
from discord.ext import commands
from datetime import datetime, timedelta, timezone

LOG_CHANNEL_ID = 1522088879446949970


class Honeypot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.honeypot_channels = {
            1522083206319570986
        }

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        if message.guild is None:
            return

        if message.channel.id not in self.honeypot_channels:
            return

        # Allow admins
        if message.author.guild_permissions.administrator:
            return

        guild = message.guild

        log_channel = guild.get_channel(LOG_CHANNEL_ID)

        now = datetime.now(timezone.utc)
        cutoff = now - timedelta(minutes=5)

        deleted_count = 0

        # DELETE LAST 5 MINUTES OF USER MESSAGES
        try:
            async for msg in message.channel.history(limit=100):
                if msg.author.id == message.author.id and msg.created_at >= cutoff:
                    try:
                        await msg.delete()
                        deleted_count += 1
                    except discord.Forbidden:
                        pass
        except Exception:
            pass

        # KICK USER
        kicked = False
        try:
            await message.author.kick(reason="Triggered honeypot channel.")
            kicked = True
        except discord.Forbidden:
            pass

        # LOG EMBED
        if log_channel:
            embed = discord.Embed(
                title="🚨 Honeypot Triggered",
                color=discord.Color.red(),
                timestamp=datetime.now(timezone.utc)
            )

            embed.add_field(
                name="User",
                value=f"{message.author} ({message.author.id})",
                inline=False
            )

            embed.add_field(
                name="Channel",
                value=message.channel.mention,
                inline=False
            )

            embed.add_field(
                name="Deleted Messages (5 min)",
                value=str(deleted_count),
                inline=True
            )

            embed.add_field(
                name="Action",
                value="Kicked" if kicked else "Kick Failed",
                inline=True
            )

            await log_channel.send(embed=embed)

        # Channel warning
        try:
            await message.channel.send(
                f"{message.author.mention} triggered the honeypot.",
                delete_after=10
            )
        except discord.Forbidden:
            pass


def setup(bot):
    bot.add_cog(Honeypot(bot))