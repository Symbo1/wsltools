checksec
********

.. warning::

    该模块仅可识别/拆分基本http响应附带的安全属性，不做其他例如Bypass等处理。


Check Web Application Firewall
==============================

checkWaf
--------

.. Method:: Method checkWaf(content)

传入Response正文进行匹配是否存在waf特征

::

    In[0]: from wsltools.checksec import checkWaf
    In[1]: import requests
    In[2]: checkWaf(requests.get('http://www.cloudflare.com/?xss=<script>alert(/xss/)</script>').content)
    Out[2]: cloudflare


updateRules
-----------

.. Method:: Method updateRules()

从 `sqlmap/wafRules <https://github.com/sqlmapproject/sqlmap/blob/master/thirdparty/identywaf/data.json>`_ 拉取waf特征进行更新

::

    In[0]: from wsltools.checksec import updateRules
    In[1]: updateRules()
    Out[1]: 
    ! 360
    + checkpoint
    + ithemes
    + tmg
    + wapples


Check HTTP Response Headers
===========================

识别并拆分主流安全策略相关的Headers，由于开发人员配置的不同会导致格式不一致，比如存在crlf。只要是浏览器可以识别的格式，都可以精确拆分。

checkHeaders
------------

.. Method:: Method checkHeaders(HTTP Response Headers)

传入一个标准的HTTP Response headers字典，将精确拆分这些安全相关的value字符串。

::

    In[0]: from pprint import pprint
    In[1]: from wsltools.checksec import checkHeaders
    In[2]: import requests
    In[3]: headers = requests.get('https://www.paypal.com/').headers
    In[4]: pprint(checkHeaders(headers))
    Out[4]:
    {'content-security-policy': {'base-uri': ['self', 'https://*.paypal.com'],
                             'connect-src': ['self',
                                             'https://nominatim.openstreetmap.org',
                                             'https://*.paypal.com',
                                             'https://*.paypalobjects.com',
                                             'https://*.google-analytics.com',
                                             'https://*.salesforce.com',
                                             'https://*.force.com',
                                             'https://*.eloqua.com',
                                             'https://nexus.ensighten.com',
                                             'https://api.paypal-retaillocator.com',
                                             'https://*.brighttalk.com',
                                             'https://*.sperse.io',
                                             'https://*.dialogtech.com'],
                             'default-src': ['self',
                                             'https://*.paypal.com',
                                             'https://*.paypalobjects.com'],
                             'font-src': ['self',
                                          'https://*.paypal.com',
                                          'https://*.paypalobjects.com',
                                          'https://assets-cdn.s-xoom.com',
                                          'data:'],
                             'form-action': ['self',
                                             'https://*.paypal.com',
                                             'https://*.salesforce.com',
                                             'https://*.eloqua.com',
                                             'https://secure.opinionlab.com'],
                             'frame-ancestors': ['self',
                                                 'https://*.paypal.com'],
                             'frame-src': ['self',
                                           'https://*.brighttalk.com',
                                           'https://*.paypal.com',
                                           'https://*.paypalobjects.com',
                                           'https://www.youtube-nocookie.com',
                                           'https://www.xoom.com',
                                           'https://www.wootag.com'],
                             'img-src': ['self', 'https:', 'data:'],
                             'object-src': ['none'],
                             'other': ['block-all-mixed-content'],
                             'report-uri': 'https://www.paypal.com/csplog/api/log/csp',
                             'script-src': ['nonce-dmnrj8qfpovrm2bv4ybke6tpgbmlhizeqrg/bqisl7m5znik',
                                            'self',
                                            'https://*.paypal.com',
                                            'https://*.paypalobjects.com',
                                            'https://assets-cdn.s-xoom.com',
                                            'unsafe-inline',
                                            'unsafe-eval'],
                             'style-src': ['self',
                                           'https://*.paypal.com',
                                           'https://*.paypalobjects.com',
                                           'https://assets-cdn.s-xoom.com',
                                           'unsafe-inline']},
    'strict-transport-security': {'max-age': '63072000'},
    'x-content-type-options': 'nosniff',
    'x-frame-options': {'sameorigin': True},
    'x-xss-protection': {'enable': True, 'mode': 'block'}}


x_xss_protection
----------------

.. Method:: Method x_xss_protection(value string)

::

    In[0]: from wsltools.checksec import x_xss_protection
    In[1]: headers = {'X-Xss-Protection': '1; mode = block; report=https://report-uri.com/r/d/xss/enforce'}
    In[2]: x_xss_protection(headers['X-Xss-Protection'])
    Out[2]: 
    {'enable': True,
     'mode': 'block',
     'report': 'https://report-uri.com/r/d/xss/enforce'}

.. _content_security_policy:

content_security_policy
-----------------------

.. Method:: Method content_security_policy(value string)

::

    In[0]: from pprint import pprint
    In[1]: from wsltools.checksec import content_security_policy
    In[2]: headers = {'Content-Security-Policy': "default-src 'self' https://*.paypal.com https://*.paypalobjects.com; frame-src 'self' https://*.brighttalk.com https://*.paypal.com https://*.paypalobjects.com https://www.youtube-nocookie.com https://www.xoom.com https://www.wootag.com; script-src 'nonce-dMNrj8qFpOVrM2Bv4yBKe6TPgBMlHizeqRg/BqiSl7M5Znik' 'self' https://*.paypal.com https://*.paypalobjects.com https://assets-cdn.s-xoom.com 'unsafe-inline' 'unsafe-eval'; connect-src 'self' https://nominatim.openstreetmap.org https://*.paypal.com https://*.paypalobjects.com https://*.google-analytics.com https://*.salesforce.com https://*.force.com https://*.eloqua.com https://nexus.ensighten.com https://api.paypal-retaillocator.com https://*.brighttalk.com https://*.sperse.io https://*.dialogtech.com; style-src 'self' https://*.paypal.com https://*.paypalobjects.com https://assets-cdn.s-xoom.com 'unsafe-inline'; font-src 'self' https://*.paypal.com https://*.paypalobjects.com https://assets-cdn.s-xoom.com data:; img-src 'self' https: data:; form-action 'self' https://*.paypal.com https://*.salesforce.com https://*.eloqua.com https://secure.opinionlab.com; base-uri 'self' https://*.paypal.com; object-src 'none'; frame-ancestors 'self' https://*.paypal.com; block-all-mixed-content; report-uri https://www.paypal.com/csplog/api/log/csp"}
    In[3]: pprint(content_security_policy(headers['Content-Security-Policy']))
    Out[3]:
    {'base-uri': ['self', 'https://*.paypal.com'],
     'connect-src': ['self',
                     'https://nominatim.openstreetmap.org',
                     'https://*.paypal.com',
                     'https://*.paypalobjects.com',
                     'https://*.google-analytics.com',
                     'https://*.salesforce.com',
                     'https://*.force.com',
                     'https://*.eloqua.com',
                     'https://nexus.ensighten.com',
                     'https://api.paypal-retaillocator.com',
                     'https://*.brighttalk.com',
                     'https://*.sperse.io',
                     'https://*.dialogtech.com'],
     'default-src': ['self', 'https://*.paypal.com', 'https://*.paypalobjects.com'],
     'font-src': ['self',
                  'https://*.paypal.com',
                  'https://*.paypalobjects.com',
                  'https://assets-cdn.s-xoom.com',
                  'data:'],
     'form-action': ['self',
                     'https://*.paypal.com',
                     'https://*.salesforce.com',
                     'https://*.eloqua.com',
                     'https://secure.opinionlab.com'],
     'frame-ancestors': ['self', 'https://*.paypal.com'],
     'frame-src': ['self',
                   'https://*.brighttalk.com',
                   'https://*.paypal.com',
                   'https://*.paypalobjects.com',
                   'https://www.youtube-nocookie.com',
                   'https://www.xoom.com',
                   'https://www.wootag.com'],
     'img-src': ['self', 'https:', 'data:'],
     'object-src': ['none'],
     'other': ['block-all-mixed-content'],
     'report-uri': 'https://www.paypal.com/csplog/api/log/csp',
     'script-src': ['nonce-dMNrj8qFpOVrM2Bv4yBKe6TPgBMlHizeqRg/BqiSl7M5Znik',
                    'self',
                    'https://*.paypal.com',
                    'https://*.paypalobjects.com',
                    'https://assets-cdn.s-xoom.com',
                    'unsafe-inline',
                    'unsafe-eval'],
     'style-src': ['self',
                   'https://*.paypal.com',
                   'https://*.paypalobjects.com',
                   'https://assets-cdn.s-xoom.com',
                   'unsafe-inline']}


content_security_policy_report_only
-----------------------------------

.. Method:: Method content_security_policy_report_only(value string)

Same :ref:`content_security_policy`

x_content_security_policy
-------------------------

.. Method:: Method x_content_security_policy(value string)

Same :ref:`content_security_policy`

x_webkit_csp
------------

.. Method:: Method x_webkit_csp(value string)

Same :ref:`content_security_policy`

feature_policy
--------------

.. Method:: Method feature_policy(value string)

Same :ref:`content_security_policy`

x_frame_options
---------------

.. Method:: Method x_frame_options(value string)

::

    In[0]: from wsltools.checksec import x_frame_options
    In[1]: headers = {'X-Frame-Options': 'allow-from  http://symbo1.com/, http://google.com/'}
    In[2]: x_frame_options(headers['X-Frame-Options'])
    Out[2]: {'allow-from': ['http://symbo1.com/', 'http://google.com/']}

    In[3]: headers = {'X-Frame-Options': 'sameorigin'}
    In[4]: x_frame_options(headers['X-Frame-Options'])
    Out[4]: {'sameorigin': True}

    In[5]: headers = {'X-Frame-Options': 'deny'}
    In[6]: x_frame_options(headers['X-Frame-Options'])
    Out[6]: {'deny': True}


access_control_allow_methods
----------------------------

.. Method:: Method access_control_allow_methods(value string)

::

    In[0]: from wsltools.checksec import access_control_allow_methods
    In[1]: headers = {'Access-Control-Allow-Methods': 'GET , POST, PUT, '}
    In[2]: access_control_allow_methods(headers['Access-Control-Allow-Methods'])
    Out[2]: ['GET', 'POST', 'PUT']


access_control_allow_headers
----------------------------

.. Method:: Method access_control_allow_headers(value string)

::

    In[0]: from wsltools.checksec import access_control_allow_headers
    In[1]: headers = {'Access-Control-Allow-Headers': ' Origin , X-Requested-With, Content-Type, Accept , '}
    In[2]: access_control_allow_headers(headers['Access-Control-Allow-Headers'])
    Out[2]: ['Origin', 'X-Requested-With', 'Content-Type', 'Accept']


access_control_expose_headers
-----------------------------

.. Method:: Method access_control_expose_headers(value string)

::

    In[0]: from wsltools.checksec import access_control_expose_headers
    In[1]: headers = {'Access-Control-Expose-Headers': ' Content-Length , Content-Range'}
    In[2]: access_control_expose_headers(headers['Access-Control-Expose-Headers'])
    Out[2]: ['Content-Length', 'Content-Range']


strict_transport_security
-------------------------

.. Method:: Method strict_transport_security(value string)

::

    In[0]: from wsltools.checksec import strict_transport_security
    In[1]: headers = {'Strict-Transport-Security': 'max-age = 16070400 ; includeSubDomains ; preload'}
    In[2]: strict_transport_security(headers['Strict-Transport-Security'])
    Out[2]: {'max-age': '16070400', 'other': ['preload']}


.. _public_key_pins:

public_key_pins
---------------

.. Method:: Method public_key_pins(value string)

::

    In[0]: from wsltools.checksec import public_key_pins
    In[1]: headers = {'Public-Key-Pins': 'pin-sha256="cUPcTAZWKaASuYWhhneDttWpY3oBAkE3h2+soZS7sWs= "; pin-sha256 ="M8HztCzM3elUxkcjR2S5P4hhyBNf6lHkmjAHKhpGPWE="; max-age =5184000; includeSubDomains; report-uri = " https://www.example.org/hpkp-report"'}
    In[2]: public_key_pins(headers['Public-Key-Pins'])
    Out[2]: 
    {'max-age': '5184000',
    'pin-sha256': ['cUPcTAZWKaASuYWhhneDttWpY3oBAkE3h2+soZS7sWs=',
    'M8HztCzM3elUxkcjR2S5P4hhyBNf6lHkmjAHKhpGPWE='],
    'report-uri': 'https://www.example.org/hpkp-report'}



public_key_pins_report_only
---------------------------

.. Method:: Method public_key_pins_report_only(value string)

Same :ref:`public_key_pins`

Other about Security Header
----------------------------

以下headers本身没有复杂的value，便原样输出：

* **access-control-allow-credentials**
* **access-control-allow-origin**
* **access-control-max-age**
* **x-content-type-options**
* **referrer-policy**
* **x-download-options**
* **x-permitted-cross-domain-policies**
* **x-ratelimit-limit**
* **x-ratelimit-remaining**
* **x-ratelimit-reset**
* **x-rate-limit-limit**
* **x-rate-limit-remaining**
* **x-rate-limit-reset**