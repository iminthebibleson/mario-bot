# cogs/moderation/mute.py

import discord
from discord.ext import commands


class Mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_muted_role(self, guild):
        muted_role = discord.utils.get(guild.roles, name="Muted")

        if muted_role:
            return muted_role

        muted_role = await guild.create_role(
            name="Muted",
            reason="Mute system auto-created role"
        )

        for channel in guild.channels:
            try:
                await channel.set_permissions(
                    muted_role,
                    send_messages=False,
                    speak=False,
                    add_reactions=False
                )
            except Exception:
                pass

        return muted_role

    @commands.command(name="mute")
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx, member: discord.Member, *, reason="No reason provided"):

        if member == ctx.author:
            return await ctx.send("You cannot mute yourself.")

        muted_role = await self.get_muted_role(ctx.guild)

        if muted_role in member.roles:
            return await ctx.send("User is already muted.")

        await member.add_roles(
            muted_role,
            reason=f"{ctx.author}: {reason}"
        )

        embed = discord.Embed(
            title="User Muted",
            color=discord.Color.red()
        )

        embed.add_field(
            name="Member",
            value=member.mention,
            inline=False
        )

        embed.add_field(
            name="Reason",
            value=reason,
            inline=False
        )

        await ctx.send(embed=embed)

    @commands.command(name="unmute")
    @commands.has_permissions(administrator=True)
    async def unmute(self, ctx, member: discord.Member):

        muted_role = discord.utils.get(
            ctx.guild.roles,
            name="Muted"
        )

        if not muted_role:
            return await ctx.send("No Muted role exists.")

        if muted_role not in member.roles:
            return await ctx.send("User is not muted.")

        await member.remove_roles(
            muted_role,
            reason=f"Unmuted by {ctx.author}"
        )

        embed = discord.Embed(
            title="User Unmuted",
            color=discord.Color.green()
        )

        embed.add_field(
            name="Member",
            value=member.mention,
            inline=False
        )

        await ctx.send(embed=embed)

    @mute.error
    @unmute.error
    async def permission_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(
                "You must be an administrator to use this command."
            )


def setup(bot):
    bot.add_cog(Mute(bot))