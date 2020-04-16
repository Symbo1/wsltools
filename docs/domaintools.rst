domaintools
************

.. _domain:

domain
======

.. Method:: Method domain(domain, main=Main Domain)

**main** - Default by **Not Use**

::

    In[0]: from wsltools.domaintools import domain
    In[1]: domain('www.symbo1.com', main='symbo1.com')
    Out[1]: symbo1.com


valid
-----

.. Attribute:: Attribute valid

::

    In[0]: from wsltools.domaintools import domain
    In[1]: domain('www.symbo1.com').valid
    Out[1]: True


main
-----

.. Attribute:: Attribute main


::

    In[0]: from wsltools.domaintools import domain
    In[1]: domain('sub.symbo1.com').main
    Out[1]: symbo1.com

    # if provide main domain:
    In[2]: domaintools.domain("sub.example.symbo1.com",'example.symbo1.com').main
    Out[2]: example.symbo1.com


sld
----

.. Attribute:: Attribute sld

::

    In[0]: from wsltools.domaintools import domain
    In[1]: domain('sub.symbo1.com').sld
    Out[1]: symbo1

    # if provide main domain:
    In[2]: domaintools.domain("sub.example.symbo1.com",'example.symbo1.com').sld
    Out[2]: example.symbo1


tld
----

.. Attribute:: Attribute tld

::

    In[0]: from wsltools.domaintools import domain
    In[1]: domain('sub.symbo1.com').tld
    Out[1]: com


subdomain
---------

.. Attribute:: Attribute subdomain

::

    In[0]: from wsltools.domaintools import domain
    In[1]: domain('sub.example.symbo1.com').subdomain
    Out[1]: sub.example

    # if provide main domain:
    In[2]: domain("sub.example.symbo1.com",'example.symbo1.com').subdomain
    Out[2]: sub

sublevel
--------

.. Attribute:: Attribute sublevel

可以通过提供main的方式选取从哪里开始截取，所以sublevel的索引从0开始。

::

    In[0]: from wsltools.domaintools import domain
    In[1]: domain('sub.example.symbo1.com').sublevel
    Out[1]: {0: 'example', 1: 'sub'}

    # if provide main domain:
    In[2]: domaintools.domain('sub.example.symbo1.com', 'example.symbo1.com').sublevel
    Out[2]: {0: 'sub'}


subMatch
========

.. Method:: Method subMatch(subdomain, mainlist)

* **subdomain** - e.g. test.symbo1.com
* **mainlist** - e.g. [symbo1.com, example.com]

当自动化收集子域名时，可通过该方法判断是否准确，并返回以上的属性。

::

    In[0]: from wsltools.domaintools import subMatch
    In[1]: subMatch('www.symbo1.com', ['symbo1.com', 'google.com', 'apple.com'])
    Out[1]: symbo1.com

    # valid/main/sld/tld/subdomain/sublevel attribute:
    In[2]: subMatch('sub3.sub2.sub1.symbo1.com', ['symbo1.com', 'google.com', 'apple.com']).sublevel
    Out[2]: {0: 'sub1', 1: 'sub2', 2: 'sub3'}


updateTLDS
==========

.. Method:: Method updateTLDS()

::

    In[0]: from wsltools.domain import updateTLDS
    In[1]: updateTLDS()
    Out[1]: 
    + llp
    + phd
    + onion
    + inc
    + xn--e1a4c
    TLDS update process ends
