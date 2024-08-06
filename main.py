import discord
from discord.ext import commands
import os
import asyncio
from art import text2art
from colorama import Fore, Style
from dotenv import load_dotenv
from discord.ext.commands import has_permissions
from datetime import datetime, timedelta

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = os.getenv('GUILD_ID')
channel_id = int(os.getenv('CHANNEL_ID'))
APPLICATION_ID = os.getenv('APPLICATION_ID')
AUTHORIZED_ROLE_ID = int(os.getenv('AUTHORIZED_ROLE_ID'))
COMMAND_PREFIX = os.getenv('COMMAND_PREFIX')

intents = discord.Intents.default()
intents.members = True  
intents.message_content = True 
intents.guilds = True

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents, help_command=None)  # تعطيل الأمر الافتراضي help

def check_authorized_role(ctx):
    role = discord.utils.get(ctx.guild.roles, id=AUTHORIZED_ROLE_ID)
    if role in ctx.author.roles:
        return True
    return False


@bot.command(name='help')
async def help(ctx):
    prefix = os.getenv('COMMAND_PREFIX')
    
    embed = discord.Embed(
        title="Bot Commands",
        description="Here are the available commands:",
        color=discord.Color.blue()
    )
    
    for command in bot.commands:
        embed.add_field(
            name=f'{prefix}{command.name}',
            value=command.help if command.help else '',
            inline=False
        )
    
    await ctx.send(embed=embed)

@bot.event
async def on_member_join(member):
    role_id = os.getenv('DEFAULT_ROLE_ID')
    
    if role_id is None:
        print("Role ID not found in .env file.")
        return
    
    role = discord.utils.get(member.guild.roles, id=int(role_id))
    
    if role is None:
        print(f"Role with ID {role_id} not found in the server.")
        return
    
    try:
        await member.add_roles(role)
        print(f"Assigned role {role.name} to {member.name}.")
    except discord.Forbidden:
        print("I don't have permission to assign roles.")


def check_channel(ctx):
    # Replace 'YOUR_CHANNEL_ID' with the actual channel ID where the command should be used
    return ctx.CHANNEL_ID == APPLICATION_ID

@bot.command(name='kick')
@commands.has_permissions(administrator=True)
async def kick(ctx):
    if not check_authorized_role(ctx) or not check_channel(ctx):
        error_embed = discord.Embed(
            title="Error",
            description="You do not have the required role or are in the wrong channel to use this command.",
            color=discord.Color.red()
        )
        await ctx.send(embed=error_embed)
        return

    embed = discord.Embed(
        title="Kick Member",
        description="Please enter the member ID to kick:",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for('message', timeout=60.0, check=check)
        member_id = int(msg.content)
        guild = ctx.guild
        member = guild.get_member(member_id)

        if member:
            if check_authorized_role(ctx) and check_channel(ctx):
                try:
                    await member.kick(reason="Requested by bot")
                    confirm_embed = discord.Embed(
                        title="Member Kicked",
                        description=f'Member {member} has been kicked.',
                        color=discord.Color.green()
                    )
                    await ctx.send(embed=confirm_embed)
                except discord.Forbidden:
                    error_embed = discord.Embed(
                        title="Error",
                        description="I don't have permission to kick this member. Please check my permissions.",
                        color=discord.Color.red()
                    )
                    await ctx.send(embed=error_embed)
            else:
                error_embed = discord.Embed(
                    title="Error",
                    description="You do not have the required role or are in the wrong channel to use this command.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=error_embed)
        else:
            not_found_embed = discord.Embed(
                title="Error",
                description="Member not found.",
                color=discord.Color.red()
            )
            await ctx.send(embed=not_found_embed)
    except ValueError:
        invalid_id_embed = discord.Embed(
            title="Error",
            description="Invalid member ID. Please enter a valid number.",
            color=discord.Color.red()
        )
        await ctx.send(embed=invalid_id_embed)
    except TimeoutError:
        timeout_embed = discord.Embed(
            title="Error",
            description="You took too long to respond.",
            color=discord.Color.red()
        )
        await ctx.send(embed=timeout_embed)

def check_authorized_role(ctx):
    role_id = int(os.getenv('AUTHORIZED_ROLE_ID'))
    return any(role.id == role_id for role in ctx.author.roles)

def check_channel(ctx):
    channel_id = int(os.getenv('CHANNEL_ID'))
    return ctx.channel.id == channel_id

@bot.command(name='ban')
@commands.has_permissions(administrator=True)
async def ban(ctx):
    if not check_authorized_role(ctx) or not check_channel(ctx):
        error_embed = discord.Embed(
            title="Error",
            description="You do not have the required role or are in the wrong channel to use this command.",
            color=discord.Color.red()
        )
        await ctx.send(embed=error_embed)
        return

    embed = discord.Embed(
        title="Ban Member",
        description="Please enter the member ID to ban:",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for('message', timeout=60.0, check=check)
        member_id = int(msg.content)
        guild = ctx.guild
        member = guild.get_member(member_id)

        if member:
            try:
                await member.ban(reason="Requested by bot")
                confirm_embed = discord.Embed(
                    title="Member Banned",
                    description=f'Member {member} has been banned.',
                    color=discord.Color.green()
                )
                await ctx.send(embed=confirm_embed)
            except discord.Forbidden:
                error_embed = discord.Embed(
                    title="Error",
                    description="I don't have permission to ban this member. Please check my permissions.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=error_embed)
        else:
            not_found_embed = discord.Embed(
                title="Error",
                description="Member not found.",
                color=discord.Color.red()
            )
            await ctx.send(embed=not_found_embed)
    except ValueError:
        invalid_id_embed = discord.Embed(
            title="Error",
            description="Invalid member ID. Please enter a valid number.",
            color=discord.Color.red()
        )
        await ctx.send(embed=invalid_id_embed)
    except TimeoutError:
        timeout_embed = discord.Embed(
            title="Error",
            description="You took too long to respond.",
            color=discord.Color.red()
        )
        await ctx.send(embed=timeout_embed)

@bot.command(name='unban')
@commands.has_permissions(administrator=True)
async def unban(ctx):
    if not check_authorized_role(ctx) or not check_channel(ctx):
        error_embed = discord.Embed(
            title="Error",
            description="You do not have the required role or are in the wrong channel to use this command.",
            color=discord.Color.red()
        )
        await ctx.send(embed=error_embed)
        return

    embed = discord.Embed(
        title="Unban Member",
        description="Please enter the member ID to unban:",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for('message', timeout=60.0, check=check)
        member_id = int(msg.content)

        banned_users = [entry async for entry in ctx.guild.bans()]
        user = discord.utils.find(lambda u: u.user.id == member_id, banned_users)

        if user:
            try:
                await ctx.guild.unban(user.user, reason="Requested by bot")
                confirm_embed = discord.Embed(
                    title="Member Unbanned",
                    description=f'Member {user.user} has been unbanned.',
                    color=discord.Color.green()
                )
                await ctx.send(embed=confirm_embed)
            except discord.Forbidden:
                error_embed = discord.Embed(
                    title="Error",
                    description="I don't have permission to unban this member. Please check my permissions.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=error_embed)
        else:
            not_found_embed = discord.Embed(
                title="Error",
                description="Member not found in the ban list.",
                color=discord.Color.red()
            )
            await ctx.send(embed=not_found_embed)
    except ValueError:
        invalid_id_embed = discord.Embed(
            title="Error",
            description="Invalid member ID. Please enter a valid number.",
            color=discord.Color.red()
        )
        await ctx.send(embed=invalid_id_embed)
    except TimeoutError:
        timeout_embed = discord.Embed(
            title="Error",
            description="You took too long to respond.",
            color=discord.Color.red()
        )
        await ctx.send(embed=timeout_embed)

# Allowed timeout durations in seconds
ALLOWED_DURATIONS = {
    '5m': timedelta(minutes=5),
    '10m': timedelta(minutes=10),
    '15m': timedelta(minutes=15),
    '30m': timedelta(minutes=30),
    '1h': timedelta(hours=1)
}

@bot.command(name='timeout')
@commands.has_permissions(administrator=True)
async def timeout(ctx):
    if not check_authorized_role(ctx) or not check_channel(ctx):
        error_embed = discord.Embed(
            title="Error",
            description="You do not have the required role or are in the wrong channel to use this command.",
            color=discord.Color.red()
        )
        await ctx.send(embed=error_embed)
        return

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        # طلب معرف العضو
        await ctx.send("Please enter the member ID to timeout:")

        msg = await bot.wait_for('message', timeout=60.0, check=check)
        member_id = int(msg.content)
        member = ctx.guild.get_member(member_id)

        if member:
            # طلب المدة
            duration_list = ', '.join(ALLOWED_DURATIONS.keys())
            duration_embed = discord.Embed(
                title="Timeout Duration",
                description=f"Please enter the timeout duration. Allowed durations are: {duration_list}",
                color=discord.Color.blue()
            )
            await ctx.send(embed=duration_embed)

            try:
                duration_msg = await bot.wait_for('message', timeout=60.0, check=check)
                duration = duration_msg.content.lower()

                if duration in ALLOWED_DURATIONS:
                    duration_timedelta = ALLOWED_DURATIONS[duration]

                    # تطبيق التوقيت
                    until_time = discord.utils.utcnow() + duration_timedelta
                    await member.timeout(until_time, reason="Requested by bot")
                    confirm_embed = discord.Embed(
                        title="Member Timeout",
                        description=f'Member {member} has been timed out for {duration}.',
                        color=discord.Color.green()
                    )
                    await ctx.send(embed=confirm_embed)
                else:
                    invalid_duration_embed = discord.Embed(
                        title="Error",
                        description=f"Invalid duration. Allowed durations are: {duration_list}.",
                        color=discord.Color.red()
                    )
                    await ctx.send(embed=invalid_duration_embed)

            except TimeoutError:
                timeout_embed = discord.Embed(
                    title="Error",
                    description="You took too long to respond.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=timeout_embed)

        else:
            not_found_embed = discord.Embed(
                title="Error",
                description="Member not found.",
                color=discord.Color.red()
            )
            await ctx.send(embed=not_found_embed)

    except ValueError:
        invalid_id_embed = discord.Embed(
            title="Error",
            description="Invalid member ID. Please enter a valid number.",
            color=discord.Color.red()
        )
        await ctx.send(embed=invalid_id_embed)
    except TimeoutError:
        timeout_embed = discord.Embed(
            title="Error",
            description="You took too long to respond.",
            color=discord.Color.red()
        )
        await ctx.send(embed=timeout_embed)
    except Exception as e:
        # أرسل رسالة خطأ مع تفاصيل الاستثناء
        error_embed = discord.Embed(
            title="Error",
            description=f"An error occurred: {e}",
            color=discord.Color.red()
        )
        await ctx.send(embed=error_embed)

@bot.command(name='remove_timeout')
@commands.has_permissions(administrator=True)
async def remove_timeout(ctx):
    if not check_authorized_role(ctx) or not check_channel(ctx):
        error_embed = discord.Embed(
            title="Error",
            description="You do not have the required role or are in the wrong channel to use this command.",
            color=discord.Color.red()
        )
        await ctx.send(embed=error_embed)
        return

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        await ctx.send("Please enter the member ID to remove timeout:")

        msg = await bot.wait_for('message', timeout=60.0, check=check)
        member_id = int(msg.content)
        member = ctx.guild.get_member(member_id)

        if member:
            if member.timed_out_until:
                await member.timeout(None, reason="Timeout removed by bot")
                confirm_embed = discord.Embed(
                    title="Timeout Removed",
                    description=f'Timeout for member {member} has been removed.',
                    color=discord.Color.green()
                )
                await ctx.send(embed=confirm_embed)
            else:
                not_timed_out_embed = discord.Embed(
                    title="Error",
                    description=f'Member {member} is not currently timed out.',
                    color=discord.Color.red()
                )
                await ctx.send(embed=not_timed_out_embed)
        else:
            not_found_embed = discord.Embed(
                title="Error",
                description="Member not found.",
                color=discord.Color.red()
            )
            await ctx.send(embed=not_found_embed)
    except ValueError:
        invalid_id_embed = discord.Embed(
            title="Error",
            description="Invalid member ID. Please enter a valid number.",
            color=discord.Color.red()
        )
        await ctx.send(embed=invalid_id_embed)
    except TimeoutError:
        timeout_embed = discord.Embed(
            title="Error",
            description="You took too long to respond.",
            color=discord.Color.red()
        )
        await ctx.send(embed=timeout_embed)
    except Exception as e:
        error_embed = discord.Embed(
            title="Error",
            description=f"An error occurred: {e}",
            color=discord.Color.red()
        )
        await ctx.send(embed=error_embed)

@bot.command(name='manage_role')
@commands.has_permissions(administrator=True)
async def manage_role(ctx):
    if not check_authorized_role(ctx) or not check_channel(ctx):
        error_embed = discord.Embed(
            title="Error",
            description="You do not have the required role or are in the wrong channel to use this command.",
            color=discord.Color.red()
        )
        await ctx.send(embed=error_embed)
        return

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        # طلب تحديد الإجراء (إضافة أو إزالة)
        await ctx.send("Please respond with 'add' to add a role or 'remove' to remove a role:")

        msg = await bot.wait_for('message', timeout=60.0, check=check)
        action = msg.content.lower()

        if action not in ['add', 'remove']:
            await ctx.send("Invalid action. Please respond with 'add' or 'remove'.")
            return

        # طلب معرف الرتبة
        await ctx.send("Please enter the role ID:")

        msg = await bot.wait_for('message', timeout=60.0, check=check)
        role_id = int(msg.content)
        role = ctx.guild.get_role(role_id)

        if not role:
            await ctx.send("Role not found. Please check the role ID.")
            return

        # طلب معرف العضو
        await ctx.send("Please enter the member ID:")

        msg = await bot.wait_for('message', timeout=60.0, check=check)
        member_id = int(msg.content)
        member = ctx.guild.get_member(member_id)

        if not member:
            await ctx.send("Member not found. Please check the member ID.")
            return

        if action == 'add':
            if role in member.roles:
                await ctx.send("Member already has this role.")
            else:
                await member.add_roles(role, reason="Role added by bot")
                await ctx.send(f"Role {role.name} has been added to {member.display_name}.")
        elif action == 'remove':
            if role not in member.roles:
                await ctx.send("Member does not have this role.")
            else:
                await member.remove_roles(role, reason="Role removed by bot")
                await ctx.send(f"Role {role.name} has been removed from {member.display_name}.")

    except ValueError:
        await ctx.send("Invalid ID format. Please enter a valid number.")
    except TimeoutError:
        await ctx.send("You took too long to respond.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.command(name='say')
@commands.has_permissions(administrator=True)
async def say(ctx):
    if not check_authorized_role(ctx) or not check_channel(ctx):
        error_embed = discord.Embed(
            title="Error",
            description="You do not have the required role or are in the wrong channel to use this command.",
            color=discord.Color.red()
        )
        await ctx.send(embed=error_embed)
        return
    await ctx.send("Please enter the message you want to send:")
    
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
    
    try:
        msg = await bot.wait_for('message', timeout=60.0, check=check)
        message_content = msg.content
        
        await ctx.send("Should the message be **normal** or **embed**? Please respond with `normal` or `embed`:")
        
        msg_type = await bot.wait_for('message', timeout=60.0, check=check)
        message_type = msg_type.content.lower()
        
        if message_type not in ['normal', 'embed']:
            await ctx.send("Invalid type. Please enter `normal` or `embed`.")
            return
        
        await ctx.send("Please enter the channel ID where you want to send the message:")
        
        msg_channel_id = await bot.wait_for('message', timeout=60.0, check=check)
        channel_id = int(msg_channel_id.content)
        channel = bot.get_channel(channel_id)
        
        if channel:
            try:
                if message_type == 'embed':
                    embed = discord.Embed(
                        description=message_content,
                        color=discord.Color.blue()
                    )
                    await channel.send(embed=embed)
                else:
                    await channel.send(message_content)
                
                confirm_embed = discord.Embed(
                    title="Message Sent",
                    description=f"The message has been sent to {channel.mention}.",
                    color=discord.Color.green()
                )
                await ctx.send(embed=confirm_embed)
            except discord.Forbidden:
                error_embed = discord.Embed(
                    title="Error",
                    description="I don't have permission to send messages in that channel.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=error_embed)
            except Exception as e:
                error_embed = discord.Embed(
                    title="Error",
                    description=f"An unexpected error occurred: {e}",
                    color=discord.Color.red()
                )
                await ctx.send(embed=error_embed)
        else:
            await ctx.send("Channel not found. Please make sure the channel ID is correct.")
    
    except TimeoutError:
        timeout_embed = discord.Embed(
            title="Error",
            description="You took too long to respond.",
            color=discord.Color.red()
        )
        await ctx.send(embed=timeout_embed)

@bot.command()
async def clear(ctx, number: int):
    # تحقق من أن العدد صحيح
    if number < 1 or number > 100:
        embed = discord.Embed(
            title="Error",
            description="The number must be between 1 and 100.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return

    # تحقق من وجود رتبة الإشراف
    authorized_role_id = int(os.getenv("AUTHORIZED_ROLE_ID"))
    user_roles = [role.id for role in ctx.author.roles]

    if authorized_role_id not in user_roles:
        embed = discord.Embed(
            title="Permission Denied",
            description="You do not have the necessary permissions to use this command.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return

    # حذف الرسائل
    deleted = await ctx.channel.purge(limit=number)
    embed = discord.Embed(
        title="Messages Cleared",
        description=f"Successfully deleted {len(deleted)} messages.",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed, delete_after=5)

@bot.command()
async def silence(ctx):
    # تحقق إذا كان المستخدم لديه الدور المطلوب
    if AUTHORIZED_ROLE_ID not in [role.id for role in ctx.author.roles]:
        await ctx.send("You do not have the required role to use this command.")
        return

    # طلب من المستخدم إدخال معرف العضو
    await ctx.send("Please provide the member ID of the person you want to silence.")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        # الانتظار للحصول على رد المستخدم
        member_id_message = await bot.wait_for('message', timeout=60.0, check=check)
        member_id = int(member_id_message.content.strip())
        member = ctx.guild.get_member(member_id)

        if member is None:
            await ctx.send("Invalid member ID. Please provide a valid member ID.")
            return

        # تأكد من أن العضو ليس البوت نفسه
        if member == ctx.guild.me:
            await ctx.send("You cannot silence the bot.")
            return

        # منع العضو من إرسال الرسائل في القناة الحالية
        await ctx.channel.set_permissions(member, send_messages=False)
        
        # إرسال رسالة تأكيد
        embed = discord.Embed(
            title="Silence Applied",
            description=f"{member.mention} has been silenced.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond. The command has been canceled.")
    except ValueError:
        await ctx.send("Invalid input. Please provide a valid member ID.")

@bot.command()
async def unsilence(ctx):
    # تحقق إذا كان المستخدم لديه الدور المطلوب
    if AUTHORIZED_ROLE_ID not in [role.id for role in ctx.author.roles]:
        await ctx.send("You do not have the required role to use this command.")
        return

    # طلب من المستخدم إدخال معرف العضو
    await ctx.send("Please provide the member ID of the person you want to unsilence.")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        # الانتظار للحصول على رد المستخدم
        member_id_message = await bot.wait_for('message', timeout=60.0, check=check)
        member_id = int(member_id_message.content.strip())
        member = ctx.guild.get_member(member_id)

        if member is None:
            await ctx.send("Invalid member ID. Please provide a valid member ID.")
            return

        # تأكد من أن العضو ليس البوت نفسه
        if member == ctx.guild.me:
            await ctx.send("You cannot unsilence the bot.")
            return

        # السماح للعضو بإرسال الرسائل في القناة الحالية
        await ctx.channel.set_permissions(member, send_messages=True)
        
        # إرسال رسالة تأكيد
        embed = discord.Embed(
            title="Silence Lifted",
            description=f"{member.mention} can now send messages again.",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond. The command has been canceled.")
    except ValueError:
        await ctx.send("Invalid input. Please provide a valid member ID.")

@bot.event
async def on_ready():
    try:
        ascii_art_text = text2art("System Team Skoda")
        print(Fore.LIGHTCYAN_EX + ascii_art_text + Style.RESET_ALL)
        print(Fore.LIGHTGREEN_EX + f"Logged in as {bot.user}" + Style.RESET_ALL)
        
        # تعيين الحالة إلى idle واستخدام نوع النشاط Streaming مع رابط Twitch
        await bot.change_presence(
            status=discord.Status.idle,
            activity=discord.Streaming(
                name="System Team Skoda",
                url="https://www.twitch.tv/pisty"
            )
        )
    except Exception as e:
        print(Fore.LIGHTRED_EX + f"Error in on_ready event: {e}" + Style.RESET_ALL)

bot.run(DISCORD_TOKEN)