# -*- coding: utf-8 -*-

__author__ = 'CongRong <tr3jer@gmail.com>'

import os
import sys
import ssl
import pprint
from .utils.TLDS import TLDS
from .utils.domaintools import Domain
from .utils.compat import bytes_decode, urlopen, Request

ssl._create_default_https_context = ssl._create_unverified_context


__all__ = ('updateTLDS', 'domain', 'subMatch')


def updateTLDS():
	'''Update TLDS datas
	:return: end flag
	'''

	req = Request(url='https://publicsuffix.org/list/effective_tld_names.dat')
	data = bytes_decode(urlopen(req).read())

	private = False
	tlds = {}
	for line in data.split('\n'):
		line = line.strip().decode('utf8') if sys.version_info.major == 2 else line.strip()
		if line.startswith('// ===BEGIN PRIVATE DOMAINS==='):
			private = True
			continue
		if not line or line.startswith('//'):
			continue
		line = bytes_decode(line.encode('idna'))
		frags = line.split('.')
		if frags[-1] not in tlds:
			tlds[frags[-1]] = {}
		tlds[frags[-1]][line] = private

	tlds_news = []

	for i in tlds.keys():
		if i not in TLDS.keys():
			tlds_news.append(i)
			print('+ {}'.format(i))

	if tlds_news:
		out = 'TLDS = {}'.format(pprint.pformat(tlds))
		frags = __file__.rsplit('/', 1)

		if len(frags) == 1:
			filename = 'utils/TLDS.py'
		else:
			filename = os.path.join(frags[0], 'utils/TLDS.py')

		f = open(filename, 'w')
		f.write(out)
		f.close()
	else:
		print('TLDS is up to date!')

	return "TLDS update process ends"


def domain(domain, main=None):
	'''
	:param domain: domain
	:param main: [optional] main domain
	:return: Object
	'''

	domain_res = Domain(domain)
	if main and domain_res.valid:
		while True:
			if '.'.join(domain.split('.')[-len(main.split('.')):]) != main:
				break
			# check subdomains of the same length.
			# check that the main domain name has no subdomains.
			# check if the subdomain belongs to the main domain.
			domain_res = domainHandle(domain, main)
			break
	return domain_res


def domainHandle(domain, main):
	result = None
	try:
		subs = domain[:-len(main) - 1]
		domain_res_main = Domain(main)
		main_sub = domain_res_main.subdomain
		main_prefix = main_sub + '.' if main_sub else ''
		domain_res_main.sld = main_prefix + Domain(domain).sld
		domain_res_main.subdomain = subs if subs else None
		domain_res_main.main = main
		result = domain_res_main
	except:
		pass
	finally:
		return result


def subMatch(subdomain, mainlist):
	'''Matches the subdomain to the list of Main domains
	:param subdomain: e.g. test.symbo1.com
	:param mainlist: e.g. ['symbo1.com', 'example.com']
	:return:
	'''

	if not isinstance(mainlist, (list, tuple)):
		mainlist = [mainlist]

	match_result = None
	for main in mainlist:
		if '.'.join(subdomain.split('.')[-len(main.split('.')):]) == main:
			match_result = domainHandle(subdomain, main)
	return match_result

