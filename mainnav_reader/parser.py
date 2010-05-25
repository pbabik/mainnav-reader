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
import struct
import datetime
import sys

from helper import verbose

if sys.version_info < (2, 6):
	from helper import int2bin as bin

def parse(data, logsize):
	'''Main parse function to extract the needed information out of the binary
	data and return the extracted tracks as a list.
	
	@param data: Binary data to parse.
	@param logsize: The size of the tracklogs, as reported by the device.'''
	verbose('parsing binary data.. ', newline=False)
	end_offsets_raw = _parse_tracklog_ends_offsets(data)
	if end_offsets_raw:
		end_offsets = _interprete_end_offsets_raw(end_offsets_raw)
		tracks_raw = _parse_tracklogs(data, end_offsets, logsize)
		tracks = _interprete_tracks_raw(tracks_raw)
		verbose('ok')
		return tracks
	else:
		verbose('ok')
		return None

def _parse_tracklog_ends_offsets(data):
	'''Extract the particular tracklog-end-offsets and return them in binary as
	a list.
	
	@param data: The tracklog binary data'''
	end_offsets = []
	for i in xrange(0, 8192, 16):
		offset_entry = data[i:i + 4]
		if offset_entry == '\xff\xff\xff\xff':
			break # no more offsets remaining
		if offset_entry[-1] == '\xff':
			# devices with 2 MB memory only have 3 bytes for offsets
			offset_entry = '%s\x00' % offset_entry[:-1]
		end_offsets.append(offset_entry)
	return end_offsets

def _interprete_end_offsets_raw(end_offsets_raw):
	'''Convert the binary offset values into real integer values.
	
	@param end_offsets_raw: The offsets in binary format.'''
	return [_convert_4_byte_little_endian_to_uint(entry) for entry in end_offsets_raw]

def _parse_tracklogs(data, end_offsets, logsize):
	'''Extract the particual tracklogs and return them in binary as a list.
	
	@param data: The tracklog binary data.
	@param end_offsets: The tracklog-end-offsets.
	@param logsize: The size of all tracklogs'''
	tracks = []
	track = []
	track_no = 0
	for i in xrange(8192, logsize, 16):
		if i == end_offsets[track_no]:
			tracks.append(track)
			track = []
			track_no += 1
		track.append(data[i:i + 16])
	tracks.append(track) # add last track
	return tracks

def _interprete_tracks_raw(tracks_raw):
	'''Convert the binary points of the tracks to points with real values.
	
	@param tracks_raw: The list of the tracks in binary form.'''
	tracks = []
	for track_raw in tracks_raw:
		track = []
		for point_raw in track_raw:
			point = {}
			point['time'] = _convert_time(point_raw[0:4])
			point['longitude'] = _convert_4_byte_little_endian_to_float(point_raw[4:8])
			point['latitude'] = _convert_4_byte_little_endian_to_float(point_raw[8:12])
			point['speed'] = _convert_speed(point_raw[12:14])
			point['elevation'] = _convert_elevation(point_raw[13:15])
			track.append(point)
		tracks.append(track)
	return tracks

def _convert_speed(bin_data):
	'''Convert the speed from 9 bit binary big endian to int in km/h. The input
	has the size of 2 byte, but only the first 9 bit are interpreted.
	
	@param bin_data: 2 byte binary data.'''
	return ord(bin_data[0]) + int(bin(ord(bin_data[1]))[2:3], 2)

def _convert_elevation(bin_data):
	'''Convert the elevation from 15 bit binary big endian to signed int. Only
	the last 15 bit are taken from the 2 byte input.
	
	@param bin_data: 2 byte binary data.'''
	chunk_one = bin(ord(bin_data[0]))[2:]
	chunk_one = '%s%s' % ((8-len(chunk_one))*'0', chunk_one)
	chunk_one = chunk_one[1:]
	chunk_two = bin(ord(bin_data[1]))[2:]
	chunk_two = '%s%s' % ((8-len(chunk_two))*'0', chunk_two)
	bit_string = '%s%s' % (chunk_one, chunk_two)
	if bit_string.startswith('1'): # negative, build two-complement
		result = ''
		for char in bit_string:
			result = '%s%s' % (result, '1' if char == '0' else '0')
		return -(int(result, 2) + 1)
	else: # positive
		return int(bit_string, 2)
		
def _convert_time(data):
	'''Convert the binary time to a datetime object and return it.
	
	@param data: The binary time.'''
	bin_data = ''
	for byte in data:
		bin_chunk = bin(ord(byte))[2:]
		bin_data = '%s%s%s' % (bin_data, (8-len(bin_chunk))*'0', bin_chunk)
	year = int(bin_data[0:6], 2) + 2006
	month = int(bin_data[6:10], 2)
	day = int(bin_data[10:15], 2)
	hour = int(bin_data[15:20], 2)
	minute = int(bin_data[20:26], 2)
	second = int(bin_data[26:32], 2)
	return datetime.datetime(year, month, day, hour, minute, second)


# common binary to data-type functions:

def _convert_4_byte_big_endian_to_uint(data):
	return struct.unpack('>I', data)[0]

def _convert_4_byte_little_endian_to_uint(data):
	return struct.unpack('<I', data)[0]

def _convert_4_byte_little_endian_to_float(data):
	return struct.unpack('<f', data)[0]
