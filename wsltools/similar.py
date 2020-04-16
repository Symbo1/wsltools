# -*- coding: utf-8 -*-

__author__ = 'CongRong <tr3jer@gmail.com>'


import difflib
from .utils.compat import bytes_decode, xrange


hashbits = 128
difflib_threshold = 0.95
simhash_threshold = 0.95


def simhash(tokens):
	v = [0] * hashbits
	for t in [string_hash(x) for x in tokens]:
		for i in xrange(hashbits):
			bitmask = 1 << i
			if t & bitmask:
				v[i] += 1
			else:
				v[i] -= 1
	fingerprint = 0
	for i in xrange(hashbits):
		if v[i] >= 0:
			fingerprint += 1 << i
	return fingerprint


def string_hash(source):
	if source == "":
		return 0
	else:
		x = ord(source[0]) << 7
		m = 1000003
		mask = 2 ** hashbits - 1
		for c in source:
			x = ((x * m) ^ ord(c)) & mask
		x ^= len(source)
		if x == -1:
			x = -2
		return x


def hamming_distance(hash1, hash2):
	x = (hash1 ^ hash2) & ((1 << hashbits) - 1)
	tot = 0
	while x:
		tot += 1
		x &= x - 1
	return tot


def similar(content1, content2, engine='difflib'):
	'''
	:param content1: content1
	:param content2: content2
	:param engine: [optional] diiflib / simhash, Default By difflib
	:return: Bool
	'''
	content1, content2 = map(lambda x: bytes_decode(x), [content1, content2])

	sim = False

	if engine == 'difflib':
		if difflib.SequenceMatcher(None, content1, content2).quick_ratio() > difflib_threshold: sim = True

	elif engine == 'simhash':
		hash1 = simhash(content1.split())
		hash2 = simhash(content2.split())

		hamming = hamming_distance(hash1, hash2)
		res = float(hashbits - hamming) / hashbits

		if hamming: simhash_threshold = 0.90

		sim = True if res >= simhash_threshold else False

	return sim

