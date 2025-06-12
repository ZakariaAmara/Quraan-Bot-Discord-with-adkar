import discord
from discord.ext import commands
import random
import os
import asyncio
from dotenv import load_dotenv
from discord.ext import tasks
from keep_alive import keep_alive
keep_alive()

# ✅ Load environment variables
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

if TOKEN is None:
    raise ValueError("❌ DISCORD_TOKEN غير موجود في متغيرات البيئة أو ملف .env")

intents = discord.Intents.default()
intents.message_content = True  # Enables message handling
intents.members = True
intents.voice_states = True  # Required for voice state updates

bot = commands.Bot(command_prefix="!", intents=intents)

selected_voice_channel_id = ID FOR QURAAN
selected_text_channel_id = ID FOR ADKAR


@tasks.loop(hours=1)
async def send_adhkar_loop():
    """Automatically sends Adhkar every hour in the selected text channel."""
    if selected_text_channel_id:
        channel = bot.get_channel(selected_text_channel_id)
        if channel:
            await send_adhkar(channel)

@bot.event
async def on_ready():
    print(f"✅ {bot.user} جاهز للعمل!")
    
    if not send_adhkar_loop.is_running():  # Ensure it starts only once
        send_adhkar_loop.start()  # ✅ Starts the loop safely



@bot.command()
async def تحديد_القناة_الصوتية(ctx, channel: discord.VoiceChannel):
    global selected_voice_channel_id
    selected_voice_channel_id = channel.id
    await ctx.send(f"🔊 سيتم تشغيل القرآن في **{channel.name}**.")

@bot.command()
async def تحديد_القناة_النصية(ctx, channel: discord.TextChannel):
    global selected_text_channel_id
    selected_text_channel_id = channel.id
    await ctx.send(f"📝 سيتم إرسال الأذكار في **{channel.name}**.")

async def connect_to_voice(channel):
    """Attempts to connect to the voice channel, with retry handling."""
    for attempt in range(3):  # Retry up to 3 times
        try:
            vc = await channel.connect()
            return vc
        except Exception as e:
            print(f"Voice connection failed (attempt {attempt + 1}): {e}")
            await asyncio.sleep(5)  # Wait before retrying
    return None

@bot.event
async def on_voice_state_update(member, before, after):
    """Handles bot voice connections and ensures smooth operation."""
    if after.channel and selected_voice_channel_id == after.channel.id:
        guild = after.channel.guild
        if not guild.voice_client:
            vc = await connect_to_voice(after.channel)  
            if vc:
                await play_quran(vc)

                if selected_text_channel_id:
                    channel = bot.get_channel(selected_text_channel_id)
                    await send_adhkar(channel)

    # Ensure bot disconnects if left alone in voice channel
    if before.channel and before.channel.guild.voice_client:
        vc = before.channel.guild.voice_client
        if vc and len(vc.channel.members) == 1:
            await vc.disconnect()

async def play_quran(vc):
    """Streams Quran recitation in the voice channel."""
    if vc.is_playing():
        return  # Avoid interruptions

    audio_url = "https://backup.qurango.net/radio/tarateel"  # Direct MP3 stream
    vc.play(discord.FFmpegPCMAudio(audio_url))
    print(f"🔊 يتم تشغيل: {audio_url}")

async def send_adhkar(channel):
    """Sends a random Arabic Adhkar to the selected text channel."""
    adhkar_list = [
        "✨ سبحان الله والحمد لله ولا إله إلا الله والله أكبر ✨",
        "☀️ اللهم اجعل هذا اليوم مباركًا، واكتب لنا فيه الخير ☀️",
        "💖 أستغفر الله الذي لا إله إلا هو الحي القيوم وأتوب إليه 💖",
        "🌙 اللهم إني أسألك الجنة وأعوذ بك من النار 🌙",
        "🙏 لا حول ولا قوة إلا بالله العلي العظيم 🙏",
        "🤲 اللهم ارزقني الإخلاص في القول والعمل 🤲",
"اللَّهُمَّ أنَْتَ رَبيِّ لَا إلِهََ إلَِّا أنَتَ، خَلَقْتنَيِ وَأنََا عَبدُْكَ، وَأنََا عَلَى عَهْدِكَ وَوَعْدِكَ مَا اسْتَطَعْتُ، أَعُوذُ بِكَ مِنْ شَرِّ مَا صَنَعْتُ، أَبُوءُ لَكَ بِنِعْمَتِكَ عَلَيَّ، وَأَبُوءُ بِذَنْبِي فَاغْفِرْ لِي فَإِنَّهُ لَا يَغْفِرُ الذُّنُوبَ إِلَّا أَنْتَ. ",
"اللَّهُمَّ إِنِّي ظَلَمْتُ نَفْسِي ظُلْمًا كَثِيرًا، وَلَا يَغْفِرُ الذُّنُوبَ إِلَّا أَنْتَ، فَاغْفِرْ لِي مَغْفِرَةً مِنْ عِنْدِكَ وَارْحَمْنِي إِنَّك أَنْتَ الْغَفُورُ الرَّحِيمُ. ",
"رَبِّ اغْفِرْ لِي خَطِيئَتِي وَجَهْلِي وَإِسْرَافِي فِي أَمْرِي كُلِّهِ وَمَا أَنْتَ أَعْلَمُ بِهِ مِنِّي، اللَّهُمَّ اغْفِرْ لِي خَطَايَايَ وَعَمْدِي وَجَهْلِي وَهَزْلِي، وَكُلُّ ذَلِكَ عِنْدِي، اللَّهُمَّ اغْفِرْ لِي مَا قَدَّمْتُ وَمَا أَخَّرْتُ وَمَا أَسْرَرْتُ وَمَا أَعْلَنْتُ أَنْتَ الْمُقَدِّمُ وَأَنْتَ الْمُؤَخِّرُ وَأَنْتَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ. ",
"اللَّهُمَّ اغْفِرْ لِي ذَنْبِي كُلَّهُ، دِقَّهُ، وَجِلَّهُ، وَأَوَّلَهُ، وَآخِرَهُ، وَعَلَانِيَتَهُ، وَسِرَّهُ. ",
"اللَّهُمَّ إِنِّي أَعُوذُ بِكَ مِنَ الْهَمِّ وَالْحَزَنِ وَالْعَجْزِ وَالْكَسَلِ وَالْجُبْنِ وَالْبُخْلِ وَضَلَعِ الدَّيْنِ وَغَلَبَةِ الرِّجَالِ. ",
"استغفر الله",
"الحمد لله",
"لا اله الا الله",
"الله اكبر",
"سبحان الله",
    ]

    adhkar_message = random.choice(adhkar_list)
    role = discord.utils.get(channel.guild.roles, name="d")  # Make sure this role name exists!

    if role:
        await channel.send(f"{role.mention}\n📿 **ذكر اليوم:**\n{adhkar_message}")
    else:
        await channel.send(f"📿 **ذكر اليوم:**\n{adhkar_message}")

# ✅ Run the bot
bot.run(TOKEN)
