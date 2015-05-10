__author__ = 'Phillip'

import math
import logging
import crcmod


class PacketGenerator(object):
	HEADER = "00000000A7"
	OVER_SAMPLE = 20
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
		if(CRC==None):
			crc=self.GetCRC(string_hex_sequence).upper()
			self.logger.debug("CRC:0x%s"%crc)
		else:
			crc = CRC.upper()
			self.logger.debug("CRC:0x%s"%crc)

		message_size=hex(len(string_hex_sequence)/2+2)[2:].upper()
		message_size.zfill(2)
		print message_size

		self.logger.debug("Payload + CRC size in bytes:0x%s"%message_size)


	def GetCRC(self, string_hex_sequence):
		"""
		CRC Function Generator - Zigbee uses CRC-16 CCITT Kermit implementation, with the additional caveat that each byte is flipped before being returned
		:param string_hex_sequence:
		:return:
		"""
		crc_func=crcmod.mkCrcFun(0x11021, initCrc=0, rev=True, xorOut=0x0000)
		test=string_hex_sequence.decode('hex')
		crc=hex(crc_func(test))[2:]
		crc=crc.zfill(4)
		# flip bits
		crc=crc[2:]+crc[:2]
		return crc
	def hex2dec(self, hexValue):
		if (type(hexValue == int)):
			return int(str(hexValue),16)
		if( type(hexValue)== str):
			return int(hexValue,16)
	def flipBytes(self,message):
		"""
		flip every byte
		:param message:
		:return:
		"""
		new_message=list()
		for count in range(0,len(message)-1,2):
			new_message.append(message[count+1])
			new_message.append(message[count])
		return "".join(new_message)

if __name__ == "__main__":
	SEQUENCE = "0x123456"
	a = PacketGenerator(SEQUENCE)



