# -*- coding: utf-8 -*-

__author__ = 'CongRong <tr3jer@gmail.com>'

import copy
from .datatype import datatype, isnumeric
from .utils.compat import unquote, urlencode, urlparse, parse_qsl, urlunparse, xrange


__all__ = ('ast', 'etl', 'pathSplit', 'mixPayload')


def char_etl(char):
	'''Extraction-Transformation-Loading.

	:param char: Character
	:return:
	'''
	symbo1 = range(33,127)
	chars = ""
	if char == '': return 'E'   #Empty
	for c in char:
		c = c.lower()
		if ord('a') <= ord(c) <= ord('z'):  #Alphabet, a-z, A-Z
			chars += 'A'
		elif ord('0') <= ord(c) <= ord('9'):    #Number, 0-9
			chars += 'N'
		elif ord(c) in symbo1:   #Symbol, exclude: a-z, A-Z, 0-9
			chars += 'S'
		else:               #Other char
			chars += 'O'
	return chars


def etl(url, scope=[]):
	'''Extraction-Transformation-Loading for url.
	Replace characters in url with universal expression characters.
	:param url: Generic URL.
	:param scope: [optional] list, e.g. [params, path, query, fragment]
	:return:
	'''

	u = urlparse(url)
	if not scope or 'params' in scope:
		params_new = char_etl(u.params)
	else:
		params_new = u.params

	if not scope or 'path' in scope:
		path_split = u.path.split("/")[1:]
		etl_path = []
		for p in path_split:
			if p == '':
				continue
			else:
				etl_path.append(char_etl(p))
		path_new = "/" + "/".join(etl_path) + ('/' if path_split[-1] == '' else '')
	else:
		path_new = u.path

	if not scope or 'query' in scope:
		query = unquote(u.query)
		querys = sorted(parse_qsl(query, True))

		query_list = [q[0] + "=" + char_etl(q[1]) for q in querys]
		# sort and did not use urlencode for stitching, choose manual stitching.
		# Because the py2/3 urlencode/dict sort is inconsistent.
		query_new = "&".join(query_list)
	else:
		query_new = u.query

	if not scope or 'fragment' in scope:
		fragment_new = char_etl(u.fragment)
	else:
		fragment_new = u.fragment

	url_new = urlunparse((u.scheme, u.netloc, path_new, params_new, query_new, fragment_new))
	return url_new


def ast(url, scope=[]):
	'''
	:param url: Generic URL.
	:param scope: [optional] list, e.g. [params, path, query, fragment]
	:return: Abstract Syntax Tree for URL.
	'''

	u = urlparse(url)
	if not scope or 'params' in scope:
		params_new = ('numeric' if isnumeric(u.params) else 'string') if u.params else ''
	else:
		params_new = u.params

	if not scope or 'path' in scope:
		path_split = u.path.split("/")[1:]
		ast_path = []
		for p in path_split:
			if p == '':
				continue
			else:
				ast_path.append('numeric' if isnumeric(p) else 'string')
		path_new = "/" + "/".join(ast_path) + ('/' if path_split[-1] == '' else '')
	else:
		path_new = u.path

	if not scope or 'query' in scope:
		query = unquote(u.query)
		querys = sorted(parse_qsl(query, True))

		ast_query_scope = ['domain', 'ip', 'numeric', 'text', 'url']

		query_list = []
		for q in querys:
			param_type = datatype(q[1], scope=ast_query_scope)
			param_type = 'string' if param_type == 'text' else param_type
			query_list.append(q[0] + "=" + str(param_type))
		#sort and did not use urlencode for stitching, choose manual stitching.
		#Because the py2/3 urlencode/dict sort is inconsistent.
		query_new = "&".join(query_list)
	else:
		query_new = u.query

	if not scope or 'fragment' in scope:
		fragment_new = ('numeric' if isnumeric(u.fragment) else 'string') if u.fragment else ''
	else:
		fragment_new = u.fragment

	url_new = urlunparse((u.scheme, u.netloc, path_new, params_new, query_new, fragment_new))
	return(url_new)


def pathSplit(url):
	'''
	:param url: Generic URL.
	:return: List of decomposed paths.
	'''

	result = set()
	u = urlparse(url)
	base_path = u.scheme + "://" + u.netloc + '/'
	result.add(base_path)

	if len(u.path) > 1:
		path_tmp = ''
		for i in u.path[:u.path.rindex("/") + 1].split('/'):
			if i:
				path_tmp += i + '/'
				result.add(base_path + path_tmp)
	result = list(result)
	return result


def mixPayload(url, payloads, scope=[]):
	'''
	:param url: Generic URL.
	:param payloads: Payloads list
	:param scope: [optional] list, e.g. [params, path, query, fragment]
	:return: list
	'''

	url = unquote(url)
	result = set()
	u = urlparse(url)

	if not isinstance(payloads, (list, tuple)):
		payloads = [payloads]

	path_split = u.path.split("/")[1:-1]
	qs_dict = dict(parse_qsl(u.query, keep_blank_values=1))

	for p in payloads:
		if (not scope or 'params' in scope) and u.params:
			result.add(urlunparse([u.scheme, u.netloc, u.path, p, u.query, u.fragment]))


		if not scope or 'path' in scope:
			for i in xrange(len(path_split)):
				pathsTmp = copy.copy(path_split)
				if pathsTmp[i] == '': continue

				pathsTmp[i] = p
				result.add(urlunparse([u.scheme, u.netloc,
				                                ('/' + '/'.join(pathsTmp) + '/' + u.path.split("/")[-1]),
				                                u.params, u.query, u.fragment]))

		if not scope or 'query' in scope:
			for k in qs_dict.keys():
				tmp_dict = copy.deepcopy(qs_dict)
				tmp_dict[k] = p
				tmp_qs = unquote(urlencode(tmp_dict))

				result.add(urlunparse([u.scheme, u.netloc, u.path, u.params, tmp_qs, u.fragment]))

		if (not scope or 'fragment' in scope) and u.fragment:
			result.add(urlunparse([u.scheme, u.netloc, u.path, u.params, u.query, p]))

	result = list(result)

	return result
