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
import xml.dom.minidom as minidom

def create_gpx_structure(track):
	'''Create the gpx-xml structure and return it.
	
	@param track: The list of points (=the track).'''
	doc = minidom.Document()

	gpx = doc.createElement('gpx')
	gpx.setAttribute('version', '1.1')
	gpx.setAttribute('creator', 'mainnav-reader (version 0.3) - http://code.google.com/p/mainnav-reader/')
	gpx.setAttribute('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
	gpx.setAttribute('xmlns', 'http://www.topografix.com/GPX/1/1')
	gpx.setAttribute('xsi:schemaLocation', 'http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd')
	doc.appendChild(gpx)

	trk = doc.createElement('trk')
	gpx.appendChild(trk)

	name = doc.createElement('name')
	trk.appendChild(name)
		
	name_txt = doc.createTextNode('track_%s' % track[0]['time'].isoformat())
	name.appendChild(name_txt)
	
	trkseg = doc.createElement('trkseg')
	trk.appendChild(trkseg)
	
	for point in track:
		trkpt = doc.createElement('trkpt')
		trkpt.setAttribute('lat', str(point['latitude']))
		trkpt.setAttribute('lon', str(point['longitude']))
		trkseg.appendChild(trkpt)
		
		ele = doc.createElement('ele')
		trkpt.appendChild(ele)
		ele_txt= doc.createTextNode(str(point['elevation']))
		ele.appendChild(ele_txt)
		
		time = doc.createElement('time')
		trkpt.appendChild(time)
		time_txt = doc.createTextNode('%s' % point['time'].isoformat())
		time.appendChild(time_txt)
		
	return doc.toprettyxml(indent='  ', encoding='UTF-8')
