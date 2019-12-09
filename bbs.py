from src.bankbasis import BankBasis
from src.output import output, log_file
from configparser import ConfigParser
from os.path import join
from shutil import copy
from getpass import getuser
from datetime import datetime

config = ConfigParser()
config.read('config_bbs.ini')

IN = config['in']['file.path']

INFO_1 = config['columns']['file.quelle']
INFO_2 = config['columns']['file.mapgruppe']
INFO_3 = config['columns']['file.info']
INFO_4 = config['columns']['file.values']

OUT = config['out']['logs.path']

COPY_TO = config['copy']['copy.file']


def main():

    user = str(getuser())
    date = str(datetime.now())

    file_name = ''.join([s for s in date[0:10]]) + '_' + user

    copy(IN, join(COPY_TO, file_name + '_BABAFilter' + '.csv'))

    test = BankBasis(file_path=r'{}'.format(IN),
                     info_1=int(INFO_1)-1,
                     info_2=int(INFO_2)-1,
                     info_3=int(INFO_3)-1,
                     info_4=int(INFO_4)-1)

    print(output(test.result))

    log_file(test.result, r'{}'.format(OUT))


if __name__ == '__main__':
    main()
