from getpass import getuser
from datetime import datetime
import os


def output(messages):

    text = ''

    for message in messages:
        text += '---------------------------------------------------------------------------\n' + message + '\n'

    return text + '---------------------------------------------------------------------------\n'


def log_file(messages, directory):

    user = str(getuser())
    date = str(datetime.now())

    text = f'TIMESTAMP: {date}' + '\n' + f'PRUEFER*IN: {user}' + '\n\n' + output(messages)
    file_name = ''.join([s for s in date[0:10]])+'_'+user

    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(directory + '/'+file_name, 'w') as f:
            f.write(text)

    except Exception:
        print('logfile konnte nicht erzeugt werden')