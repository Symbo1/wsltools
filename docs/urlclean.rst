urlclean
========

该模块会对url进行清理：

* :ref:`ast` 分析url每块部位的数据类型并进行替换 
* :ref:`etl` 分析url每块部位的每个字符数据类型并进行替换
* :ref:`pathSplit` 拆分url path根据相对路径返回url列表
* :ref:`mixPayload` 提供一个payload列表，将其组合进url指定部位

.. _ast:

ast
----

.. Method:: Method ast(url, scope=[])

**scope** - [path, params, query, fragment], Default By **All**

::

    In[0]: from wsltools.urlclean import ast
    In[1]: scope = ['path', 'query']
    In[2]: ast('https://www.example.com/path/index;params?a=query1&b=2#fragment', scope=scope)
    Out[2]: 'https://www.example.com/string/string;params?a=string&b=numeric#fragment'

Support Type:

* **path** - numeric/string
* **params** - numeric/string
* **query** - numeric/string/domain/ip/text/url
* **fragment** - numeric/string

.. _etl:

etl
----

.. Method:: Method etl(url, scope=[])

**scope** - [path, params, query, fragment], Default By **All**

::

    In[0]: from wsltools.urlclean import etl
    In[1]: scope = ['path', 'query']
    In[2]: etl('https://www.example.com/path/index;params?a=query1&b=2#fragment', scope=scope)
    Out[2]: 'https://www.example.com/AAAA/AAAAA;params?a=AAAAAN&b=N#fragment'

Implication:

* **E** - Empty
* **A** - Alphabet
* **N** - Number
* **S** - Symbol
* **O** - Other

.. _pathSplit:

pathSplit
---------

.. Method:: Method pathSplit(url)

::

    In[0]: from wsltools.urlclean import pathSplit
    In[1]: pathSplit('https://www.example.com/path1/path2/path3/index;params?a=query1&b=2#fragment')
    Out[1]: 
    ['https://www.example.com/path1/path2/path3/', 'https://www.example.com/path1/', 'https://www.example.com/path1/path2/', 'https://www.example.com/']

.. _mixPayload:

mixPayload
----------

.. Method:: Method mixPayload(url, payloads, scope=[], append=True)

* **payloads** - [payload list]
* **scope** - [path, params, query, fragment], Default By **All**
* **append** - append payload for params/query/fragment, Default is **False**

::

    In[0]: from wsltools.urlclean import mixPayload
    In[1]: payloads = ['-Symbo1-']
    In[2]: url = 'https://www.example.com/path/index;params?a=1&b=2&c=3#fragment'
    In[3]: mixPayload(url, payloads, ['path', 'query', 'params'])
    Out[3]: ['https://www.example.com/-Symbo1-/index;params?a=1&b=2&c=3#fragment',
    'https://www.example.com/path/index;-Symbo1-?a=1&b=2&c=3#fragment',
    'https://www.example.com/path/index;params?a=-Symbo1-&b=3&c=2#fragment',
    'https://www.example.com/path/index;params?a=1&b=-Symbo1-&b=2#fragment',
    'https://www.example.com/path/index;params?a=1&b=3&c=-Symbo1-#fragment']

    # use append:
    In[4]: mixPayload(url, payloads, ['query', 'params', 'fragement'], append=True)
    Out[4]: ['https://www.example.com/path/index;params?a=1&c=3-symbo1-&b=2#fragment',
    'https://www.example.com/path/index;params-symbo1-?a=1&b=2&c=3#fragment',
    'https://www.example.com/path/index;params?a=1&b=2&c=3#fragment-symbo1-',
    'https://www.example.com/path/index;params?a=1&c=3&b=2-symbo1-#fragment',
    'https://www.example.com/path/index;params?a=1-symbo1-&c=3&b=2#fragment']

