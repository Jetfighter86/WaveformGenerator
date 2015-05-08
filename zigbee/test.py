__author__ = 'Phillip'

import decimal

def eng(num):
    return decimal.Decimal(num).normalize().to_eng_string()

test =[-78951,500,1e-3]
for x in test:
    print "%s: %s " %(x,eng(x))

# hi
print 'hi'
def testing(num):
    print "testing"