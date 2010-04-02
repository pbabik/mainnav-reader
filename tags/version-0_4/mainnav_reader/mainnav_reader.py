# -*- coding: utf-8 -*-
#
# mainnav-reader - Version: 0.4
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
import os
import tempfile
from optparse import OptionParser
import datetime

import helper
from helper import verbose
from helper import die
import communication
import parser
import gpx

def run():
	'''Main function.'''
	helper.check_requirements()
	args = _parse_args()
	helper.verbose_ = args.verbose
	con = communication.Connection(args.device)
	if con.open_connection() and con.check_device_status():
		if args.memory:
			con.close_connection()
			used = (con.logsize - 8192) / 2080000.0 * 100
			print 'memory usage: %.1f%%' % used
			points_remaining = (2080000 - (con.logsize - 8192)) / 16
			time_remaining = points_remaining / 3600.0
			print '%s points or %.1f hours of tracking remaining' % (points_remaining, time_remaining)
		elif args.download:
			raw_data = con.download_data()
			con.close_connection()
			if args.raw:
				_write(((raw_data, 'trackdata.bin'),), args.target_dir)
			else:
				tracks = parser.parse(raw_data, con.logsize)
				i = 1
				gpx_structures = []
				for track in tracks:
					verbose('creating gpx structure for track #%s.. ' % i, newline=False)
					gpx_structure = gpx.create_gpx_structure(track)
					date = track[0]['time'].strftime('%y-%m-%d_%H:%M')
					gpx_structures.append((gpx_structure, 'track_%s.gpx' % date))
					verbose('ok')
					i += 1
				_write(gpx_structures, args.target_dir)
		elif args.purge:
			con.purge_log_on_device()
			con.close_connection()
		else:
			con.close_connection()
			print('nothing to do..')

def _parse_args():
	'''Parse the command-line arguments.'''
	parser = OptionParser(usage='%prog [Options] <device>', version='%prog 0.4')
	parser.add_option('-p', '--purge',
		dest='purge',
		help='purge the tracklog memory on the device',
		action='store_true',
		default=False)
	parser.add_option('-d', '--download',
		dest='download',
		help='download tracklogs from device',
		action='store_true',
		default=False)
	parser.add_option('-t', '--target-dir',
		dest='target_dir',
		help='target directory for downloaded tracklogs [default: %default]',
		default='%s/mainnav-tracklogs/' % os.environ.get('HOME', tempfile.gettempdir()))
	parser.add_option('-r', '--raw',
		dest='raw',
		help='store the raw binary data in the target directory (must be combined with the download option)',
		action='store_true',
		default=False)
	parser.add_option('-m', '--memory',
		dest='memory',
		help='show the amount of memory in use',
		action='store_true',
		default=False)
	parser.add_option('-v', '--verbose',
		dest='verbose',
		help='be verbose',
		action='store_true',
		default=False)

	(options, args) = parser.parse_args()

	try:
		options.device = args[0]
	except IndexError:
		options.device = ''
	if not options.device:
		parser.error('please specify device path, for example \'/dev/ttyUSB0\'')
	if options.download and options.purge:
		parser.error('options -d and -p are mutually exclusive')
	if options.download and options.memory:
		parser.error('options -d and -m are mutually exclusive')
	if options.memory and options.purge:
		parser.error('options -m and -p are mutually exclusive')

	return options

def _write(datas, path):
	'''Write the tracklogs in their specific GPX-files.
	
	@param datas: The list of tracklogs.
	@param path: The target directory.'''
	try:
		os.chdir(path)
	except OSError, e:
		if path == '%s/mainnav-tracklogs/' % os.environ.get('HOME', tempfile.gettempdir()):
			try:
				os.mkdir(path)
				os.chdir(path)
			except OSError, e:
				die(e)
		else:
			die(e)
	folder = datetime.datetime.now().strftime('%y-%m-%d_%H:%M')
	try:
		os.chdir(folder)
	except OSError:
		try:
			os.mkdir(folder)
			os.chdir(folder)
		except OSError, e:
			die('error while creating folder: \'%s\'' % folder)
	i = 1
	for data in datas:
		filename = data[1]
		fullpath = '%s/%s' % (os.getcwd(),  filename)
		if data[1] == 'trackdata.bin':
			verbose('writing binary data to: \'%s\'.. ' % fullpath, newline=False)
		else:
			verbose('writing track #%s to: \'%s\'.. ' % (i, fullpath), newline=False)
		i += 1
		try:
			while os.path.isfile(filename):
				filename = '%s_another.%s' % (filename[:-4], filename[-3:])
			fd = open(filename, 'w')
			fd.write(data[0])
		except OSError, e:
			die(e)
		finally:
			fd.close()
		verbose('ok')

if __name__ == '__main__':
	print('this is the wrong way')