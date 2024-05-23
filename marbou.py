import discord
import os
import asyncio
import yt_dlp
import random
from dotenv import load_dotenv
from discord.ext import commands, tasks

def run_bot():
    load_dotenv()
    TOKEN = os.getenv('discord_token')
    GENERAL_TEXT_CHANNEL = 609841336547410046
    CYTATY_TEXT_CHANNEL = 1014167636306829332
    TEST_BOT_TEXT_CHANNEL = 1242091992750620672
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    queues = {}
    voice_clients = {}
    yt_dl_options = {"format": "bestaudio/best"}
    ytdl = yt_dlp.YoutubeDL(yt_dl_options)

    ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn -filter:a "volume=0.25"'}

    @client.event
    async def on_ready():
        print(f'{client.user} is GOLD')
        random_quote.start()

    async def play_next(message):
        if queues[message.guild.id] != []:
            link = queues[message.guild.id].pop(0)
            target_channel = message.channel
            await target_channel.send(f'Ej Bartek zaśpiewaj {link}')

    
    @client.event
    async def on_message(message):
        if message.content.startswith("Ej Bartek zaśpiewaj"):
            try:
                voice_client = await message.author.voice.channel.connect()
                voice_clients[voice_client.guild.id] = voice_client
            except Exception as e:
                print(e)

            try:
                url = message.content.split()[3]

                loop = asyncio.get_event_loop()
                data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

                song = data['url']
                player = discord.FFmpegOpusAudio(song, **ffmpeg_options)

                voice_clients[message.guild.id].play(player, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(message), client.loop))
            except Exception as e:
                print(e)

        if message.content.startswith("przerwa na 🍻") or message.content.startswith("przerwa na 🍺") or message.content.startswith("przerwa na piwko"):
            try:
                voice_client = await message.author.voice.channel.connect()
                voice_clients[voice_client.guild.id] = voice_client
            except Exception as e:
                print(e)
            try:
                voice_clients[message.guild.id].stop()
                source = discord.FFmpegPCMAudio("beer.mp3")
                voice_clients[message.guild.id].play(source)
            except Exception as e:
                print (e)
            
        if message.content.startswith("po przerwie"):
            try:
                voice_clients[message.guild.id].resume()
            except Exception as e:
                print(e)
        if message.content.startswith("szybki łyczek 🥃") or message.content.startswith("szybki łyczek whiskey") or message.content.startswith("🥃"):
            try:
                voice_clients[message.guild.id].pause()
            except Exception as e:
                print(e)
        
        if message.content.startswith("status"):
            try:
                voice_client = await message.author.voice.channel.connect()
                voice_clients[voice_client.guild.id] = voice_client
            except Exception as e:
                print(e)
            try:
                voice_clients[message.guild.id].stop()
                source = discord.FFmpegPCMAudio("pelne_check.mp3")
                voice_clients[message.guild.id].play(source)
            except Exception as e:
                print (e)

        if message.content.startswith("potem zaśpiewaj"):
            url = message.content.split()[2]
            if message.guild.id not in queues:
                queues[message.guild.id] = []
            queues[message.guild.id].append(url)
            target_channel = message.channel
            await target_channel.send("dodano do kolejki kowboju EEEEEHAAAAA!")
    
        if message.content.startswith("marbou help"):
            target_channel = client.get_channel(message.channel.id)
            await target_channel.send("Ej Bartek zaśpiewaj <youtube URL>        odpala muzykę z podanego linku z YT\n"\
                                      "przerwa na piwko         marbou idzie na piwko i przerywa koncert\n"\
                                      "szybki łyczek whiskey        marbou bierze szybkiego łyczka złotego trunku\n"\
                                      "po przerwie      przywłuje marbou żeby grał dalej\n"\
                                      "status       podaje aktualny status poziomu płynu w kuflu")
            
    @tasks.loop(hours=24)
    async def random_quote():
        random_seconds = random.randint(0, 86400)
        await asyncio.sleep(random_seconds)
        print(f'task loop działa +{random_seconds}s')
        source_channel = client.get_channel(CYTATY_TEXT_CHANNEL)
        target_channel = client.get_channel(GENERAL_TEXT_CHANNEL)
        if source_channel and target_channel:
            messages = []
            async for message in source_channel.history(limit=200):
                if message.content.startswith("\""):
                    messages.append(message)

            if messages:
                random_message = random.choice(messages)
                if random_message.content:
                    sent_message = await target_channel.send(f'Error: O nie ktoś rozlał piwko na serwery!!!\n Wyciek danych...\n{random_message.content}')
                else:
                    await target_channel.send("\"Załóż czapke\" - Marbou bot")
                await asyncio.sleep(60)
                #delete sent message
                await sent_message.delete()

    @random_quote.before_loop
    async def before_random_quote():
        print("czekam")
        await client.wait_until_ready()
    client.run(TOKEN)