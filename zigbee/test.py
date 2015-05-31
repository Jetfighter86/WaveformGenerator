__author__ = 'Phillip'


try:
    from msvcrt import getche
    import sys
except ImportError:
    import termios
    import tty

while True:
    k = getche()
    if k == 'q':
        sys.exit()
    if k == 'm':
        print 'hi'
