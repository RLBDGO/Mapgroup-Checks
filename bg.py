from src.bilanzgliederung import BilanzGliederung
from src.output import output, log_file
from configparser import ConfigParser


config = ConfigParser()
config.read('config_bg.ini')

IN = config['in']['file.path']

INFO_1 = config['columns']['file.bgs']
INFO_2 = config['columns']['file.mg']
INFO_3 = config['columns']['file.m']
INFO_4 = config['columns']['file.ba']
INFO_5 = config['columns']['file.V']

OUT = config['out']['Ergebnisse.path']


def main():

    test = BilanzGliederung(file_path=r'{}'.format(IN),
                            info_1=int(INFO_1)-1,
                            info_2=int(INFO_2)-1,
                            info_3=int(INFO_3)-1,
                            info_4=int(INFO_4)-1,
                            info_5=int(INFO_5)-1)

    print(output(test.result))
    for i in test.compare_tup_tri():
        print(i)

    log_file(test.result, r'{}'.format(OUT))


if __name__ == '__main__':
    main()
