import discord
from discord.ext import commands
from discord.ui import View, Button
import asyncio
import os

class HelpView(View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot
        self.page = 0
        self.embeds = [
            self.general_embed(),
            self.moderation_embed()
        ]

    def gradient_color(self, start_hex: str, end_hex: str, step: int):
        """Blend two hex colors for gradient-like theme."""
        start = tuple(int(start_hex[i:i+2], 16) for i in (0, 2, 4))
        end = tuple(int(end_hex[i:i+2], 16) for i in (0, 2, 4))
        ratio = step / (len(self.embeds) - 1)
        blend = tuple(int(start[i] + (end[i] - start[i]) * ratio) for i in range(3))
        return discord.Color.from_rgb(*blend)


    def general_embed(self):
        embed = discord.Embed(
            title=f"📜 {self.bot.user.name} Help Menu - General Commands",
            description="Here are some of the general commands you can use!",
            color=discord.Color.magenta()
        )
        embed.add_field(name="📋 `!serverinfo`", value="Shows detailed server information.", inline=False)
        embed.add_field(name="👤 `!userinfo`,`!whois`, `!profile`", value="Displays information about a user.", inline=False)
        embed.add_field(name="🕒 `!uptime`", value="Shows how long the bot has been online.", inline=False)
        embed.add_field(name="💡 `!ping`,`!latency`, `!speed`", value="Check the bot's latency.", inline=False)
        embed.add_field(name="🤖 `!botinfo`", value="Displays information about the bot.", inline=False)
        embed.set_footer(text="Page 1/2 • Use the buttons below to navigate")
        return embed

    def moderation_embed(self):
        embed = discord.Embed(
            title=f"🛡️ {self.bot.user.name} Help Menu - Moderation Commands",
            description="Moderation-related commands (coming soon!)",
            color=discord.Color.purple()
        )
        embed.add_field(name="🔒 `!ban`", value="Ban a member from the server.", inline=False)
        embed.add_field(name="⚠️ `!kick`", value="Kick a member from the server.", inline=False)
        embed.add_field(name="🧹 `!clear`", value="Clear messages in a channel.", inline=False)
        embed.set_footer(text="Page 2/3 • Use the buttons below to navigate")
        return embed

    def utilities_embed(self):
        embed = discord.Embed(
            title=f"🛠️ {self.bot.user.name} Help Menu - Utilities",
            description="Utilities-related commands (coming soon!)",
            color=discord.Color.purple()
        )
        embed.add_field(name="🔒 `!ban`", value="Ban a member from the server.", inline=False)
        embed.add_field(name="⚠️ `!kick`", value="Kick a member from the server.", inline=False)
        embed.add_field(name="🧹 `!clear`", value="Clear messages in a channel.", inline=False)
        embed.set_footer(text="Page 3/3 • Use the buttons below to navigate")
        return embed

    @discord.ui.button(label="◀️ Previous", style=discord.ButtonStyle.gray)
    async def previous_page(self, interaction: discord.Interaction, button: Button):
        self.page = (self.page - 1) % len(self.embeds)
        await interaction.response.edit_message(embed=self.embeds[self.page], view=self)

    @discord.ui.button(label="Next ▶️", style=discord.ButtonStyle.gray)
    async def next_page(self, interaction: discord.Interaction, button: Button):
        self.page = (self.page + 1) % len(self.embeds)
        await interaction.response.edit_message(embed=self.embeds[self.page], view=self)


class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help(self, ctx):
        """Displays a paginated help menu."""
        view = HelpView(self.bot)
        embed = view.embeds[0]
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(HelpCommand(bot))
