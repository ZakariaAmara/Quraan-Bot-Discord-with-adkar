Discord Bot for Quraan recitation and Adkar
Overview
This Discord bot provides Quraan recitation and Adkar playback functionality.
Installation Steps
1. Clone the Repository
```
git clone https://github.com/ZakariaAmara/Quraan-Bot-Discord-with-adkar
cd Quraan-Bot-Discord-with-adkar
```


2. Install Dependencies
   
```
pip install -r requirements.txt
```


3. Set Up Your Bot Token
Replace DISCORD_BOT_TOKEN in the .env file with your bot's actual token.
4. Configure the Bot Settings
Modify the following values in your bot's script:
```
selected_voice_channel_id = YOUR_QURAAN_CHANNEL_ID
selected_text_channel_id = YOUR_ADKAR_CHANNEL_ID
audio_url = "https://backup.qurango.net/radio/tarateel"
```


5. Keep-Alive Configuration
The keep_alive.py script ensures your bot stays online while hosted on Render.
6. Run the Bot
Start your bot using:
```
python qu.py
```
If your bot is hosted using Render. Ensure that:
- The keep_alive.py script is running.
- The correct environment variables are set up.
- The required dependencies are installed.
Troubleshooting
If you encounter issues:
- Check Render logs for errors.
- Ensure all dependencies are installed.
- Verify your bot token is correctly set in .env.
