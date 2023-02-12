import discord
from discord.ext import commands
import re
import asyncio
from datetime import datetime
import time

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    channel = bot.get_channel('<channel_id>')

    await channel.edit(topic="HIGH SCORE: undefined 6/6")
    while True:
        now = datetime.now()
        if now.hour == 23 and now.minute == 59:
            try:
                await channel.edit(topic='HIGH SCORE: undefined 6/6')
            except discord.errors.HTTPException as ex:
                if ex.status == 429:
                    retry_after = ex.retry_after
                    print(
                        "[ERROR] Too Many Requests, retrying after %d seconds." % retry_after)
                    time.sleep(retry_after)
                    await channel.edit(topic='HIGH SCORE: undefined 6/6')
        await asyncio.sleep(60)


@bot.event
async def on_message(message):
    if message.channel.name == 'wordle':
        fraction_match = re.search(r'(\d+)/(\d+)', message.content)
        if fraction_match:
            numerator = int(fraction_match.group(1))
            denominator = int(fraction_match.group(2))
            current_topic = message.channel.topic
            score_match = re.search(r'(\d+)/(\d+)', current_topic)
            if score_match:
                current_numerator = int(score_match.group(1))
                current_denominator = int(score_match.group(2))
                if numerator / denominator < current_numerator / current_denominator:
                    try:
                        await message.channel.edit(topic=f'HIGH SCORE: {message.author} {numerator}/{denominator}')
                    except discord.errors.HTTPException as ex:
                        if ex.status == 429:
                            retry_after = ex.retry_after
                            print(
                                "[ERROR] Too Many Requests, retrying after %d seconds." % retry_after)
                            time.sleep(retry_after)
                            await message.channel.edit(topic=f'HIGH SCORE: {message.author} {numerator}/{denominator}')
bot.run('<token>')
