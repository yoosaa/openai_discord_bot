import discord
import openai
from dotenv import dotenv_values
CONFIG = dotenv_values('.env')

# インテントの生成
intents = discord.Intents.default()
intents.message_content = True

# クライアントの生成
client = discord.Client(intents=intents)

# discordと接続した時に呼ばれる
@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')

# メッセージを受信した時に呼ばれる
@client.event
async def on_message(message):
  # 自分のメッセージを無効に
  if message.author == client.user:
    return

  # botにメンションしたら
  if bool(message.mentions) and message.mentions[0].name == CONFIG['DISCORD_BOT_NAME']:
    # メッセージがない or ある
    if len(message.content) <= 22:
      await message.channel.send('何か御用でしょうか？')
    else:
      openai.api_key = CONFIG['OPENAI_TOKEN']
      # api通信
      res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
          {"role": "user", "content": str(message.content)}
        ]
      )
      completion = res["choices"][0]["message"]["content"]
      await message.channel.send(completion)

client.run(CONFIG['DISCORD_TOKEN'])
