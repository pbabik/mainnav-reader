# -*- coding: utf-8 -*-
#
# mainnav-reader - Version: 0.3
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
		offset_entry = data[i:i + 3]
		if offset_entry == '\xff\xff\xff':
			break
		end_offsets.append(offset_entry)
	return end_offsets

def _interprete_end_offsets_raw(end_offsets_raw):
	'''Convert the binary offset values into real integer values.
	
	@param end_offsets_raw: The offsets in binary format.'''
	return [_convert_3_byte_little_endian_to_uint(entry) for entry in end_offsets_raw]

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
		last_elevation = 0
		for point_raw in track_raw:
			point = {}
			point['time'] = _convert_time(point_raw[0:4])
			point['longitude'] = _convert_4_byte_little_endian_to_float(point_raw[4:8])
			point['latitude'] = _convert_4_byte_little_endian_to_float(point_raw[8:12])
			point['speed'] = _convert_9_bit_big_endian_to_int(point_raw[12:14])
			point['elevation'] = last_elevation = _get_elevation(point_raw[14:16], last_elevation)
			track.append(point)
		tracks.append(track)
	return tracks

def _get_elevation(bin_data, last_elevation):
	'''If there is only a 3D-fix, return the last available elevation.'''
	elevation = _convert_2_byte_little_endian_to_uint(bin_data)
	return last_elevation if elevation == 255 else elevation # 255 means 2D-fix

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


# binary to data-type functions:

def _convert_4_byte_big_endian_to_uint(data):
	return struct.unpack('>I', data)[0]

def _convert_3_byte_little_endian_to_uint(data):
	return struct.unpack('<I', '%s\x00' % data)[0]

def _convert_4_byte_little_endian_to_float(data):
	return struct.unpack('<f', data)[0]

def _convert_9_bit_big_endian_to_int(data):
	return ord(data[0]) + int(bin(ord(data[1]))[:3], 2)

def _convert_2_byte_little_endian_to_uint(data):
	return struct.unpack('<H', data)[0]
