import subprocess
import sys
import os

def python_install_package(package_name):
    # 現在実行中のPython環境と同じ環境にインストールする
    subprocess.check_call([
        sys.executable,
        '-m',
        'pip',
        'install',
        '--upgrade',
        package_name
    ])

def restart_program():
    # Pythonプログラム自身を再起動する
    python = sys.executable
    print(f'Restarting {python} {sys.argv}\n')
    os.execv(python, [python] + sys.argv)

if __name__ == '__main__':
    try:
        print('Library check: pip')
        python_install_package('pip')
        print('Library check: discord')
        import discord
        print('Boot...')
    except ModuleNotFoundError as e:
        print(e)
        python_install_package('discord')
        restart_program()
    except Exception as e:
        print(e)
        sys.exit(1)
  
