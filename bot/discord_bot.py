import os
import discord
import asyncio
from discord.ext import commands
from db import init_db, add_ticket, search_tickets

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    # Initialize DB on startup
    await init_db()

@bot.command(name='add')
async def cmd_add(ctx, *, content: str):
    # Dummy embedding: replace with real model output
    embedding = [0.0] * 1536
    await add_ticket(content, embedding)
    await ctx.send('Ticket added.')

@bot.command(name='search')
async def cmd_search(ctx, *, query: str):
    # Dummy query vector: replace with model embed
    query_vec = [0.0] * 1536
    results = await search_tickets(query_vec)
    if not results:
        await ctx.send('No matches.')
    else:
        msg = '\n'.join(f"ID {r['id']}: {r['content']}" for r in results)
        await ctx.send(f'Results:\n{msg}')

if __name__ == '__main__':
    TOKEN = os.getenv('DISCORD_TOKEN')
    bot.run(TOKEN)
