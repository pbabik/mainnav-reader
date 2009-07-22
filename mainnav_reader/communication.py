# -*- coding: utf-8 -*-
#
# mainnav-reader - Version: 0.1 
#
# Copyright (c) 2009, Dennis Keitzel
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
import time
try:
	import serial
except ImportError as e:
	raise SystemExit(e)

from parser import _convert_4_byte_big_endian_to_uint as convert_logsize_value
from helper import verbose
from helper import die
from helper import fprint

#commands
INIT_DOWNLOAD = '$1\r\n'
PURGE_LOG = '$2\r\n'
CHECK_STATUS = '$3\r\n'
DOWNLOAD_CHUNK = '\x15'
DOWNLOAD_CHUNK_COUNTER = '\x06'
ABORT_TRANSMISSION = '\x18'
INIT_STANDARD = '\x0f\x06'

#replies
OK = '$OK!\r\n'
FINISH = '$FINISH\r\n'
ABORTED = '\x06\x06\x06\x06'

class Connection():
	'''Represents a connection to the device, either via USB or Bluetooth,
	through a virtual serial port.
	
	@param port: The path to the port which represents the device.
	@param slow: If set, the download-speed gets decreased.'''
	def __init__(self, port, slow):
		try:
			self.ser = serial.Serial(
				port=port,
				baudrate=115200,
				parity=serial.PARITY_NONE,
				stopbits=serial.STOPBITS_ONE,
				bytesize=serial.EIGHTBITS)
		except serial.serialutil.SerialException as e:
			die('error: %s' % e)
		self.logsize = 0
		self.dl_waittime = 0.1 if slow else 0.03

	def _communicate(self, command, waittime=1, answer=True):
		'''Talk to the device and return the answer.
		
		@param command: The command being send.
		@param waittime: Time to sleep, before the answer is being red.
		@param answer: Set this to False, if you no answer is needed.'''
		self.ser.write(command)
		time.sleep(waittime)
		if answer:
			return self.ser.read(self.ser.inWaiting())

	def open_connection(self):
		'''Open the connection to the device.'''
		verbose('opening \'%s\'.. ' % self.ser.port, newline=False)
		self.ser.open()
		success = self.ser.isOpen()
		verbose('ok' if success else 'error')
		return success

	def close_connection(self):
		'''Close the connection.'''
		verbose('closing connection.. ', newline=False)
		self.ser.close()
		success = not self.ser.isOpen()
		verbose('ok' if success else 'error')
		return success

	def check_device_status(self):
		'''Check if the device responds, and also save the size of the tracklogs
		which's inside the respond.'''
		verbose('checking device status.. ', newline=False)
		buf = self._communicate(CHECK_STATUS)
		success = True if OK in buf else False
		verbose('ok' if success else 'error: is the device turned on?')
		if success:
			self.logsize = convert_logsize_value(buf[-4:])
		return success

	def download_data(self):
		'''Download all tracklogs from the device.'''
		verbose('switching device to download mode.. ', newline=False)
		if OK in self._communicate(INIT_DOWNLOAD):
			verbose('ok')
			buf = ''
			newline = ''
			while True:
				internal_buf = self._communicate(DOWNLOAD_CHUNK, waittime=self.dl_waittime)
				if FINISH in internal_buf:
					break
				if len(internal_buf) != 132:
					print('%serror: connection is too slow, retrying with decreased speed..' % newline)
					if ABORTED in self._communicate(ABORT_TRANSMISSION):
						self.dl_waittime += 0.03
						return self.download_data()
					else:
						die('error while downloading tracklogs')
				else:
					fprint('\rdownloading: %s%%' % int((len(buf) / float(self.logsize)) * 100), newline=False)
					buf += internal_buf[3:-1]
					newline = '\n'
			fprint('')
			verbose('switching device back to standard mode.. ', newline=False)
			self._communicate(INIT_STANDARD, answer=False)
			verbose('ok')
			return buf
		else:
			fprint('error')
			
	def purge_log_on_device(self):
		'''Delete all tracklogs from the device.'''
		fprint('purge log on device.. ', newline=False)
		buf = self._communicate(PURGE_LOG, waittime=1)
		if OK not in buf:
			die('error while trying to purge the log')
		else:
			while FINISH not in buf:
				time.sleep(1)
				buf += self.ser.read(self.ser.inWaiting())
			fprint('ok')