import os
import discord
import requests
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

BLOCKED_USERS = {
    144307117950631936: "STAY OUTTA FLAVORTOWN",
}

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
print("Loaded token:", TOKEN[:8] + "..." if TOKEN else "No token found")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)
intents.message_content = True

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.check
async def block_users_globally(ctx):
    if ctx.author.id in BLOCKED_USERS:
        reason = BLOCKED_USERS[ctx.author.id]
        await ctx.send(f"🚫 Sorry {ctx.author.display_name}, you can't use this bot. Reason: I could care less.")
        return False
    return True

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

@bot.command()
async def roll(ctx, sides: int = 20):
    import random
    if sides < 2:
        await ctx.send("🎲 Minimum sides is 2.")
    else:
        result = random.randint(1, sides)
        await ctx.send(f"🎲 You rolled a {result} on a d{sides}.")

@bot.command()
async def price(ctx, *, query: str):
    url = f"https://api.scryfall.com/cards/named?fuzzy={query}"
    response = requests.get(url)

    if response.status_code != 200:
        await ctx.send(f"❌ Could not find `{query}`.")
        return

    data = response.json()
    price = data.get("prices", {}).get("usd")
    foil_price = data.get("prices", {}).get("usd_foil")
    name = data.get("name")

    msg = f"💵 **{name}** price:\n"
    msg += f"• Normal: ${price if price else 'N/A'}\n"
    msg += f"• Foil: ${foil_price if foil_price else 'N/A'}"
    await ctx.send(msg)

bot.run(TOKEN)
