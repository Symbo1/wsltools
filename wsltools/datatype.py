# -*- coding: utf-8 -*-

__author__ = 'CongRong <tr3jer@gmail.com>'

import re
import sys
import json
import binascii
from io import BytesIO
from ast import literal_eval
from .utils.ipaddr import IPAddress
from .utils.domaintools import Domain
from .utils.compat import urlparse, bytes_decode, xrange

try:
	import xml.etree.cElementTree as ET
except ImportError:
	import xml.etree.ElementTree as ET

__all__ = ('isdomain', 'isip', 'isjson', 'isjsonp', 'isnumeric',
           'isserialize', 'istext', 'isurl', 'isxml', 'isimage', 'isaudio',
           'isvideo', 'isdocument', 'isarchive', 'datatype', 'data_types')

data_types = ('image', 'audio', 'video', 'document', 'archive', 'ip', 'domain',
              'xml', 'numeric', 'json', 'jsonp', 'serialize', 'url', 'text')


def isnumeric(datas):
	try:
		literal = literal_eval(datas)
		return True if isinstance(literal, (int, float)) else False
	except:
		return False


def istext(datas, decrange=[]):
	'''
	:param decrange: [optional] Ascii Decimal range list, e.g range(32,127) : normal char
	:return:
	'''
	try:
		if decrange:
			if False in list(map(lambda x: ord(x) in decrange, datas)):
				return False

		if isnumeric(datas) or not datas: return False
		literal = literal_eval("'{}'".format(datas))
		return True if isinstance(literal, str) else False
	except:
		return False


def isxml(datas):
	try:
		ET.fromstring(datas)
		return True
	except:
		return False


def isjson(datas):
	try:
		if isnumeric(datas): return False
		json.loads(datas)
		return True
	except:
		return False


def isjsonp(datas):
	try:
		re_match = re.sub(r'([a-zA-Z_0-9\.]*\()|(\);?$)', '', datas)
		literal = literal_eval(re_match)
		if datas == re_match: return False

		if isinstance(literal, (dict, list, str)):
			return True
		else:
			return False
	except:
		return False


def isurl(datas):
	try:
		parse = urlparse(datas)

		#https://en.wikipedia.org/wiki/List_of_URI_schemes
		schemes = ['rtsp', 'gopher', 'file', 'rtspu', 'git+ssh',
		           'ftp', 'rsync', 'git', 's3', 'shttp', 'nntp',
		           'http', 'https', 'telnet', 'ws', 'mms', 'wais',
		           'imap', 'svn', 'prospero', 'svn+ssh', 'sftp',
		           'wss', 'vnc', 'ldap', 'ldaps']

		if parse.scheme not in schemes: return False
		if not Domain(parse.hostname).valid and not isip(parse.hostname): return False

		return True
	except:
		return False


def isip(datas):
	''' Support ipv4/6
	'''
	try:
		IPAddress(datas)
		return True
	except:
		return False


def isdomain(datas):
	try:
		return True if Domain(datas).valid else False
	except:
		return False


def unserialize(buffer):
	buffer_items = []

	def followup(byte):
		v = buffer.read(len(byte))
		if v != byte:
			raise ValueError('failed')

	def load_range(end):
		buf = []
		while 1:
			char = buffer.read(1)
			if char == end:
				break
			elif not char:
				raise ValueError('failed')
			buf.append(char)
		return b''.join(buf)

	def load_array():
		items = int(load_range(b':')) * 2
		followup(b'{')
		result = []
		last_item = None
		for _ in xrange(items):
			item = _unserialize()
			buffer_items.append(item)
			if last_item is None:
				last_item = item
			else:
				result.append((last_item, item))
				last_item = None
		followup(b'}')
		return result

	def _unserialize():
		type_ = buffer.read(1).lower()
		if type_ == b'n':
			followup(b';')
			return None
		if type_ in b'idb':
			followup(b':')
			data = load_range(b';')
			if type_ == b'i':
				return int(data)
			if type_ == b'd':
				return float(data)
			return bool(int(data))
		if type_ == b's':
			followup(b':')
			range_len = int(load_range(b':'))
			followup(b'"')
			data = buffer.read(range_len)
			followup(b'"')
			followup(b';')
			return data
		if type_ == b'a':
			followup(b':')
			return dict(load_array())
		if type_ == b'o':
			followup(b':')
			name_len = int(load_range(b':'))
			followup(b'"')
			name = buffer.read(name_len)
			followup(b'":')
			return name, dict(load_array())
		if type_ == b'r':
			followup(b':')
			reference = int(load_range(b';'))
			values = []
			for k,v in enumerate(buffer_items):
				if k % 2 != 0:
					values.append(v)
			return values[reference - 2]
		raise ValueError('failed')

	return _unserialize()


def isserialize(datas):
	try:
		if sys.version_info.major == 3 and isinstance(datas, str):
			datas = datas.encode()
		unserialize(BytesIO(datas))

		return True
	except:
		return False


def isimage(datas):
	try:
		return True if stream(datas, stype='image') else False
	except:
		return False


def isaudio(datas):
	try:
		return True if stream(datas, stype='audio') else False
	except:
		return False


def isvideo(datas):
	try:
		return True if stream(datas, stype='video') else False
	except:
		return False


def isdocument(datas):
	try:
		return True if stream(datas, stype='document') else False
	except:
		return False


def isarchive(datas):
	try:
		return True if stream(datas, stype='archive') else False
	except:
		return False


# https://www.filesignatures.net/
# https://en.wikipedia.org/wiki/List_of_file_signatures
def streamTypes():
	return {
		'image': {
			'FFD8FFE0': 'JPG',
			'89504E47': 'PNG',
			'47494638': 'GIF',
			'49492A00': 'TIF',
			'424D228C': 'BMP',
			'424D8240': 'BMP',
			'424D8E1B': 'BMP',
			'00000100': 'ICO'
		},
		'audio': {
			'49443303': 'MP3',
			'4C414D45': 'MP3',
			'2E7261FD': 'RAM',
			'57415645': 'WAV',
			'52494646': 'WAV',
			'4D546864': 'MID',
			'00000020667479704D34': 'M4A',
		},
		'video': {
			'465753': 'SWF',
			'6D6F6F76': 'MOV',
			'2E524D46': 'RMVB',
			'464C560105': 'FLV',
			'0000002066747970': 'MP4',
			'000001BA': 'MPG',
			'000001B3': 'MPG',
			'3026B2758E66CF11': 'WMV/WMA/ASF',
			'A6D900AA0062CE6C': 'WMV/WMA/ASF',
			'52494646': 'AVI',
		},
		'document': {
			'25504446': 'PDF',
			'21424EA56FB5A6':'PST',
			'2142444E':'OST',
			'5265636569766564': 'EML',
			'504B030414000600': 'DOCX/XSLX/PPTX ...',   #Priority is higher than 504B0304
			'D0CF11E0A1': 'DOC/XLS/PPT/WPS ...'
		},
		'archive': {
			'425A68': 'BZ2/TBZ2',
			'4C5A4950': 'LZ',
			'EDABEEDB': 'RPM',
			'49536328': 'CAB',
			'4D534346': 'CAB',
			'1F8B0800': 'GZIP',
			'526172211A': 'RAR',
			'4344303031': 'ISO',
			'377ABCAF271C': '7ZIP',
			'EB3C902A': 'IMG',
			'504B0304': 'ZIP/JAR/APK ...',
			'504B0506': 'ZIP',
			'504B0708': 'ZIP',
			'504B4C495445': 'ZIP',
			'504B537058': 'ZIP',
			'57696E5A6970': 'ZIP',
			'213C617263683E': 'DEB',
			'FD377A585A0000': 'XZ',
			'7801730D': 'DMG'
		}
	}


def stream(datas, scope=[], stype=None):
	try:
		if sys.version_info.major == 3 and isinstance(datas, str):
			datas = datas.encode()

		buffer = BytesIO(datas).read(10)
		hexs = binascii.hexlify(buffer).upper()

		if isinstance(hexs, bytes):
			hexs = hexs.decode()

		stream_type = None
		stypes = streamTypes()
		if stype: stypes = {stype: stypes[stype]}

		if scope:
			stypes_tmp = {}
			for skey in scope:
				stypes_tmp[skey] = stypes[skey]
			stypes = stypes_tmp

		for typeis in stypes.keys():
			for hcode, typename in stypes[typeis].items():
				lens = len(hcode)
				if hexs[0:lens] == hcode:
					if typeis == 'archive' and hexs[lens:lens+8] == '14000600':
						continue
					stream_type = typeis
					break
			else:
				continue
			break

		return stream_type
	except:
		pass


def datatype(datas, scope=[], decrange=[]):
	'''
	:param datas:
	:param scope: [optional] a list, e.g. ['json', 'ip' ...], See data_types
	:param decrange: for istext function
	:return:
	'''
	try:
		if scope:
			for stype in scope:
				if stype not in data_types:
					raise ValueError('scope not in data_types')

			streams = ['image', 'audio', 'video', 'document', 'archive']
			normals = {'ip': isip, 'domain': isdomain, 'xml': isxml, 'numeric': isnumeric, 'json': isjson,
			           'jsonp': isjsonp, 'serialize': isserialize, 'url': isurl, 'text': istext}

			stream_scope = [stype for stype in scope if stype in streams]
			normal_scope = sorted([stype for stype in scope if stype in normals.keys()], key=data_types.index)

			if stream_scope:
				stype = stream(datas, scope=stream_scope)
				if stype: return stype

			try:
				datas = bytes_decode(datas)

				datas = datas.lstrip().rstrip()
				typeis = None
				for stype in normal_scope:
					if stype == 'text':
						if istext(datas, decrange=decrange):
							typeis = stype
							break
					elif normals[stype](datas):
						typeis = stype
						break

				return typeis
			except:
				return None

		stype = stream(datas)
		if stype:
			return stype

		datas = bytes_decode(datas)
		datas = datas.lstrip().rstrip()

		datasLen = len(datas)

		if 7 <= datasLen <= 40 and isip(datas):
			return "ip"
		elif 3 <= datasLen <= 253 and isdomain(datas):
			return "domain"
		elif isxml(datas):
			return "xml"
		elif isnumeric(datas):
			return "numeric"
		elif isjson(datas):
			return "json"
		elif isjsonp(datas):
			return "jsonp"
		elif isserialize(datas):
			return "serialize"
		elif isurl(datas):
			return "url"
		elif istext(datas, decrange=decrange):
			return "text"


	except:
		return None

