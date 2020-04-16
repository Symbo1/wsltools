# -*- coding: utf-8 -*-

import sys

PY2 = sys.version_info.major == 2


if PY2:
	xrange = xrange
	text_type = unicode
	string_types = (str, unicode)
	from urllib import unquote, urlencode
	from urllib2 import urlopen, Request
	from urlparse import urlparse, parse_qsl, urlunparse
else:
	xrange = range
	text_type = str
	string_types = (str,)
	from urllib.request import urlopen, Request
	from urllib.parse import urlparse, parse_qsl, unquote, urlencode, urlunparse


def bytes_decode(content):
	if isinstance(content, string_types):
		pass
	elif isinstance(content, bytes):
		content = bytes.decode(content)
	else:
		content = str(content)
	return content
