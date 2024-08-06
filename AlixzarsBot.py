import discord
from discord.ext import commands
import os
import requests
import asyncio
import webserver

intents = discord.Intents.default()
intents.message_content = True  # Enable reading message content
intents.members = True  # Enable member join/leave events
client = commands.Bot(command_prefix='!', intents=intents)


@client.event
async def on_message(message):
    """
    Listens to all messages and processes the !convert command.
    """
    if message.author == client.user:
        return  # Ignore messages from the bot itself

    # Check for the !convert command
    if message.content.startswith('!convert'):
        if message.author.guild_permissions.administrator:  # Check for admin permissions
            url = message.content.split(' ')[1]  # Extract the URL
            print(f"Received URL: {url}")
            if "githubusercontent.com" in url or "pastebin.com" in url:
                print("URL is valid")
                loadstring_command = f"loadstring(game:HttpGet('{url}'))"
                print(f"Loadstring command: {loadstring_command}")
                await message.channel.send(loadstring_command)
            else:
                print("URL is invalid")
                await message.channel.send(
                    "Invalid URL: Please provide a valid GitHub or Pastebin URL."
                )
        else:
            await message.channel.send(
                "You do not have permission to use this command.")


@client.event
async def on_member_join(member):
    """
    Sends a welcome message when a new member joins the server.
    """
    guild = member.guild
    welcome_channel_id = 1267939055220293663  # Replace with your welcome channel ID
    welcome_channel = client.get_channel(welcome_channel_id)
    if welcome_channel:
        member_count = guild.member_count
        embed = discord.Embed(
            title=f"Welcome to the server, {member.name}!",
            description=
            f"We now have {member_count} members. Please take a moment to read the rules.",
            color=discord.Color.blue())
        if member.avatar:  # Check if member has an avatar
            embed.set_thumbnail(
                url=member.avatar.url)  # Add member profile picture
        embed.set_footer(
            text="Made by Alixzar",
            icon_url=
            "https://cdn.discordapp.com/avatars/913734466768338964/19e359ddd80cd0cbd07fa9e05ccb173e.png?size=2048"
        )  # Add footer message
        await welcome_channel.send(embed=embed)  # Send the embed
    else:
        print("Welcome channel not found")


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')


webserver.keep_alive()
client.run(os.environ["DISCORD_BOT_TOKEN"])
