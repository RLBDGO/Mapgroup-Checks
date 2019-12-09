from os import system

packages = ['numpy-1.17.1-cp36-cp36m-win_amd64.whl',
            'pyparsing-2.4.2-py2.py3-none-any.whl',
            'cycler-0.10.0-py2.py3-none-any.whl',
            'kiwisolver-1.1.0-cp36-none-win_amd64.whl',
            'matplotlib-3.1.1-cp36-cp36m-win_amd64.whl',
            'pytz-2019.2-py2.py3-none-any.whl',
            'pandas-0.25.1-cp36-cp36m-win_amd64.whl']


def main():

    for package in packages:
        try:
            system('python -m pip install --user ' + package)
            print(package.split('-')[0] + ' erfolgreich installiert')
        except Exception:
            raise Exception(package.split('-')[0] + ' konnte nicht installiert werden')


if __name__ == '__main__':
    main()