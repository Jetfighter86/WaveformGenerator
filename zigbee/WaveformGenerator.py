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


	def GetCRC(self, string_hex_sequence):
		"""
		CRC Function Generator - Zigbee uses CRC-16 CCITT Kermit implementation, with the additional caveat that each byte is flipped before being returned
		:param string_hex_sequence:
		:return:
		"""
		crc_func = crcmod.mkCrcFun(0x11021, initCrc=0, rev=True, xorOut=0x0000)

	def hex2dec(self, hexValue):
		if (type(hexValue == int)):
			print 'true'


if __name__ == "__main__":
	SEQUENCE = "0x1234"
	a = PacketGenerator(SEQUENCE)
	a.GetCRC(SEQUENCE)
