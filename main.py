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
  completion = await handleMessage(message)
  if not completion:
    return
  else:
    await message.channel.send(completion)

client.run(CONFIG['DISCORD_TOKEN'])


async def handleMessage(msg):
  # 自分のメッセージを無効に
  if msg.author == client.user:
    return False

  # botにメンションしたら
  if bool(msg.mentions) and msg.mentions[0].name == CONFIG['DISCORD_BOT_NAME']:
    # メッセージがない or ある
    if len(msg.content) <= 22:
      return '何か御用でしょうか？'
    else:
      openai.api_key = CONFIG['OPENAI_TOKEN']
      # api通信
      res = await openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
          {"role": "user", "content": str(msg.content)}
        ]
      )
      return res["choices"][0]["message"]["content"]
