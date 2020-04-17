# wsltools - Web Scan Lazy Tools


![](https://img.shields.io/pypi/v/wsltools.svg)
![](https://img.shields.io/pypi/l/wsltools.svg)
![](https://img.shields.io/pypi/wheel/wsltools.svg)
![](https://img.shields.io/pypi/pyversions/wsltools.svg)

> **wsltools** is an elegant and simple Web Scan auxiliary library for Python.

-------------------

**Installation**:

```
>>> pip install wsltools
```
**Basic Use**:

```python
In[0]: from wsltools import *
In[1]: payloads = ['-Symbo1-']
In[2]: url = 'https://www.example.com/path/index;params?a=1&b=2&c=3#fragment'
In[3]: urlclean.mixPayload(url, payloads, ['path', 'query', 'params'])
Out[3]: ['https://www.example.com/-Symbo1-/index;params?a=1&b=2&c=3#fragment',
'https://www.example.com/path/index;-Symbo1-?a=1&b=2&c=3#fragment',
'https://www.example.com/path/index;params?a=-Symbo1-&b=3&c=2#fragment',
'https://www.example.com/path/index;params?a=1&b=-Symbo1-&b=2#fragment',
'https://www.example.com/path/index;params?a=1&b=3&c=-Symbo1-#fragment']
```

**Documents**:

https://wsltools.readthedocs.io/

![](https://raw.githubusercontent.com/symbo1/wsltools/master/doc.png)


**User Guide Tree**:

* urlclean
	* [ast](https://wsltools.readthedocs.io/en/latest/urlclean.html#ast)
	* [etl](https://wsltools.readthedocs.io/en/latest/urlclean.html#etl)
	* [pathSplit](https://wsltools.readthedocs.io/en/latest/urlclean.html#pathsplit)
	* [mixPayload](https://wsltools.readthedocs.io/en/latest/urlclean.html#mixpayload)
* checksec
	* Check Web Application Firewall
		* [checkWaf](https://wsltools.readthedocs.io/en/latest/checksec.html#checkwaf)
		* [updateRules](https://wsltools.readthedocs.io/en/latest/checksec.html#updaterules)
	* Check HTTP Response Headers
		* [checkHeaders](https://wsltools.readthedocs.io/en/latest/checksec.html#checkheaders)
		* [x_xss_protection](https://wsltools.readthedocs.io/en/latest/checksec.html#x-xss-protection)
		* [content_security_policy](https://wsltools.readthedocs.io/en/latest/checksec.html#x-xss-protection)
		* [content_security_policy_report_only](https://wsltools.readthedocs.io/en/latest/checksec.html#content-security-policy-report-only)
		* [x_content_security_policy](https://wsltools.readthedocs.io/en/latest/checksec.html#x-content-security-policy)
		* [x_webkit_csp](https://wsltools.readthedocs.io/en/latest/checksec.html#x-webkit-csp)
		* [feature_policy](https://wsltools.readthedocs.io/en/latest/checksec.html#feature-policy)
		* [x_frame_options](https://wsltools.readthedocs.io/en/latest/checksec.html#x-frame-options)
		* [access_control_allow_methods](https://wsltools.readthedocs.io/en/latest/checksec.html#access-control-allow-methods)
		* [access_control_allow_headers](https://wsltools.readthedocs.io/en/latest/checksec.html#access-control-allow-headers)
		* [access_control_expose_headers](https://wsltools.readthedocs.io/en/latest/checksec.html#access-control-expose-headers)
		* [strict_transport_security](https://wsltools.readthedocs.io/en/latest/checksec.html#strict-transport-security)
		* [public_key_pins](https://wsltools.readthedocs.io/en/latest/checksec.html#public-key-pins)
		* [public_key_pins_report_only](https://wsltools.readthedocs.io/en/latest/checksec.html#public-key-pins-report-only)
		* [Other about Security Header](https://wsltools.readthedocs.io/en/latest/checksec.html#other-about-security-header)
* datatype
	* [datatype](https://wsltools.readthedocs.io/en/latest/datatype.html#id1)
	* [isnumeric](https://wsltools.readthedocs.io/en/latest/datatype.html#isnumeric)
	* [istext](https://wsltools.readthedocs.io/en/latest/datatype.html#istext)
	* [isxml](https://wsltools.readthedocs.io/en/latest/datatype.html#isxml)
	* [isjson](https://wsltools.readthedocs.io/en/latest/datatype.html#isjson)
	* [isjsonp](https://wsltools.readthedocs.io/en/latest/datatype.html#isjsonp)
	* [isurl](https://wsltools.readthedocs.io/en/latest/datatype.html#isurl)
	* [isip](https://wsltools.readthedocs.io/en/latest/datatype.html#isip)
	* [isdomain](https://wsltools.readthedocs.io/en/latest/datatype.html#isdomain)
	* [isserialize](https://wsltools.readthedocs.io/en/latest/datatype.html#isserialize)
	* [isimage](https://wsltools.readthedocs.io/en/latest/datatype.html#isimage)
	* [isaudio](https://wsltools.readthedocs.io/en/latest/datatype.html#isaudio)
	* [isvideo](https://wsltools.readthedocs.io/en/latest/datatype.html#isvideo)
	* [isdocument](https://wsltools.readthedocs.io/en/latest/datatype.html#isdocument)
	* [isarchive](https://wsltools.readthedocs.io/en/latest/datatype.html#isarchive)
	* [isurl Support Schemes](https://wsltools.readthedocs.io/en/latest/datatype.html#isurl-support-schemes)
	* [Stream Support Types](https://wsltools.readthedocs.io/en/latest/datatype.html#isurl-support-schemes)
* similar
	* [similar](https://wsltools.readthedocs.io/en/latest/similar.html)
* faker
	* [Instance](https://wsltools.readthedocs.io/en/latest/faker.html#instance)
	* [profile](https://wsltools.readthedocs.io/en/latest/faker.html#profile)
	* [userAgent](https://wsltools.readthedocs.io/en/latest/faker.html#useragent)
	* [creditCard](https://wsltools.readthedocs.io/en/latest/faker.html#creditcard)
	* [email](https://wsltools.readthedocs.io/en/latest/faker.html#email)
	* [name](https://wsltools.readthedocs.io/en/latest/faker.html#name)
	* [ssn](https://wsltools.readthedocs.io/en/latest/faker.html#ssn)
	* [phone](https://wsltools.readthedocs.io/en/latest/faker.html#phone)
	* [job](https://wsltools.readthedocs.io/en/latest/faker.html#job)
	* [company](https://wsltools.readthedocs.io/en/latest/faker.html#company)
	* [address](https://wsltools.readthedocs.io/en/latest/faker.html#address)
	* [Support Credit Card Types](https://wsltools.readthedocs.io/en/latest/faker.html#support-credit-card-types)
	* [Support Locales code](https://wsltools.readthedocs.io/en/latest/faker.html#support-locales-code)
* domaintools
	* [domain](https://wsltools.readthedocs.io/en/latest/domaintools.html#domain)
	* [valid](https://wsltools.readthedocs.io/en/latest/domaintools.html#valid)
	* [main](https://wsltools.readthedocs.io/en/latest/domaintools.html#main)
	* [sld](https://wsltools.readthedocs.io/en/latest/domaintools.html#sld)
	* [tld](https://wsltools.readthedocs.io/en/latest/domaintools.html#tld)
	* [subdomain](https://wsltools.readthedocs.io/en/latest/domaintools.html#subdomain)
	* [sublevel](https://wsltools.readthedocs.io/en/latest/domaintools.html#sublevel)
	* [subMatch](https://wsltools.readthedocs.io/en/latest/domaintools.html#subMatch)
	* [updateTLDS](https://wsltools.readthedocs.io/en/latest/domaintools.html#updatetlds)