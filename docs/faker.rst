faker
=====

该模块主要用于爬虫/扫描器在动态爬取的同时可生成对应需要填充的数据，例如搜索参数/注册登陆表单等。

而且实现代码并不多，是因为调用了 `joke2k/faker <https://github.com/joke2k/faker>`_ 。对其做了很多改动。保留了主要的数据生成provider，并fixed几个本地化语言的bug，感兴趣可以将 **wsltools/utils/faker/** 与原Package diff对比。

Instance
--------

.. Class:: Class faker(Locale code)

**Locale code** - :ref:`locale_code` , Default By **en**

::

    In[0]: from wsltools import faker
    In[1]: faker('en_US')
    Out[1]: <class: faker en_US>


profile
-------

.. Attribute:: Attribute profile

::

    In[0]: from pprint import pprint
    In[1]: from wsltools import faker
    In[2]: obj = faker()
    In[3]: pprint(obj.profile)
    Out[3]: 
    {'address': '761 Perez Village Apt. 282\nWest John, NE 36491',
     'birthdate': datetime.date(1911, 10, 26),
     'company': 'Johnston PLC',
     'credit_card': {'code': '036',
                     'expire': '01/30',
                     'first_name': 'Jennifer',
                     'last_name': 'Harris',
                     'name': 'Jennifer Harris',
                     'number': '3553426503431050',
                     'security': 'CVC',
                     'type': 'jcb16',
                     'type_full': 'JCB 16 digit'},
     'first_name': 'Jennifer',
     'job': 'Speech and language therapist',
     'last_name': 'Harris',
     'mail': 'ashley97@yahoo.com',
     'name': 'Jennifer Harris',
     'phone': '979-648-3157',
     'residence': '213 Darrell Wells Suite 305\nSouth Manuelmouth, CT 64277',
     'sex': 'M',
     'ssn': '893-66-9475',
     'username': 'ramirezchristina',
     'website': 'http://www.parker.org/'}


userAgent
---------

.. Method:: Method userAgent(platform='desktop')

**platform** - desktop or mobile, Default By **desktop**

::

    In[0]: from wsltools import faker
    In[1]: obj = faker()
    In[2]: obj.userAgent(platform='mobile')
    Out[2]: Mozilla/5.0 (iPod; U; CPU iPhone OS 4_1 like Mac OS X; iu-CA) AppleWebKit/534.19.7 (KHTML, like Gecko) Version/4.0.5 Mobile/8B116 Safari/6534.19.7


creditCard
----------

.. Method:: Method creditCard(card_type=Card Type)

**card_type** - :ref:`card_type` , Default By **random choice**

::

    In[0]: from pprint import pprint
    In[1]: from wsltools import faker
    In[2]: obj = faker()
    In[3]: pprint(obj.creditCard())
    Out[3]: 
    {'code': '529',
     'expire': '09/24',
     'first_name': 'Derek',
     'last_name': 'Barrett',
     'name': 'Derek Barrett',
     'number': '4375995106301',
     'security': 'CVC',
     'type': 'visa13',
     'type_full': 'VISA 13 digit'}


email
-----

.. Attribute:: Attribute email

::

    In[0]: from wsltools import faker
    In[1]: obj = faker()
    In[2]: obj.email
    Out[2]: wsmith@griffin-wright.biz


name
----

.. Attribute:: Attribute name

::

    In[0]: from wsltools import faker
    In[1]: obj = faker()
    In[2]: obj.name
    Out[2]: {'first_name': 'Lori', 'last_name': 'Williams', 'name': 'Lori Williams'}


ssn
---

.. Attribute:: Attribute ssn

::

    In[0]: from wsltools import faker
    In[1]: obj = faker()
    In[2]: obj.ssn
    Out[2]: 833-22-4862


phone
------

.. Attribute:: Attribute phone

::

    In[0]: from wsltools import faker
    In[1]: obj = faker()
    In[2]: obj.phone
    Out[2]: (062)144-8497x2311


job
---

.. Attribute:: Attribute job

::

    In[0]: from wsltools import faker
    In[1]: obj = faker()
    In[2]: obj.job
    Out[2]: Chartered legal executive (England and Wales)


company
--------

.. Attribute:: Attribute company

::

    In[0]: from wsltools import faker
    In[1]: obj = faker()
    In[2]: obj.company
    Out[2]: Kennedy PLC


address
-------

.. Attribute:: Attribute address

::

    In[0]: from wsltools import faker
    In[1]: obj = faker()
    In[2]: obj.address
    Out[2]: 
    01065 Armstrong Streets Apt. 665
    Markfort, AL 85969


.. _card_type:

Support Credit Card Types
-------------------------

* **maestro** - Maestro
* **discover** - Discover
* **jcb15** - JCB 15 digit
* **jcb16** - JCB 16 digit
* **visa13** - VISA 13 digit
* **visa16** - VISA 16 digit
* **visa19** - VISA 19 digit
* **mastercard** - Mastercard
* **amex** - American Express
* **diners** - Diners Club / Carte Blanch

If locale code use **fa_IR**:

* **ansar** - انصار
* **iran_zamin** - ایران زمین
* **hekmat** - حکمت
* **keshavarzi** - کشاورزی
* **shahr** - شهر
* **mehre_ghtesad** - مهراقتصاد
* **sarmayeh** - سرمایه
* **post_bank** - پست بانک
* **tose** - توسعه
* **eghtesad_novin** - اقتصاد نوین
* **meli** - ملی
* **pasargad** - پاسارگاد
* **tourism_bank** - گردشگری
* **ghavamin** - قوامین
* **day** - دی
* **mellat** - ملت
* **tejarat** - تجارت
* **mellal** - ملل
* **saman** - سامان
* **kosar** - کوثر
* **refah** - رفاه
* **saderat** - صادرات
* **tat** - تات
* **sina** - سینا
* **kar_afarin** - کار آفرین
* **sepah** - سپه
* **maskan** - مسکن
* **parsian** - پارسیان
* **bim** - صنعت و معدن


.. _locale_code:

Support Locales code
--------------------

* **ar_EG** - Arabic (Egypt)
* **ar_PS** - Arabic (Palestine)
* **ar_SA** - Arabic (Saudi Arabia)
* **bg_BG** - Bulgarian
* **bs_BA** - Bosnian
* **cs_CZ** - Czech
* **de_DE** - German
* **dk_DK** - Danish
* **el_GR** - Greek
* **en_AU** - English (Australia)
* **en_CA** - English (Canada)
* **en_GB** - English (Great Britain)
* **en_IN** - English (India)
* **en_NZ** - English (New Zealand)
* **en_US** - English (United States)
* **es_ES** - Spanish (Spain)
* **es_MX** - Spanish (Mexico)
* **et_EE** - Estonian
* **fa_IR** - Persian (Iran)
* **fi_FI** - Finnish
* **fr_FR** - French
* **hi_IN** - Hindi
* **hr_HR** - Croatian
* **hu_HU** - Hungarian
* **hy_AM** - Armenian
* **it_IT** - Italian
* **ja_JP** - Japanese
* **ka_GE** - Georgian (Georgia)
* **ko_KR** - Korean
* **lt_LT** - Lithuanian
* **lv_LV** - Latvian
* **ne_NP** - Nepali
* **nl_NL** - Dutch (Netherlands)
* **no_NO** - Norwegian
* **pl_PL** - Polish
* **pt_BR** - Portuguese (Brazil)
* **pt_PT** - Portuguese (Portugal)
* **ro_RO** - Romanian
* **ru_RU** - Russian
* **sl_SI** - Slovene
* **sv_SE** - Swedish
* **tr_TR** - Turkish
* **uk_UA** - Ukrainian
* **zh_CN** - Chinese (China)
* **zh_TW** - Chinese (Taiwan)