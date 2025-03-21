import discord
import webserver
import os
import asyncio
import yt_dlp
import random
import requests
from pyht import Client
from PIL import Image, ImageDraw, ImageFont
from pyht.client import TTSOptions
from dotenv import load_dotenv
from discord.ext import tasks, commands

def run_bot():
    load_dotenv()
    TOKEN = os.getenv('discord_token')
    GENERAL_TEXT_CHANNEL = 609841336547410046
    CYTATY_TEXT_CHANNEL = 1014167636306829332
    TEST_BOT_TEXT_CHANNEL = 1242091992750620672
    NOT_MESSAGE = 1122278853562343565

    #PYHT_ID = os.getenv('pyht_id')
    #PYHT_KEY = os.getenv('pyht_key')
    #pyht_client = Client(
    #    user_id=PYHT_ID,
    #   api_key=PYHT_KEY,
    #)
    #pyht_options = TTSOptions(voice="s3://voice-cloning-zero-shot/abc2d0e6-9433-4dcc-b416-0b035169f37e/original/manifest.json")

    KOSTYKA_ID = 214659041706770432
    NORMIE_BE_LIKE_ID = 444953338631421953
    VENGEFUL1_ID = 428594821351997440
    OLIWIUU_ID = 531173644102139915
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)

    ANIME_URL = "https://api.animethemes.moe/video/"

    queues = {}
    voice_clients = {}
    yt_dl_options = {"format": "bestaudio/best"}
    ytdl = yt_dlp.YoutubeDL(yt_dl_options)

    ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn -filter:a "volume=0.25"'}

    async def play_audio(ctx, url):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            vc = await channel.connect()

            vc.play(discord.FFmpegPCMAudio(url))
            return vc
        else:
            await ctx.send("You need to be in a voice channel to start the contest!")
            return None

    @bot.event
    async def on_ready():
        print(f'{bot.user} is GOLD')
        random_quote.start()

    async def play_next(message):
        if queues[message.guild.id] != []:
            link = queues[message.guild.id].pop(0)
            target_channel = message.channel
            await target_channel.send(f'Ej Bartek zaśpiewaj {link}')

    
    @bot.event
    async def on_message(message):
        '''
        if message.channel.id == CYTATY_TEXT_CHANNEL and not message.author.bot:
            user = await bot.fetch_user(OLIWIUU_ID)
            user.send("```"
                      ""
            "```")'
        '''
        if message.content.startswith("Ej Bartek zaśpiewaj"):
            chuj_moment = random.randint(1, 10)
            if message.author.id == KOSTYKA_ID and chuj_moment == 10:
                target_channel = message.channel
                await target_channel.send("Sam zaśpiewaj Bartek")
            else:
                try:
                    voice_client = await message.author.voice.channel.connect()
                    voice_clients[voice_client.guild.id] = voice_client
                except Exception as e:
                    print(e)

                try:
                    if message.author.id == NORMIE_BE_LIKE_ID and chuj_moment > 9:
                        url = "https://www.youtube.com/watch?v=ytWz0qVvBZ0&ab_channel=TheYogscast"
                    else:
                        url = message.content.split()[3]

                    loop = asyncio.get_event_loop()
                    data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
                    song = data['url']
                    player = discord.FFmpegOpusAudio(song, **ffmpeg_options)
                    voice_clients[message.guild.id].play(player, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(message), bot.loop))
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
                source = discord.FFmpegPCMAudio("assets/beer.mp3")
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
                source = discord.FFmpegPCMAudio("assets/pelne_check.mp3")
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
            target_channel = bot.get_channel(message.channel.id)
            await target_channel.send("```Ej Bartek zaśpiewaj <youtube URL>     odpala muzykę z podanego linku z YT\n"\
                                      "przerwa na piwko                 marbou idzie na piwko i przerywa koncert\n"\
                                      "szybki łyczek whiskey       marbou bierze szybkiego łyczka złotego trunku\n"\
                                      "po przerwie                              przywłuje marbou żeby grał dalej\n"\
                                      "status                       podaje aktualny status poziomu płynu w kuflu\n"\
                                      "potem zaśpiewaj <youtube URL>             Dodaje do kolejki utwór z linku```")
    
    @bot.event
    async def on_voice_state_update(member, before, after):
        if before.channel and not after.channel:
            voice_client = discord.utils.get(bot.voice_clients, guild=before.channel.guild)
            if voice_client and len(voice_client.channel.members) == 1:  # Only bot left
                await voice_client.disconnect()

    polish_to_universal = str.maketrans(
        'ąćęłńóśźżĄĆĘŁŃÓŚŹŻ',
        'acelnoszzACELNOSZZ'
    )

    def insert_newlines_at_whitespace(text, interval):
        lines = text.split('\n')
        
        def split_line_at_whitespace(line, interval):
            words = line.split()
            result = []
            current_line = []

            for word in words:
                if len(' '.join(current_line + [word])) > interval:
                    result.append(' '.join(current_line))
                    current_line = [word]
                else:
                    current_line.append(word)
            
            if current_line:
                result.append(' '.join(current_line))
            
            return '\n'.join(result)
    
        processed_lines = [split_line_at_whitespace(line, interval) for line in lines]
        
        return '\n'.join(processed_lines)

    @tasks.loop(hours=24)
    async def random_quote():
        random_seconds = random.randint(0, 86400)
        await asyncio.sleep(random_seconds)
        print(f'task loop działa +{random_seconds}s')
        source_channel = bot.get_channel(CYTATY_TEXT_CHANNEL)
        target_channel = bot.get_channel(GENERAL_TEXT_CHANNEL)
        if source_channel and target_channel:
            messages = []
            async for message in source_channel.history(limit=1000):
                if message.content.startswith("\"") or message.content.startswith(",,") and not message.id == NOT_MESSAGE:
                    messages.append(message)

            if messages:
                random_message = random.choice(messages)
                if random_message.content:
                    original_gif = Image.open("assets/piwko.gif")
                    temp_gif_path = "SPOILER_temp_gif.gif"
                    frames = []
                    try:
                        while True:
                            frame = original_gif.copy()
                            frames.append(frame)
                            original_gif.seek(len(frames))
                    except EOFError:
                        pass

                    font_path = "assets/GlitchGoblin-2O87v.ttf"
                    font = ImageFont.truetype(font_path,30)
                    text_pos = (20, 20) #5 370
                    text_to_add = random_message.content
                    text_to_add = insert_newlines_at_whitespace(random_message.content,65)
                    text_to_add = text_to_add.translate(polish_to_universal)
                    new_frames = []
                    for frame in frames:
                        draw = ImageDraw.Draw(frame)
                        draw.text(text_pos,text_to_add, font=font, fill="black")
                        new_frames.append(frame)
                    new_frames[0].save(temp_gif_path,save_all=True,append_images=new_frames[1:],loop=0)
                    with open(temp_gif_path,"rb") as f:
                        picture = discord.File(f)
                        sent_message = await target_channel.send(file=picture)
                else:
                    await target_channel.send("\"Załóż czapke\" - Marbou bot")
                await asyncio.sleep(60)
                await sent_message.delete()

    @random_quote.before_loop
    async def before_random_quote():
        await bot.wait_until_ready()

    #webserver.keep_alive() # if on render

    bot.run(TOKEN)