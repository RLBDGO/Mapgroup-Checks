from src.bankbasis import BankBasis
from src.output import output, log_file

def main():

    o = BankBasis('test_case/BankBasisFilter.csv', 5, 10, 13, 15)
    print(output(o.result))
    log_file(o.result, 'test_case')

if __name__ == '__main__':
    main()
