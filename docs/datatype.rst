datatype
========

通过url suffix/content-type判断response类型未必精准，e.g. `Content Sniffing <https://en.wikipedia.org/wiki/Content_sniffing>`_ ，还可以借助此方法扫描备份/敏感文件等。

如果判断流文件，image/audio/video/document/archive，支持类型可参考 :ref:`stream_types`

datatype
--------

.. Method:: Method datatype(datas, scope=[], decrange=[])

* **scope** - [ip, domain, xml, numeric, text, json, jsonp, serialize, url, image, audio, video, document, archive] Default By **All**
* **decrange** - #for **istext**\()# Dec Range e.g range(32,127): normal char. Default By **All**

::

    In[0]: from wsltools.datatype import datatype
    In[1]: import requests
    In[2]: datatype(requests.get('https://www.symbo1.com/feed.xml').content)
    Out[2]: xml


isnumeric
---------

.. Method:: Method isnumeric(datas)

::

    In[0]: from wsltools.datatype import isnumeric
    In[1]: isnumeric('-1.1')
    Out[1]: True


istext
--------

.. Method:: Method istext(datas, decrange=[])

**decrange** - Dec Range e.g range(32,127): normal char. Default By **All**

由于数据类型过多，HTTP Response可能返回frontend等等数据类型。如果需要匹配字符串如flag/密文，
可以指定十进制的范围，例如33-126: **range(33,127)** ，即除了空格以外的正常字符。或 **[1,range(10,30),2]** 等。


::

    In[0]: from wsltools.datatype import istext
    In[1]: istext('U3ltYm8x', decrange=range(33,127))
    Out[1]: True


isxml
--------

.. Method:: Method isxml(datas)

::

    In[0]: from wsltools.datatype import isxml
    In[1]: import requests
    In[2]: isxml(requests.get('https://www.symbo1.com/feed.xml').content)
    Out[2]: True


isjson
--------

.. Method:: Method isjson(datas)

::

    In[0]: from wsltools.datatype import isjson
    In[1]: isjson('{"site":[{"id":"1","name":"Symbo1","url":"www.symbo1.com"}]}')
    Out[1]: True


isjsonp
--------

.. Method:: Method isjsonp(datas)

::

    In[0]: from wsltools.datatype import jsjsonp
    In[1]: isjsonp('symbo1({"site":[{"name":"Symbo1","url":"www.symbo1.com"}]})')
    Out[1]: True


isurl
--------

.. Method:: Method isurl(datas)

:ref:`isurl_schemes`

::

    In[0]: from wsltools.datatype import isurl
    In[1]: isurl('rsync://www.symbo1.com/')
    Out[1]: True


isip
--------

.. Method:: Method isip(datas)

Support Ipv4/6

::

    In[0]: from wsltools.datatype import isip
    In[1]: isip('2404:6800:4012:1::200e')
    Out[1]: True


isdomain
--------

.. Method:: Method isdomain(datas)

不会发起任何请求，会调用 :ref:`domain` 判断是否为合法domain格式。

::

    In[0]: from wsltools.datatype import isdomain
    In[1]: isdomain('symbo1.com')
    Out[1]: True


isserialize
-----------

.. Method:: Method isserialize(datas)

::

    In[0]: from wsltools.datatype import isserialize
    In[1]: isserialize('a:3:{s:12:"merchantname";i:3;s:8:"zip_city";i:1;s:4:"sent";r:2;}')
    Out[1]: True


isimage
--------

.. Method:: Method isimage(datas)

::

    In[0]: from wsltools.datatype import isimage
    In[1]: import requests
    In[2]: isimage(requests.get('https://statics.symbo1.com/file/symbo1/logo.png').content)
    Out[2]: True


isaudio
--------

.. Method:: Method isaudio(datas)

::

    In[0]: from wsltools.datatype import isaudio
    In[1]: import requests
    In[2]: isaudio(requests.get('https://www.example.com/symbo1.mp3').content)
    Out[2]: True


isvideo
--------

.. Method:: Method isvideo(datas)

::

    In[0]: from wsltools.datatype import isvideo
    In[1]: import requests
    In[2]: isvideo(requests.get('https://www.example.com/symbo1.mp4').content)
    Out[2]: True


isdocument
----------

.. Method:: Method isdocument(datas)

::

    In[0]: from wsltools.datatype import isdocument
    In[1]: import requests
    In[2]: isdocument(requests.get('https://www.example.com/symbo1.pdf').content)
    Out[2]: True


isarchive
---------

.. Method:: Method isarchive(datas)

::

    In[0]: from wsltools.datatype import isarchive
    In[1]: import requests
    In[2]: isarchive(requests.get('https://www.example.com/symbo1.zip').content)
    Out[2]: True


.. _isurl_schemes:

isurl Support Schemes
---------------------

* rtsp
* gopher
* file
* rtspu
* git+ssh
* ftp
* rsync
* git
* s3
* shttp
* nntp
* http
* https
* telnet
* ws
* mms
* wais
* imap
* svn
* prospero
* svn+ssh
* sftp
* wss
* vnc
* ldap
* ldaps

.. _stream_types:

Stream Support Types
--------------------

* JPG
* PNG
* GIF
* TIF
* ICO
* MP3
* RAM
* WAV
* MID
* M4A
* SWF
* MOV
* RMVB
* FLV
* MP4
* MPG
* WMV
* AVI
* WMA
* ASF
* PDF
* PST
* OST
* EML
* LZ
* RPM
* CAB
* GZIP
* RAR
* ISO
* 7ZIP
* IMG
* ZIP
* JAR
* APK
* DEB
* XZ
* DMG
* BZ2
* TBZ2
* DOCX/XSLX/PPTX ...
* DOC/XLS/PPT/WPS ...
