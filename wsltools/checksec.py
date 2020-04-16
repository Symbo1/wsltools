# -*- coding: utf-8 -*-

__author__ = 'CongRong <tr3jer@gmail.com>'

import os
import re
import ssl
import json
from .utils.WAFS import WAFS
from .utils.compat import bytes_decode, urlopen, Request

ssl._create_default_https_context = ssl._create_unverified_context


__all__ = ('updateRules', 'checkWaf', 'x_xss_protection', 'content_security_policy',
           'content_security_policy_report_only', 'x_content_security_policy', 'x_webkit_csp',
           'feature_policy', 'x_frame_options', 'access_control_allow_methods',
           'access_control_allow_headers', 'access_control_expose_headers', 'strict_transport_security',
           'public_key_pins', 'public_key_pins_report_only', 'checkHeaders', 'waf_rules')


def prepare_pattern(pattern):
	regex, _, rest = pattern.partition('\\;')
	try:
		return re.compile(regex, re.I)
	except:
		return re.compile(r'(?!x)x')


waf_rules = {}
for name,items in WAFS.items():
	if items['regex']: waf_rules[name] = prepare_pattern(items['regex'])


def updateRules():
	'''Update Waf Rules
	:return: end flag
	'''
	req = Request(url='https://raw.githubusercontent.com/sqlmapproject/sqlmap/master/thirdparty/identywaf/data.json')
	data = json.loads(urlopen(req).read())['wafs']

	wafs_new = []

	for name, items in data.items():
		if name not in WAFS.keys():
			wafs_new.append(name)
			print('+ {}'.format(name))
		if name in WAFS.keys() and data[name]['regex'] != WAFS[name]['regex']:
			print('! {}'.format(name))
			wafs_new.append(name)

	if wafs_new:
		frags = __file__.rsplit('/', 1)
		if len(frags) == 1:
			filename = 'utils/WAFS.py'
		else:
			filename = os.path.join(frags[0], 'utils/WAFS.py')

		with open(filename, 'w') as fp:
			fp.write('__copyright__ = "Copyright (c) 2019 Miroslav Stampar (@stamparm), MIT."\n'
			         '__notice__ = "The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software"\n\n')
			fp.write('WAFS = ')
			json.dump(data, fp, indent=4, ensure_ascii=False)
			fp.close()
	else:
		print('Waf Rules is up to date!')

	return "Waf Rules update process ends"


def checkWaf(content):
	'''
	:param content: HTTP Response
	:return: WAF Name or None
	'''
	content = bytes_decode(content)

	for name,regex in waf_rules.items():
		if regex.search(content):
			return name
	return None


def x_xss_protection(value):
	''' https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-XSS-Protection
	:param value: HTTP Header X-XSS-Protection Value
	:return: dict
	'''
	result = {}
	try:
		value_split = [i.strip() for i in value.split(';')]
		result['enable'] = True if int(value_split[0]) == 1 else False

		for v in value_split[1:]:
			v_tmp = [i.strip() for i in v.split('=')]
			result[v_tmp[0]] = v_tmp[1]

		return result
	except:
		return result


def split_csp_format(value):
	result = {}
	try:
		value_split = [i.strip() for i in value.split(';')]

		for directive in value_split:
			if not directive: continue
			d_tmp = directive.split(' ')
			if len(d_tmp) > 1:
				for v in d_tmp[1:]:
					v_tmp = v.strip("'").strip()
					# Split "xxx-src  'self' ; "

					if not v_tmp: continue

					if d_tmp[0] == 'report-uri':
						result['report-uri'] = v_tmp
					elif d_tmp[0] in result.keys():
						result[d_tmp[0]].append(v_tmp)
					else:
						result[d_tmp[0]] = [v_tmp]
			elif len(d_tmp) == 1:
				if 'other' in result.keys():
					result['other'].append(d_tmp[0])
				else:
					result['other'] = [d_tmp[0]]

		return result
	except:
		return result


def content_security_policy(value):
	''' https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP
	:param value: HTTP Header Content-Security-Policy Value
	:return: dict
	'''
	return split_csp_format(value)


def content_security_policy_report_only(value):
	''' https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy-Report-Only
	:param value: HTTP Header Content-Security-Policy-Report-Only Value
	:return: dict
	'''
	return split_csp_format(value)


def x_content_security_policy(value):
	''' https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP
	:param value: HTTP Header X-Content-Security-Policy Value
	:return: dict
	'''
	return split_csp_format(value)


def x_webkit_csp(value):
	'''
	:param value: HTTP Header X-WebKit-CSP Value
	:return: dict
	'''
	return split_csp_format(value)


def feature_policy(value):
	''' https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Feature-Policy
	:param value: HTTP Header Feature-Policy Value
	:return: dict
	'''
	return split_csp_format(value)


def x_frame_options(value):
	''' https://developer.mozilla.org/en-US/docs/Web/HTTP/X-Frame-Options
	:param value: HTTP Header X-Frame-Options Value
	:return: dict
	'''
	result = {}
	try:
		value_split = value.strip().split(' ')
		# Split " ALLOW-FROM  https://symbo1.com/ , https://example.com/"
		directive = value_split[0]
		if directive == 'allow-from':
			result['allow-from'] = []
			d_tmp = ''.join(value_split[1:])
			for v in d_tmp.split(','):
				if not v: continue
				result['allow-from'].append(v)
		elif directive in ['deny', 'sameorigin']:
			result[value_split[0]] = True

		return result
	except:
		return result


def split_access_control(value):
	result = []
	try:
		value_split = value.split(',')
		for v in value_split:
			v = v.strip()
			if not v: continue
			result.append(v)
		return result
	except:
		return result


def access_control_allow_methods(value):
	''' https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Methods
	:param value: HTTP Header Access-Control-Allow-Methods Value
	:return: list
	'''
	return split_access_control(value)


def access_control_allow_headers(value):
	''' https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Headers
	:param value: HTTP Header Access-Control-Allow-Headers Value
	:return: list
	'''
	return split_access_control(value)


def access_control_expose_headers(value):
	''' https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Expose-Headers
	:param value: HTTP Header Access-Control-Expose-Headers Value
	:return: list
	'''
	return split_access_control(value)


def strict_transport_security(value):
	''' https://infosec.mozilla.org/guidelines/web_security#http-strict-transport-security
	:param value: HTTP Header Strict-Transport-Security Value
	:return: dict
	'''
	result = {}
	try:
		value_split = value.strip().split(';')
		max_age = value_split[0].split('=')
		result[max_age[0].strip()] = max_age[1].strip()
		# Split "max-age = 16070400 ; includeSubDomains ; preload"
		if len(value_split) > 1 and value_split[1]:
			result['other'] = []
			for v in value_split[1:]:
				v = v.strip()
				if v in ['includesubdomains', 'preload']:
					result['other'].append(v)

		return result
	except:
		return result


def public_key_pins(value):
	''' https://developer.mozilla.org/en-US/docs/Web/HTTP/Public_Key_Pinning
	:param value: HTTP Header Public-Key-Pins Value
	:return: dict
	'''
	result = {}
	try:
		value_split = value.split(';')
		for v in value_split:
			v = v.strip()
			v_tmp = v.split('=', 1)
			v_tmp0 = v_tmp[0].strip()
			if v_tmp0 == 'includesubdomains':
				result['includesubdomains'] = True
				continue

			if len(v_tmp) > 1:
				v_tmp1 = [i.strip() for i in v_tmp[1].split('"') if i.strip()][0]
				# Split e.g report-uri = " https://example.com "
				if v_tmp0 in ['report-uri', 'max-age']:
					result[v_tmp0] = v_tmp1
					continue

				if v_tmp0 in result.keys():
					# pin-sha256
					result[v_tmp0].append(v_tmp1)
				else:
					result[v_tmp0] = [v_tmp1]

		return result
	except:
		return result


def public_key_pins_report_only(value):
	''' https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Public-Key-Pins-Report-Only
	:param value: HTTP Header Public-Key-Pins-Report-Only Value
	:return: dict
	'''
	return public_key_pins(value)


def checkHeaders(header):
	'''
	:param header: HTTP Headers dict.
	:return: The value of the split headers becomes dict, list, etc.
	'''

	not_split_headers = ['access-control-allow-credentials', 'access-control-allow-origin',
	                     'access-control-max-age', 'x-content-type-options', 'referrer-policy',
	                     'x-download-options', 'x-permitted-cross-domain-policies', 'x-ratelimit-limit',
	                     'x-ratelimit-remaining', 'x-ratelimit-reset', 'x-rate-limit-limit',
	                     'x-rate-limit-remaining', 'x-rate-limit-reset']
	#These have only unique values

	sec_headers = {}

	for k,v in header.items():
		k,v = k.lower(), v.lower()
		if k in not_split_headers:
			sec_headers[k] = v
		if k == 'x-frame-options':
			sec_headers[k] = x_frame_options(v)
		if k == 'x-xss-protection':
			sec_headers[k] = x_xss_protection(v)
		if k == 'strict-transport-security':
			sec_headers[k] = strict_transport_security(v)
		if k in ['public-key-pins', 'public-key-pins-report-only']:
			sec_headers[k] = public_key_pins(v)
		if k in ['access-control-allow-methods', 'access-control-allow-headers',
		         'access-control-expose-headers']:
			sec_headers[k] = split_access_control(v)
		if k in ['content-security-policy', 'content-security-policy-report-only',
		         'x-content-security-policy', 'x-webkit-csp', 'feature-policy']:
			sec_headers[k] = split_csp_format(v)

	return sec_headers
