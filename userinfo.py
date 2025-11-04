import discord
from discord.ext import commands
from datetime import datetime

class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="userinfo", aliases=["whois", "profile"])
    async def userinfo(self, ctx, member: discord.Member = None):
        member = member or ctx.author

        # Dynamic gradient color (based on user's ID for variation)
        gradient_colors = [0xff7eb3, 0x8b5cf6, 0x4ade80]
        color = gradient_colors[member.id % len(gradient_colors)]

        embed = discord.Embed(
            title=f"🌈 AI HOSHINO | User Profile",
            description=f"Here’s everything about **{member.mention}**",
            color=color,
            timestamp=datetime.utcnow()
        )

        # Avatar + banner
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_author(
            name=f"{member.display_name}",
            icon_url=member.display_avatar.url
        )
        embed.set_footer(
            text=f"Requested by {ctx.author.display_name} • {ctx.guild.name}",
            icon_url=ctx.author.display_avatar.url
        )

        # Fetch user banner (if available)
        try:
            user = await ctx.bot.fetch_user(member.id)
            if user.banner:
                embed.set_image(url=user.banner.url)
        except:
            pass

        # Dates
        created = member.created_at.strftime("%b %d, %Y — %I:%M %p")
        joined = member.joined_at.strftime("%b %d, %Y — %I:%M %p") if member.joined_at else "N/A"

        # Roles
        roles = [r.mention for r in member.roles if r != ctx.guild.default_role]
        roles_display = ", ".join(roles) if roles else "No roles"

        # Badges
        badges = []
        pf = member.public_flags
        if pf.hypesquad_bravery: badges.append("🦁 Bravery")
        if pf.hypesquad_brilliance: badges.append("🦄 Brilliance")
        if pf.hypesquad_balance: badges.append("🐉 Balance")
        if pf.staff: badges.append("👑 Discord Staff")
        if pf.partner: badges.append("💎 Partner")
        if pf.verified_bot: badges.append("🤖 Verified Bot")
        if pf.active_developer: badges.append("💻 Active Dev")
        badges_display = " | ".join(badges) if badges else "No badges"

        # Status + activity
        status = str(member.status).title()
        if member.activity:
            activity_type = member.activity.type.name.title()
            activity_name = member.activity.name
            activity_display = f"{activity_type}: {activity_name}"
        else:
            activity_display = "No current activity"

        # Add all fields
        embed.add_field(name="🆔 ID", value=f"`{member.id}`", inline=True)
        embed.add_field(name="💻 Status", value=f"{status}", inline=True)
        embed.add_field(name="🤖 Bot Account", value="✅ Yes" if member.bot else "❌ No", inline=True)
        embed.add_field(name="📅 Account Created", value=created, inline=False)
        embed.add_field(name="📥 Joined Server", value=joined, inline=False)
        embed.add_field(name="🏷️ Roles", value=roles_display, inline=False)
        embed.add_field(name="🏆 Badges", value=badges_display, inline=False)
        embed.add_field(name="🎮 Activity", value=activity_display, inline=False)

        # Fancy divider line
        embed.add_field(
            name="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            value="✨ *User data pulled successfully by AI HOSHINO*",
            inline=False
        )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(UserInfo(bot))
