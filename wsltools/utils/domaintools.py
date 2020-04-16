# -*- coding: utf-8 -*-
'''\
:mod:`domaintools` -- Domain name parsing tools
===============================================

.. moduleauthor:: Mark Lee <markl@evomediagroup.com>
.. moduleauthor:: Gerald Thibault <jt@evomediagroup.com>
.. changer:: CongRong <tr3jer@gmail.com>

'''

import re
import sys
from .TLDS import TLDS



def cached_property(f):
    '''Decorator which caches property values.

    :param f: The function to decorate.
    :type f: function
    :returns: The wrapper function.
    '''

    def cached(self):
        prop = '_%s' % f.__name__

        if hasattr(self, prop):
            result = getattr(self, prop)
        else:
            result = f(self)
            setattr(self, prop, result)
        return result
    # needed so that doctests are properly discovered
    cached.__doc__ = f.__doc__
    return property(cached)


class Domain(object):
    '''Handles parsing domains. All domain names are canonicalized
        via lowercasing and conversion to punycode. __unicode__ will
        return the decoded version

    TODO make sure it's compliant with http://tools.ietf.org/html/rfc1035

    :param domain_string: the domain name to parse.
    :type domain_string: unicode
    '''

    __domain_part_regex = re.compile(u'(?!-)[A-Z\d-]{1,63}(?<!-)$', re.IGNORECASE)

    def __init__(self, domain_string, allow_private=False):
        if ':' in domain_string:
            # strip out port numbers
            domain_string, port = domain_string.rsplit(':', 1)
        self.allow_private = allow_private
        self.__private = False
        try:
            self.__full_domain = str(bytes.decode(domain_string.lower().encode('idna')))
        except:
            self.__full_domain = domain_string.lower()
        self.__domain_parts = self.__full_domain.split('.')
        if self.__domain_parts[-1] == '':
            self.__domain_parts.pop()

    @cached_property
    def domain(self):
        '''The full domain name (second level domain + top level domain)

        :rtype: unicode, or None if the domain name is invalid.

        >>> d = Domain(u'www.brokerdaze.co.uk')
        >>> d.domain
        u'brokerdaze.co.uk'
        '''
        if self.valid:
            return '%s.%s' % (self.sld, self.tld)
        else:
            return None

    @domain.setter
    def domain(self, newdomain):
        setattr(self, '_domain', newdomain)

    @cached_property
    def subdomain(self):
        '''The subdomain (i.e., www).

        :rtype: unicode, or None if the subdomain does not exist.

        >>> d = Domain(u'www.brokerdaze.co.uk')
        >>> d.subdomain
        u'www'
        '''
        result = None
        tld = self.tld
        if tld is not None:
            dots = tld.count('.')
            if dots == len(self.__domain_parts) - 2:
                return None
            result = '.'.join(self.__domain_parts[:-2 - dots])
        return result

    @subdomain.setter
    def subdomain(self, newsub):
        setattr(self, '_subdomain', newsub)

    @cached_property
    def sublevel(self):
        '''The subdomain level (i.e. 0:a,1:b,c:d).

        >>> d = Domain(u'c.b.a.symbo1.com')
        >>> d.sublevel
        "{0:'a',1:'b',2:'c'}"
        '''
        result = {}
        subdomains = self.subdomain.split(".")[::-1] if self.subdomain else ""
        for sub in range(0, len(subdomains)):
            result[sub] = subdomains[sub]
        return result

    @cached_property
    def main(self):
        '''Exclude subdomain, sld + tld.

        >>> d = Domain(u'www.symbo1.com')
        >>> d.main
        'symbo1.com'
        '''
        return self.sld + '.' + self.tld

    @main.setter
    def main(self, newmain):
        setattr(self, '_main', newmain)

    @cached_property
    def sld(self):
        '''The second level domain (SLD).

        :rtype: unicode, or None if the SLD does not exist.

        >>> d = Domain(u'www.brokerdaze.co.uk')
        >>> d.sld
        u'brokerdaze'
        '''
        result = None
        tld = self.tld
        if tld is not None:
            dots = tld.count('.')
            if dots == len(self.__domain_parts) - 1:
                return None
            result = self.__domain_parts[-2 - dots]
        return result

    @sld.setter
    def sld(self, newsld):
        setattr(self, '_sld', newsld)

    @cached_property
    def tld(self):
        '''The top level domain (TLD) (i.e., co.uk).

        :rtype: unicode, or None if the TLD is invalid.

        >>> d = Domain(u'www.brokerdaze.co.uk')
        >>> d.tld
        u'co.uk'
        '''
        result = None
        if len(self.__domain_parts) == 1:
            return result
        tld = self.__domain_parts[-1]
        if tld in TLDS:
            choices = TLDS[tld]
            for i in range(len(self.__domain_parts)):
                _parts = self.__domain_parts[-1-i:]
                check = '.'.join(_parts)
                if check in choices:
                    # found a match, first check if it's private
                    self.__private = choices[check]
                    if self.__private:
                        if not self.allow_private:
                            # ignore this and return the true tld
                            self.__private = False
                            break
                    # valid match, store it and try for a longer match
                    result = check
                    continue

                if i == 0:
                    # do not try wildcard matches on single components
                    continue
                # check for wildcard
                check2 = '.'.join(['*'] + _parts[1:])
                if check2 in choices:
                    # wildcard found in choices, the tested tld is valid
                    result = check
                if result:
                    break
        else:
            pass
        return result

    @cached_property
    def valid(self):
        '''Determines if the domain is valid.

        :returns: True if valid, False otherwise.
        :rtype: bool

        >>> d = Domain(u'www.brokerdaze.co.uk')
        >>> d.valid
        True
        >>> d = Domain(u'foo')
        >>> d.valid
        False
        '''
        if self.tld is None or self.sld is None or '' in self.__domain_parts:
            return False
        if len(self.__full_domain) > 253:
            return False
        for part in self.__domain_parts:
            if len(part) > 63:
                return False
            if part[-1] == '-':
                return False
            if part[0] == '*' and len(part) > 1:
                return False
            if self.__domain_part_regex.match(part) is None:
                return False
        return True

    @cached_property
    def valid_host(self):
        '''Determines if the domain is valid.

        :returns: True if valid, False otherwise.
        :rtype: bool

        >>> d = Domain(u'www.brokerdaze.co.uk')
        >>> d.valid
        True
        >>> d = Domain(u'foo')
        >>> d.valid
        False
        '''
        if self.tld is None or self.sld is None or '' in self.__domain_parts:
            return False
        if len(self.__full_domain) > 253:
            return False
        ix = 0
        for part in self.__domain_parts:
            ix += 1
            if len(part) > 63:
                return False
            if part[-1] == '-':
                return False
            if part[0] == '*' and len(part) > 1:
                return False
            if part[0] == '*' and len(part) == 1 and ix == 1:
                continue
            if self.__domain_part_regex.match(part) is None:
                return False
        return True

    @cached_property
    def private(self):
        if self.tld is None:
            return False
        return self.__private

    def __repr__(self):
        '''Generates a representation of the object, with the domain as an
        ASCII string.

        >>> Domain(u'www.brokerdaze.co.uk')
        <Domain: www.brokerdaze.co.uk>
        '''
        return '<%s: %s>' % (self.__class__.__name__, self.__str__())

    def __unicode__(self):
        '''Returns the full domain name. Any punycode is converted.

        >>> unicode(Domain('www.brokerdaze.co.uk'))
        u'www.brokerdaze.co.uk'
        '''
        return self.__full_domain.decode('idna') if sys.version_info.major == 2 else str.encode(self.__full_domain).decode('idna')

    def __str__(self):
        u'''Returns the full domain name, in punycode (if necessary).

        >>> str(Domain(u'www.brokerdaze.рф'))
        'www.brokerdaze.xn--p1ai'
        >>> str(Domain('www.brokerdaze.xn--p1ai'))
        'www.brokerdaze.xn--p1ai'
        '''
        return self.__full_domain

