__author__ = 'Phillip'

import math
import logging
import crcmod
import numpy
import matplotlib.pylab as plt


class PacketGenerator(object):
    HEADER = "00000000A7"
    OVER_SAMPLE = 50
    PI = 3.141593
    DAC_PEAK = pow(2, 14)
    DAC_MIN = 0
    BIT_REDUCTION = 1

    def __init__(self, string_hex_sequence, CRC=None):
        """
        Zigbee Phy Packet Generator
        :param string_hex_sequence:
        :param CRC:
        :return:
        """
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger("Waveform Generator")
        # Strip hex '0x' in front if present
        if ( string_hex_sequence[:2] == "0x"):
            string_hex_sequence = string_hex_sequence[2:]
        self.logger.debug("\nPayload:0x%s" % string_hex_sequence)
        # perform CRC
        if (CRC == None):
            crc = self.GetCRC(string_hex_sequence).upper()
            self.logger.debug("CRC:0x%s" % crc)
        else:
            crc = CRC.upper()
            self.logger.debug("CRC:0x%s" % crc)

        message_size = hex(len(string_hex_sequence) / 2 + 2)[2:].upper()
        message_size.zfill(2)

        self.logger.debug("Payload + CRC size in bytes:0x%s" % message_size)
        self.message = self.flipBytes(self.HEADER + str(message_size) + string_hex_sequence.upper() + crc.upper())
        self.nonFlipMessage = self.HEADER + str(message_size) + string_hex_sequence.upper() + crc.upper()
        self.logger.info("Generated Packet:0x%s" % self.message)
        print self.message
        print self.nonFlipMessage
        # self.GetIQData(self.message)

    def GetCRC(self, string_hex_sequence):
        """
        CRC Function Generator - Zigbee uses CRC-16 CCITT Kermit implementation, with the additional caveat that each byte is flipped before being returned
        :param string_hex_sequence:
        :return:
        """
        crc_func = crcmod.mkCrcFun(0x11021, initCrc=0, rev=True, xorOut=0x0000)
        test = string_hex_sequence.decode('hex')
        crc = hex(crc_func(test))[2:]
        crc = crc.zfill(4)
        # flip bits
        crc = crc[2:] + crc[:2]
        return crc

    def hex2dec(self, hexValue):
        if (type(hexValue == int)):
            return int(str(hexValue), 16)
        if ( type(hexValue) == str):
            return int(hexValue, 16)

    def flipBytes(self, message):
        """
        flip every byte
        :param message:
        :return:
        """
        new_message = list()
        for count in range(0, len(message) - 1, 2):
            new_message.append(message[count + 1])
            new_message.append(message[count])
        return "".join(new_message)


class WaveformGenerator2400MHZ(PacketGenerator):
    """
    2400MHZ Waveform Generator: Creates a 2.4GHZ OQPSK Zigbee PHY packet for Agilent SGs
    """
    spreading_sequence = dict({
    '0': '11011001110000110101001000101110',
    '1': '11101101100111000011010100100010',
    '2': '00101110110110011100001101010010',
    '3': '00100010111011011001110000110101',
    '4': '01010010001011101101100111000011',
    '5': '00110101001000101110110110011100',
    '6': '11000011010100100010111011011001',
    '7': '10011100001101010010001011101101',
    '8': '10001100100101100000011101111011',
    '9': '10111000110010010110000001110111',
    'A': '01111011100011001001011000000111',
    'B': '01110111101110001100100101100000',
    'C': '00000111011110111000110010010110',
    'D': '01100000011101111011100011001001',
    'E': '10010110000001110111101110001100',
    'F': '11001001011000000111011110111000',
    'z': '00000010100111001011101110000000'
    }
    )
    DATA_I=list()
    DATA_Q=list()
    COMBINED_IQ=list()

    def __init__(self, string_hex_sequence, delay_ms=0, CRC=None):
        self.delay_ms = delay_ms
        # super(WaveformGenerator2400MHZ, self).__init__(string_hex_sequence, CRC)
        DATA_Q= self.GetIQData(string_hex_sequence)
        DATA_I=self.GetIQData(string_hex_sequence)
        COMBINED_IQ=self.GetIQData(string_hex_sequence)


    def GetIQData(self, message):
        """
        Waveform Generator for IQ purposes
        :param message:
        :return:
        """
        if(message[:2]=='0x'):
            message=message[2:]
        y = self.OVER_SAMPLE / 2
        half_point = self.DAC_MIN
        data_I = list()
        data_Q = list()
        norm_d = list()
        coefList=list()
        for a in range(0, self.OVER_SAMPLE):
            d = math.sin(a * self.PI / self.OVER_SAMPLE)
            norm_d.append(math.floor(math.floor(d * (self.DAC_PEAK - 1) + 0.5) / self.BIT_REDUCTION))
        for i in message:
            for j in xrange(0, 31, 2):
                try:
                    data_bit_I = self.spreading_sequence[i][j]
                    data_bit_Q = self.spreading_sequence[i][j + 1]
                except KeyError:
                    self.logger.critical("key Error: %s, %s" % (i,data_bit_I))
                if (data_bit_I == '1'):
                    coef = 1
                else:
                    coef = -1
                for k in range(0, self.OVER_SAMPLE):
                    data_I.append((norm_d[k] * coef) + half_point)
                if(data_bit_Q=='1'):
                    coef=1
                else:
                    coef=-1
                for k in range(0,self.OVER_SAMPLE):
                    data_Q.append((norm_d[k]*coef)+half_point)
                y=+self.OVER_SAMPLE
        y = self.OVER_SAMPLE/2
        self.COMBINED_IQ = [x+y for x,y in zip(data_Q,data_I)]
        self.DATA_I = data_I
        self.DATA_Q = data_Q
        # self.Graph(range(0,len(dataTotal)), dataTotal,range(len(data_Q)),data_Q)

    def OQPSK(self,data_I,data_Q,period=None):
        period = self.OVER_SAMPLE
        I = data_I
        Q = data_Q
        ILength = len(I)
        QLength = len(Q)
        CombineList = list()
        for i in range(ILength):
            if(i < period/2):
                CombineList.append(I[i])
            else:
                CombineList.append((I[i]+ Q[i-period/2]))
        return CombineList



    def GetXAxis(self,list):
        try:
            return range(0,len(list))
        except Exception:
            logging.critical("GetXAxis: %s" % Exception.message)

    def Graph(self, x_axis, y_axis, x_axis2=None, y_axis2=None, x_axis3=None, y_axis3=None):
        try:
            if(x_axis2==None and y_axis2==None and x_axis3==None and y_axis3==None):
                graph = plt.plot(x_axis, y_axis, 'r.', linewidth=2)
                plt.show()
            elif(x_axis3==None and y_axis3==None):
                plt.figure(1)
                plt.subplot(211)
                plt.plot(x_axis, y_axis, 'g.', linewidth=2)
                plt.subplot(212)
                plt.plot(x_axis2,y_axis2,'r.')
                plt.show()

            else:
                plt.figure(1)
                plt.subplot(3,1,1)
                plt.plot(x_axis, y_axis, 'g.', linewidth=2)
                plt.subplot(3,1,2)
                plt.plot(x_axis2,y_axis2,'r.')
                plt.subplot(3,1,3)
                plt.figure(2)
                plt.plot(x_axis3,y_axis3,'b.')
                for i in range(0,len(x_axis),self.OVER_SAMPLE+ self.OVER_SAMPLE/2):
                    plt.axvline(x=i+self.OVER_SAMPLE/2)
                plt.show()
        except ValueError:
            self.logger.critical("ValueError %s"% ValueError.message)

if __name__ == "__main__":
    SEQUENCE = "0x0"
    # a = PacketGenerator(SEQUENCE)
    # b = WaveformGenerator2400MHZ(SEQUENCE).GetIQData(SEQUENCE)
    b= WaveformGenerator2400MHZ(SEQUENCE)
    c = b.OQPSK(b.DATA_I,b.DATA_Q)
    print b.DATA_I
    print b.DATA_Q
    print c
    b.Graph(b.GetXAxis(b.DATA_I), b.DATA_I,b.GetXAxis(b.DATA_Q),b.DATA_Q,b.GetXAxis(b.COMBINED_IQ),b.COMBINED_IQ)



