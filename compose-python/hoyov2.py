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
logger_config['handlers']['fileHandler']['filename'] = '/media/console.log'
logger_config['handlers']['discord'] = {}
logger_config['handlers']['discord']['class'] = 'logging.FileHandler'
logger_config['handlers']['discord']['level'] = 'DEBUG'
logger_config['handlers']['discord']['formatter'] = 'simple'
logger_config['handlers']['discord']['filename'] = '/media/console.log'
logger_config['handlers']['discord.http'] = {}
logger_config['handlers']['discord.http']['class'] = 'logging.FileHandler'
logger_config['handlers']['discord.http']['level'] = 'DEBUG'
logger_config['handlers']['discord.http']['formatter'] = 'simple'
logger_config['handlers']['discord.http']['filename'] = '/media/console.log'
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

import subprocess
import sys
import os
import json
import pathlib

def python_install_package(package_name):
    # 現在実行中のPython環境と同じ環境にインストールする
    logger.info(f'Installing package: {package_name}')
    subprocess.check_call([
        sys.executable,
        '-m',
        'pip',
        'install',
        '--upgrade',
        package_name
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def restart_program():
    # Pythonプログラム自身を再起動する
    python = sys.executable
    logger.warning(f'Restarting {python} {sys.argv}\n')
    os.execv(python, [python] + sys.argv)

try:
    logger.info(f'Library check: pip')
    python_install_package('pip')
except Exception as e:
    print(e)
    sys.exit(1)
try:
    logger.info(f'Library check: discord')
    import discord
except ModuleNotFoundError as e:
    logger.error(f'{e.msg}')
    python_install_package('discord')
    restart_program()
try:
    logger.info(f'Library check: dotenv')
    import dotenv
except ModuleNotFoundError as e:
    logger.error(f'{e.msg}')
    python_install_package('python-dotenv')
    restart_program()

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.typing = True
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

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

@tree.command(name="help",description="コマンドヘルプを表示します。")
async def help(interaction: discord.Interaction):
    embed = discord.Embed(
        title='Help',
        description='コマンドヘルプ',
        color=0x333333,
        timestamp=datetime.datetime.now(datetime.timezone.utc),
    )
    await interaction.response.send_message(embed=embed,ephemeral=True)#ephemeral=True→「これらはあなただけに表示されています」


if __name__ == '__main__':
    filepath = pathlib.Path(__file__).resolve().parent / '.tmp'
    if os.path.isfile(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            print(f.read())
    else:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('0')
    
    logger.info('Boot')
    dotenv.load_dotenv()
    TOKEN_DISCORD=os.environ.get('TOKEN_DISCORD')
    if TOKEN_DISCORD is None:
        raise ValueError('Require the TOKEN_DISCORD')

    logger.info(f'TOKEN_DISCORD: {TOKEN_DISCORD}')

    logger.info('Connecting to Discord API')
    try:
        client.run(TOKEN_DISCORD)
    except discord.errors.PrivilegedIntentsRequired as e:
        logger.error(str(e))
        sys.exit(3)


