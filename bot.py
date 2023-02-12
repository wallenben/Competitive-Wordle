import discord
from discord.ext import commands
import re
import asyncio
from datetime import datetime
import time

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

now = datetime.now()

channel = bot.get_channel('id')


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await channel.edit(topic="HIGH SCORE: undefined 6/6")


@bot.event
async def on_message(message):
    if now.hour == 23 and now.minute == 59 or message.content == '!reset':
        try:
            await channel.edit(topic='HIGH SCORE: undefined 6/6')
        except discord.errors.HTTPException as ex:
            if ex.status == 429:
                retry_after = ex.retry_after
                print(
                    "[ERROR] Too Many Requests, retrying after %d seconds." % retry_after)
                time.sleep(retry_after)
                await channel.edit(topic='HIGH SCORE: undefined 6/6')
    if message.channel.name == 'wordle':
        pattern = re.compile(
            r'(Scoredle|Wordle)\s(\d+|X|x)\s?(\d)?\/(\d)\*?\n?\n(\d+,\d+)?(\n[⬛🟩🟨]+\s(\d+)|\n[⬛🟩🟨]+){1,6}')
        match = re.match(pattern, message.content)
        if match:
            numerator = int(match.group(2))
            denominator = 6
            current_topic = message.channel.topic
            score_match = re.search(r'(\d+)/(\d+)', current_topic)
            if score_match:
                current_numerator = int(score_match.group(1))
                if numerator < current_numerator:
                    try:
                        await message.channel.edit(topic=f'HIGH SCORE: {message.author} {numerator}/{denominator}')
                    except discord.errors.HTTPException as ex:
                        if ex.status == 429:
                            retry_after = ex.retry_after
                            print(
                                "[ERROR] Too Many Requests, retrying after %d seconds." % retry_after)
                            time.sleep(retry_after)
                            await message.channel.edit(topic=f'HIGH SCORE: {message.author} {numerator}/{denominator}')
# Replace <token> with your Discord bot token
bot.run('token')
