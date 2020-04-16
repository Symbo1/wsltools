wsltools: Web Scan Lazy Tools
==============================



.. image:: https://img.shields.io/pypi/v/wsltools.svg
    :target: https://pypi.org/project/wsltools/

.. image:: https://img.shields.io/pypi/l/wsltools.svg
    :target: https://pypi.org/project/wsltools/

.. image:: https://img.shields.io/pypi/wheel/wsltools.svg
    :target: https://pypi.org/project/wsltools/

.. image:: https://img.shields.io/pypi/pyversions/wsltools.svg
    :target: https://pypi.org/project/wsltools/


**wsltools** is an elegant and simple Web Scan auxiliary library for Python.

-------------------

**Installation**:

.. highlight:: sh

::

	>>> pip install wsltools

**Basic Use**:

::

    In[0]: from wsltools import *
    In[1]: payloads = ['-Symbo1-']
    In[2]: url = 'https://www.example.com/path/index;params?a=1&b=2&c=3#fragment'
    In[3]: urlclean.mixPayload(url, payloads, ['path', 'query', 'params'])
    Out[3]: ['https://www.example.com/-Symbo1-/index;params?a=1&b=2&c=3#fragment',
    'https://www.example.com/path/index;-Symbo1-?a=1&b=2&c=3#fragment',
    'https://www.example.com/path/index;params?a=-Symbo1-&b=3&c=2#fragment',
    'https://www.example.com/path/index;params?a=1&b=-Symbo1-&b=2#fragment',
    'https://www.example.com/path/index;params?a=1&b=3&c=-Symbo1-#fragment']


.. toctree::
   :maxdepth: 2

   intro

.. toctree::
   :maxdepth: 3
   :caption: User Guide:

   urlclean
   checksec
   datatype
   similar
   faker
   domaintools

.. toctree::
   :maxdepth: 3
   :caption: Other:

   credits

