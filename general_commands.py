import discord
from discord.ext import commands
import datetime, time
import os
import asyncio
import typing



class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.datetime.now(datetime.timezone.utc)
    
    
    @commands.command(name="serverinfo", aliases=["guildinfo"])
    async def serverinfo(self, ctx):
        """Shows a detailed, stylish overview of the server."""
        guild = ctx.guild
        now = datetime.datetime.now(datetime.timezone.utc)

        # --- Basic server data ---
        created_at = guild.created_at.strftime("%B %d, %Y • %I:%M %p")
        age_days = (now - guild.created_at).days
        owner = guild.owner or "Unknown"
        region = getattr(guild, "region", "Auto")
        boosts = guild.premium_subscription_count
        level = guild.premium_tier

        # --- Members ---
        total_members = guild.member_count
        humans = sum(not m.bot for m in guild.members)
        bots = total_members - humans

        # --- Channels ---
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        categories = len(guild.categories)

        # --- Other ---
        roles = len(guild.roles)
        emojis = len(guild.emojis)
        stickers = len(guild.stickers)

        # --- Embed Setup ---
        embed_color = discord.Color.from_str("#9b59b6")  # purple tone
        embed = discord.Embed(
            title=f"🏙️ Server Information — {guild.name}",
            description=f"Welcome to **{guild.name}**! Here’s everything you need to know ✨",
            color=embed_color,
            timestamp=now
        )

        # --- Server banner/icon handling ---
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        if guild.banner:
            embed.set_image(url=guild.banner.url)

        # --- Main Fields ---
        embed.add_field(
            name="👑 Owner",
            value=f"{owner.mention if isinstance(owner, discord.Member) else owner}",
            inline=True
        )
        embed.add_field(name="🆔 Server ID", value=f"`{guild.id}`", inline=True)
        embed.add_field(name="📅 Created On", value=f"{created_at}\n({age_days} days ago)", inline=False)

        embed.add_field(name="👥 Members", value=f"**Total:** {total_members}\n🙂 Humans: {humans}\n🤖 Bots: {bots}", inline=True)
        embed.add_field(name="💬 Channels", value=f"📝 Text: {text_channels}\n🔊 Voice: {voice_channels}\n📂 Categories: {categories}", inline=True)
        embed.add_field(name="🎭 Roles", value=f"{roles}", inline=True)

        embed.add_field(name="💎 Boosts", value=f"Level {level} ({boosts} boosts)", inline=True)
        embed.add_field(name="🌍 Region / Locale", value=f"`{region}`", inline=True)
        embed.add_field(name="🔐 Verification", value=f"{str(guild.verification_level).title()}", inline=True)

        # --- Optional sections ---
        if emojis > 0 or stickers > 0:
            embed.add_field(name="😀 Emojis", value=f"{emojis} custom", inline=True)
            embed.add_field(name="🏷️ Stickers", value=f"{stickers} custom", inline=True)

        # --- Footer and aesthetics ---
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)

        await ctx.send(embed=embed)

    @commands.command(help="Shows the avatar.")
    async def avatar(self, ctx, member: typing.Optional[discord.Member] = None): 
        member = member or ctx.author
        embed = discord.Embed(
            title=f"🖼️ Avatar - {member}",
            color=discord.Color.purple()
        )
        if member.avatar:
            embed.set_image(url=member.avatar.url)
        await ctx.send(embed=embed)

    @commands.command(help="Shows the bot uptime.")
    async def uptime(self, ctx):
        now = datetime.datetime.utcnow()
        uptime_seconds = (now - self.start_time).total_seconds()
        hours, remainder = divmod(int(uptime_seconds), 3600)
        minutes, seconds = divmod(remainder, 60)
        await ctx.send(f"⏱️ Uptime: {hours}h {minutes}m {seconds}s")



# Add the cog to the bot
async def setup(bot):
    await bot.add_cog(General(bot))
