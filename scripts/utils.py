from datetime import datetime, date
import os

class bcolors:
    DEFAULT = '\033[37m'
    INFO = '\33[92m'
    WARN = '\33[33m'
    FAIL = '\033[91m'

def bot_print(msg: str, status: str) -> str:
    now = datetime.now()
    td = date.today()

    col = bcolors.DEFAULT
    if status == 'INFO':
        col = bcolors.INFO
    elif status == 'WARN':
        col = bcolors.WARN
    elif status == 'FAIL':
        col = bcolors.FAIL


    # prints a string of format
    # <date>T<time> <status> <msg)
    print(f'{bcolors.DEFAULT}[{td}T{now.strftime("%H:%M:%S")}] {col}{status}{col} {bcolors.DEFAULT}{msg}{bcolors.DEFAULT}{bcolors.DEFAULT}')

if __name__ == '__main__':
    bot_print('making money', 'INFO')
    bot_print('medium error', 'WARN')
    bot_print('big error', 'FAIL')

