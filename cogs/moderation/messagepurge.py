import discord
from discord.ext import commands


class PurgeUser(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="purgeuser")
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def purgeuser(self, ctx, target: str, amount: str):

        await ctx.message.delete()

        # DELETE ALL MESSAGES IN CHANNEL
        if target.lower() == "all":

            if amount.lower() == "all":
                deleted = await ctx.channel.purge(limit=None)

                msg = await ctx.send(f"Deleted {len(deleted)} messages.")
                await msg.delete(delay=5)
                return

            try:
                amount = int(amount)
            except ValueError:
                return await ctx.send("Amount must be a number.", delete_after=5)

            deleted = await ctx.channel.purge(limit=amount)

            msg = await ctx.send(f"Deleted {len(deleted)} messages.")
            await msg.delete(delay=5)
            return

        # MUST BE A USER MENTION
        if not ctx.message.mentions:
            return await ctx.send("Please mention a user.", delete_after=5)

        member = ctx.message.mentions[0]

        # DELETE ALL FROM USER
        if amount.lower() == "all":
            deleted = await ctx.channel.purge(
                limit=1000,
                check=lambda m: m.author.id == member.id
            )

            msg = await ctx.send(
                f"Deleted {len(deleted)} messages from {member.mention}."
            )
            await msg.delete(delay=5)
            return

        # DELETE X AMOUNT FROM USER
        try:
            amount = int(amount)
        except ValueError:
            return await ctx.send("Amount must be a number or 'all'.", delete_after=5)

        found = 0

        def check(message):
            nonlocal found
            if message.author.id == member.id and found < amount:
                found += 1
                return True
            return False

        deleted = await ctx.channel.purge(
            limit=1000,
            check=check
        )

        msg = await ctx.send(
            f"Deleted {len(deleted)} messages from {member.mention}."
        )
        await msg.delete(delay=5)


def setup(bot):
    bot.add_cog(PurgeUser(bot))