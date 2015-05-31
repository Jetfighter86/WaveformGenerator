__author__ = 'Phillip'

import operator

class Formula:

    def __init__(self):
        pass

    def hex2bin(self,hexVal):
        """
        :param hexVal:
        :return: binary
        """
        if hexVal[:2]=='0x':
            hexVal = hexVal[2:]
        return bin(int(hexVal,16))[2:]

    def hex2dec(self,decVal):
        return hex(decVal)

    def hexcomp(self,hexVal):
        """

        :param hexVal:
        :return: One's Complement of a hex number
        """
        print hex(hexVal ^ )


if __name__ == '__main__':
    zb = Formula()
    print type(0xff)
    print zb.hexcomp(0xFFFF)