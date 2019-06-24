'''
    Discovery Tester Entry Point
'''

from nose.core import run

if __name__ == '__main__':
    print()
    print('Discovery Local Test')
    print('-' * 70)
    print()
    run(argv=['', '--logging-level=INFO', '-v'], defaultTest='discovery.tests')
