import discord
from discord.ext import commands
from fuzzywuzzy import process
from utils.ida_loader import load_sprites


class SearchResultsView(discord.ui.View):
    def __init__(self, results, author_id):
        super().__init__(timeout=300)

        self.results = results
        self.author_id = author_id
        self.page = 0
        self.per_page = 5

    def create_embed(self):
        embed = discord.Embed(
            title="🔍 Search Results",
            color=discord.Color.blue()
        )

        start = self.page * self.per_page
        end = start + self.per_page

        for sid, data, score in self.results[start:end]:

            embed.add_field(
                name=f"{data.get('name', 'Unknown')} ({score}%)",
                value=(
                    f"ID: `{sid}`\n"
                    f"Address: `{data.get('address', 'Unknown')}`\n"
                    f"Size: `{data.get('size', 'Unknown')}`\n"
                    f"Calls: `{data.get('called_from_count', 0)}`"
                ),
                inline=False
            )

        total_pages = (
            len(self.results) + self.per_page - 1
        ) // self.per_page

        embed.set_footer(
            text=f"Page {self.page + 1}/{total_pages}"
        )

        return embed

    async def interaction_check(self, interaction):
        if interaction.user.id != self.author_id:
            await interaction.response.send_message(
                "❌ This menu isn't yours.",
                ephemeral=True
            )
            return False

        return True

    @discord.ui.button(
        emoji="⬅️",
        style=discord.ButtonStyle.secondary
    )
    async def previous(self, button, interaction):

        if self.page > 0:
            self.page -= 1

        await interaction.response.edit_message(
            embed=self.create_embed(),
            view=self
        )

    @discord.ui.button(
        emoji="➡️",
        style=discord.ButtonStyle.secondary
    )
    async def next(self, button, interaction):

        max_page = (
            len(self.results) - 1
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


class FuzzySprite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sprites = load_sprites()

    @commands.slash_command(
        name="fuzzysprite",
        description="Search sprite/function names"
    )
    async def fuzzysprite(self, ctx, query: str):

        names = {}

        for sid, sprite in self.sprites.items():
            names[sid] = sprite.get("name", "Unknown")

        matches = process.extract(
            query,
            list(names.values()),
            limit=50
        )

        results = []

        for name, score in matches:

            sid = next(
                (k for k, v in names.items() if v == name),
                None
            )

            if sid:
                results.append(
                    (
                        sid,
                        self.sprites[sid],
                        score
                    )
                )

        if not results:
            return await ctx.respond(
                "❌ No matches found."
            )

        view = SearchResultsView(
            results,
            ctx.author.id
        )

        await ctx.respond(
            embed=view.create_embed(),
            view=view
        )


def setup(bot):
    bot.add_cog(FuzzySprite(bot))