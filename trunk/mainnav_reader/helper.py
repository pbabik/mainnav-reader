# -*- coding: utf-8 -*-
#
# mainnav-reader - Version: 0.5-dev
#
# Copyright (c) 2009-2010, Dennis Keitzel
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
import sys

verbose_ = False

def verbose(msg, newline=True):
	'''Helper function to print messages only if verbose is set.
	
	@param msg: The message.
	@param newline: Set to False, to omit the newline.'''
	if verbose_:
		fprint(msg, newline)
			
def fprint(msg, newline=True):
	'''Function which flushes a print instantly.
	
	@param msg: The message.
	@param newline: Set to False, to omit the newline.'''
	sys.stdout.write('%s\n' % msg if newline else msg)
	sys.stdout.flush()

def die(msg):
	'''Exit the program with a message.
	
	@param msg: The message.'''
	raise SystemExit(msg)

def int2bin(n):
	'''convert denary integer n to binary string b.
	Used for python versions below 2.6
	
	@param n: the denary integer.'''
	b = ''
	if n < 0:  raise ValueError, 'must be a positive integer'
	if n == 0: return '0b0'
	while n > 0:
		b = '%s%s' % (str(n % 2), b)
		n = n >> 1
	return '0b%s' % b

def check_requirements():
	'''Check if all requirements are met.'''
	# Python
	version = sys.version_info
	if version < (2, 5) or version >= (3, 0):
		die('Python version not supported, use Python-2.5 or above. Python 3 is not supported.')
	
	# pySerial / python-serial
	try:
		import serial
	except ImportError:
		die('Module \'serial\' from pySerial (python-serial on some distributions) is needed.')
