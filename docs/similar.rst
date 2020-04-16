similar
=======

similar
-------

.. Method:: Method similar(content1, content2, engine='difflib')

**engine** - difflib or simhash, Default By **difflib**

::

    In[0]: from wsltools import similar
    In[1]: import requests
    In[2]: a = requests.get("https://www.symbo1.com/404notFoundPages").content
    In[3]: b = requests.get("https://www.symbo1.com/spiderHere").content
    In[4]: similar(a, b)
    Out[4]: True
