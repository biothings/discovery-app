''' Discovery Tester Entry Point '''

import os
import sys

from nose.core import run

if __name__ == '__main__':
    SRC_PATH = os.path.dirname(os.path.abspath(__file__))
    PROJ_PATH = os.path.dirname(SRC_PATH)
    if PROJ_PATH not in sys.path:
        sys.path.append(PROJ_PATH)
    print()
    print('Discovery Local Test')
    print('-' * 70)
    print()
    run(argv=['', '--logging-level=INFO', '-v'], defaultTest='discovery.tests')
