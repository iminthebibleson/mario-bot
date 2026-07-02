import discord
from discord.ext import commands
from utils.ida_loader import load_profiles


class ProfilePages(discord.ui.View):
    def __init__(self, profiles, author_id):
        super().__init__(timeout=300)

        self.author_id = author_id
        self.profiles = list(profiles.items())

        self.page = 0
        self.per_page = 5

    def create_embed(self):
        start = self.page * self.per_page
        end = start + self.per_page

        embed = discord.Embed(
            title="Profile Browser",
            color=discord.Color.blue()
        )

        for pid, profile in self.profiles[start:end]:

            name = profile.get("name") or "Unknown"

            embed.add_field(
                name=f"{pid} - {name}",
                value=(
                    f"Type: {profile.get('type', 'unknown')}\n"
                    f"Build: {profile.get('build_function', 'unknown')}"
                ),
                inline=False
            )

        total_pages = (
            len(self.profiles) + self.per_page - 1
        ) // self.per_page

        embed.set_footer(
            text=f"Page {self.page + 1}/{total_pages}"
        )

        return embed

    async def interaction_check(self, interaction):
        if interaction.user.id != self.author_id:
            await interaction.response.send_message(
                "❌ You can't control this menu.",
                ephemeral=True
            )
            return False

        return True

    @discord.ui.button(
        label="⬅️",
        style=discord.ButtonStyle.secondary
    )
    async def previous(
        self,
        button,
        interaction
    ):
        if self.page > 0:
            self.page -= 1

        await interaction.response.edit_message(
            embed=self.create_embed(),
            view=self
        )

    @discord.ui.button(
        label="➡️",
        style=discord.ButtonStyle.secondary
    )
    async def next(
        self,
        button,
        interaction
    ):
        max_page = (
            len(self.profiles) - 1
        ) // self.per_page

        if self.page < max_page:
            self.page += 1

        await interaction.response.edit_message(
            embed=self.create_embed(),
            view=self
        )

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True


class Profiles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.profiles = load_profiles()

    @commands.slash_command(
        name="profiles",
        description="Browse all profiles"
    )
    async def profiles_cmd(self, ctx):

        view = ProfilePages(
            self.profiles,
            ctx.author.id
        )

        await ctx.respond(
            embed=view.create_embed(),
            view=view
        )


def setup(bot):
    bot.add_cog(Profiles(bot))