from src.mapgro import BBS
from src.output import output, log_file

def main():

    o = BBS('test_case/testdata.csv', 5, 10, 13, 15)
    print(output(o.results))
    log_file(o.results, 'test_case')

if __name__ == '__main__':
    main()
