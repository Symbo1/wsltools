from __future__ import absolute_import, unicode_literals

import sys

if sys.version_info.major == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')

from .. import BaseProvider
from .....utils.compat import text_type
from ...utils.text_unidecode import unidecode

localized = True

import re
import unicodedata
from functools import wraps


_re_pattern = re.compile(r'[^\w\s-]', flags=re.U)
_re_pattern_allow_dots = re.compile(r'[^\.\w\s-]', flags=re.U)
_re_spaces = re.compile(r'[-\s]+', flags=re.U)


def slugify2(value, allow_dots=False, allow_unicode=False):
    """
    Converts to lowercase, removes non-word characters (alphanumerics and
    underscores) and converts spaces to hyphens. Also strips leading and
    trailing whitespace. Modified to optionally allow dots.

    Adapted from Django 1.9
    """
    if allow_dots:
        pattern = _re_pattern_allow_dots
    else:
        pattern = _re_pattern

    value = text_type(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
        value = pattern.sub('', value).strip().lower()
        return _re_spaces.sub('-', value)
    value = unicodedata.normalize('NFKD', value).encode(
        'ascii', 'ignore').decode('ascii')
    value = pattern.sub('', value).strip().lower()
    return _re_spaces.sub('-', value)


def slugify(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        return slugify2(fn(*args, **kwargs))
    return wrapper


def slugify_domain(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        return slugify2(fn(*args, **kwargs), allow_dots=True)
    return wrapper


def slugify_unicode(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        return slugify2(fn(*args, **kwargs), allow_unicode=True)
    return wrapper


def lowercase(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs).lower()
    return wrapper


class Provider(BaseProvider):
    safe_email_tlds = ('org', 'com', 'net')
    free_email_domains = ('gmail.com', 'yahoo.com', 'hotmail.com')
    tlds = (
        'com', 'com', 'com', 'com', 'com', 'com', 'biz', 'info', 'net', 'org',
    )
    hostname_prefixes = ('db', 'srv', 'desktop', 'laptop', 'lt', 'email', 'web')

    user_name_formats = (
        '{{last_name}}.{{first_name}}',
        '{{first_name}}.{{last_name}}',
        '{{first_name}}##',
        '?{{last_name}}',
    )
    email_formats = (
        '{{user_name}}@{{domain_name}}',
        '{{user_name}}@{{free_email_domain}}',
    )
    url_formats = (
        'www.{{domain_name}}/',
        '{{domain_name}}/',
    )
    uri_formats = (
        '{{url}}',
        '{{url}}{{uri_page}}/',
        '{{url}}{{uri_page}}{{uri_extension}}',
        '{{url}}{{uri_path}}/{{uri_page}}/',
        '{{url}}{{uri_path}}/{{uri_page}}{{uri_extension}}',
    )
    image_placeholder_services = (
        'https://www.lorempixel.com/{width}/{height}',
        'https://dummyimage.com/{width}x{height}',
        'https://placekitten.com/{width}/{height}',
        'https://placeimg.com/{width}/{height}/any',
    )

    replacements = ()

    def _to_ascii(self, string):
        for search, replace in self.replacements:
            string = string.replace(search, replace)

        string = unidecode(string)
        return string

    @lowercase
    def email(self, domain=None):
        if domain:
            email = '{}@{}'.format(self.user_name(), domain)
        else:
            pattern = self.random_element(self.email_formats)
            email = "".join(self.generator.parse(pattern).split(" "))
        return email

    @lowercase
    def safe_email(self):
        return '{}@example.{}'.format(
            self.user_name(), self.random_element(self.safe_email_tlds),
        )

    @lowercase
    def free_email(self):
        return self.user_name() + '@' + self.free_email_domain()

    @lowercase
    def company_email(self):
        return self.user_name() + '@' + self.domain_name()

    @lowercase
    def free_email_domain(self):
        return self.random_element(self.free_email_domains)

    @lowercase
    def ascii_email(self):
        pattern = self.random_element(self.email_formats)
        return self._to_ascii(
            "".join(self.generator.parse(pattern).split(" ")),
        )


    @slugify_unicode
    def user_name(self):
        pattern = self.random_element(self.user_name_formats)
        username = self._to_ascii(
            self.bothify(self.generator.parse(pattern)).lower(),
        )
        return username

    @lowercase
    def hostname(self, levels=1):
        """
        Produce a hostname with specified number of subdomain levels.

        >>> hostname()
        db-01.nichols-phillips.com
        >>> hostname(0)
        laptop-56
        >>> hostname(2)
        web-12.williamson-hopkins.jackson.com
        """
        if levels < 1:
            return self.random_element(self.hostname_prefixes) + '-' + self.numerify('##')
        return self.random_element(self.hostname_prefixes) + '-' + self.numerify('##') + '.' + self.domain_name(levels)

    @lowercase
    def domain_name(self, levels=1):
        """
        Produce an Internet domain name with the specified number of
        subdomain levels.

        >>> domain_name()
        nichols-phillips.com
        >>> domain_name(2)
        williamson-hopkins.jackson.com
        """
        if levels < 1:
            raise ValueError("levels must be greater than or equal to 1")
        if levels == 1:
            return self.domain_word() + '.' + self.tld()
        else:
            return self.domain_word() + '.' + self.domain_name(levels - 1)

    @lowercase
    @slugify_unicode
    def domain_word(self):
        company = self.generator.format('company')
        company_elements = company.split(' ')
        company = self._to_ascii(company_elements.pop(0))
        return company

    def tld(self):
        return self.random_element(self.tlds)

    def url(self, schemes=None):
        """
        :param schemes: a list of strings to use as schemes, one will chosen randomly.
        If None, it will generate http and https urls.
        Passing an empty list will result in schemeless url generation like "://domain.com".

        :returns: a random url string.
        """
        if schemes is None:
            schemes = ['http', 'https']

        pattern = '{}://{}'.format(
            self.random_element(schemes) if schemes else "",
            self.random_element(self.url_formats),
        )

        return self.generator.parse(pattern)
