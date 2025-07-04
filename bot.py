import os
import discord
import requests
from discord.ext import commands

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def card(ctx, *, query: str):
    url = f"https://api.scryfall.com/cards/named?fuzzy={query}"
    response = requests.get(url)

    if response.status_code != 200:
        await ctx.send(f"❌ Could not find a card for `{query}`.")
        return

    data = response.json()
    name = data.get("name", "Unknown")
    type_line = data.get("type_line", "No type")
    oracle_text = data.get("oracle_text", "No rules text")
    image_url = data.get("image_uris", {}).get("normal")

    embed = discord.Embed(title=name, description=type_line, color=0x00ff99)
    embed.add_field(name="Rules Text", value=oracle_text, inline=False)

    if image_url:
        embed.set_image(url=image_url)

    await ctx.send(embed=embed)

bot.run(TOKEN)
