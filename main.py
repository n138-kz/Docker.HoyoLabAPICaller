from logging import getLogger,config as logging_conf
logger_config = {}
logger_config['version'] = 1
logger_config['disable_existing_loggers'] = False
logger_config['formatters'] = {}
logger_config['formatters']['simple'] = {}
logger_config['formatters']['simple']['format'] = '%(asctime)s %(name)s:%(lineno)s %(funcName)s [%(levelname)s]: %(message)s'
logger_config['formatters']['simple']['format'] = '%(asctime)s %(levelname)s: %(message)s'
logger_config['handlers'] = {}
logger_config['handlers']['consoleHandler'] = {}
logger_config['handlers']['consoleHandler']['class'] = 'logging.StreamHandler'
logger_config['handlers']['consoleHandler']['level'] = 'INFO'
logger_config['handlers']['consoleHandler']['formatter'] = 'simple'
logger_config['handlers']['consoleHandler']['stream'] = 'ext://sys.stdout'
logger_config['handlers']['fileHandler'] = {}
logger_config['handlers']['fileHandler']['class'] = 'logging.FileHandler'
logger_config['handlers']['fileHandler']['level'] = 'DEBUG'
logger_config['handlers']['fileHandler']['formatter'] = 'simple'
logger_config['handlers']['fileHandler']['filename'] = '/log/custom/console.log'
logger_config['handlers']['discord'] = {}
logger_config['handlers']['discord']['class'] = 'logging.FileHandler'
logger_config['handlers']['discord']['level'] = 'DEBUG'
logger_config['handlers']['discord']['formatter'] = 'simple'
logger_config['handlers']['discord']['filename'] = '/log/custom/console.log'
logger_config['handlers']['discord.http'] = {}
logger_config['handlers']['discord.http']['class'] = 'logging.FileHandler'
logger_config['handlers']['discord.http']['level'] = 'DEBUG'
logger_config['handlers']['discord.http']['formatter'] = 'simple'
logger_config['handlers']['discord.http']['filename'] = '/log/custom/console.log'
logger_config['loggers'] = {}
logger_config['loggers']['__main__'] = {}
logger_config['loggers']['__main__']['level'] = 'DEBUG'
logger_config['loggers']['__main__']['handlers'] = ['consoleHandler', 'fileHandler']
logger_config['loggers']['__main__']['propagate'] = False
logger_config['loggers']['same_hierarchy'] = {}
logger_config['loggers']['same_hierarchy']['level'] = 'DEBUG'
logger_config['loggers']['same_hierarchy']['handlers'] = ['consoleHandler', 'fileHandler']
logger_config['loggers']['same_hierarchy']['propagate'] = False
logger_config['loggers']['lower.sub'] = {}
logger_config['loggers']['lower.sub']['level'] = 'DEBUG'
logger_config['loggers']['lower.sub']['handlers'] = ['consoleHandler', 'fileHandler']
logger_config['loggers']['lower.sub']['propagate'] = False
logger_config['root'] = {}
logger_config['root']['level'] = 'INFO'
logging_conf.dictConfig(logger_config)
logger = getLogger(__name__)
logger.info('Init')

import os,sys
import hashlib
import traceback
import discord
import json
import datetime
import math
from dotenv import load_dotenv

load_dotenv()
TOKEN_DISCORD=os.environ['TOKEN_DISCORD']
if len(TOKEN_DISCORD) > 0:
    logger.info('Load & set the token DISCORD {}'.format(
        hashlib.sha1(
            hashlib.sha1(TOKEN_DISCORD.encode()).hexdigest()[0:7],
            hashlib.sha1(TOKEN_DISCORD.encode()).hexdigest()[-7:],
        ).hexdigest()[0:7]
    ))
else:
    raise ValueError('Require the token.discord')

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.typing = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    logger.info('Connect OK id:{0}'.format(client.user.id))
    logger.info('Invite link: https://discord.com/oauth2/authorize?client_id={}'.format(client.user.id))

    await client.change_presence(
        status=discord.Status.online,
        activity=discord.CustomActivity(name=client.user.name)
    )
    logger.info('Change presence to {}'.format(discord.Status.online))

    # 起動完了
    logger.info('Ready')

@client.event
async def on_connect():
    logger.info('Connected')

@client.event
async def on_disconnect():
    logger.warning('Disconnected')

@client.event
async def on_resumed():
    logger.info('resumed')

@client.event
async def on_error(event, args, kwargs):
    logger.error('on_error: {}'.format(
        event,
    ))
    logger.error(sys.exc_info())

@client.event
async def on_typing(channel, user, when):
    logger.info('on_typing: channel:{} user:{} when:{}'.format(
        channel.id,
        user.id,
        when,
    ))

@client.event
async def on_message_delete(message):
    logger.info('on_message_delete')

@client.event
async def on_bulk_message_delete(message):
    logger.info('on_bulk_message_delete')

@client.event
async def on_message_edit(before, after):
    # 送信者が自分自身である場合は弾く
    if after.author.id == client.user.id:
        return
    # 送信者がbotである場合は弾く
    if after.author.bot:
        logger.warning('Message author is BOT: {}({})'.format(
            after.author.name,
            after.author.id,
        ))
        return
    # テキストチャンネルのみ処理
    if after.channel.type != discord.ChannelType.text:
        logger.warning('Channel type is not text channel')
        return
    # メッセージ受取り
    logger.info('on_message_edit author: {}({}) guild:{} channel:{}'.format(
        after.author.name,
        after.author.id,
        after.guild.id,
        after.channel.id,
    ))
    logger.debug('on_message_edit author: {}({}) guild:{}({}) channel:{}({}) content:{}'.format(
        after.author.name,
        after.author.id,
        after.guild.id,
        after.guild.name,
        after.channel.id,
        after.channel.name,
        after.content,
    ))

@client.event
async def on_message(message):
    # 変数初期化
    timeu=datetime.datetime.now(datetime.timezone.utc)
    title=None
    descr=None
    color=0x000000
    color_custom={
        'success': 0x00FF00,
        'failure': 0xFF0000,
    }
    url=None
    text=None

    # 送信者が自分自身である場合は弾く
    if message.author.id == client.user.id:
        return
    # 送信者がbotである場合は弾く
    if message.author.bot:
        logger.warning('Message author is BOT: {}({})'.format(
            message.author.name,
            message.author.id,
        ))
        return
    # テキストチャンネルのみ処理
    if message.channel.type != discord.ChannelType.text:
        logger.warning('Channel type is not text channel')
        return

# botを起動
def main():
    logger.info('Connecting to Discord API')
    try:
        client.run(TOKEN_DISCORD)
    except discord.errors.PrivilegedIntentsRequired:
        logger.error(traceback.format_exc())
        sys.exit(1)

logger.info(__name__)
if __name__ == '__main__':
    main()
