# -*- coding: utf-8 -*-

__author__ = 'CongRong <tr3jer@gmail.com>'


'''
Data source:
/usr/share/i18n/SUPPORTED
https://github.com/joke2k/faker
Other data is provided by the official list of country.
'''

import random
from .utils import faker as fakerOrigin
from .utils.UAS import USER_AGENTS


class faker():
	def __init__(self, locale='en_US'):
		'''
		:param locale: locales language code
		'''

		self.locale = locale

		self.language_locale_codes = ['fi_FI', 'uk_UA', 'ar_AA', 'et_EE', 'fil_PH', 'dk_DK', 'en_CA', 'nl_NL', 'el_CY', 'hr_HR',
		                     'en_NZ', 'de', 'ka_GE', 'en_PH', 'he_IL', 'en_US', 'ta_IN', 'es', 'hi_IN', 'zh_TW',
		                     'en_TH', 'bg_BG', 'ro_RO', 'pt_BR', 'de_DE', 'fa_IR', 'tl_PH', 'fr_FR', 'sk_SK', 'la',
		                     'mt_MT', 'de_AT', 'sl_SI', 'ko_KR', 'tr_TR', 'ru_R', 'fr_QC', 'lt_LT', 'ar_JO', 'en_GB',
		                     'id_ID', 'ja_JP', 'de_CH', 'en_IE', 'es_ES', 'pl_PL', 'lb_L', 'ar_PS', 'en', 'lv_LV',
		                     'tw_GH', 'no_NO', 'ne_NP', 'es_CA', 'es_MX', 'it_IT', 'hy_AM', 'en_A', 'nl_BE', 'sv_SE',
		                     'el_GR', 'cs_CZ', 'fr_CH', 'zh_CN', 'ar_SA', 'th_TH', 'ar_EG', 'pt_PT', 'bs_BA', 'hu_H']

		try:
			self.localeUse = fakerOrigin.Faker(self.locale)
		except:
			raise ValueError('locale-code not support!')

		self.USER_AGENTS = USER_AGENTS


	def __repr__(self):
		return "<class: {} {}>".format(self.__class__.__name__, self.locale)


	@property
	def email(self):
		return self.localeUse.email()


	@property
	def address(self):
		return self.localeUse.address()


	@property
	def company(self):
		return self.localeUse.company()


	@property
	def job(self):
		return self.localeUse.job()


	@property
	def phone(self):
		return self.localeUse.phone_number()


	@property
	def ssn(self):
		return self.localeUse.ssn()


	@property
	def name(self):
		'''
		:return: person name with out prefix/suffix
		'''
		name = {}
		name['first_name'] = self.localeUse.first_name()
		name['last_name'] = self.localeUse.last_name()
		#todo 解释去除自带的prefix
		if ' ' in self.localeUse.name():
			name['name'] = name['first_name'] + ' ' + name['last_name']
		else:
			name['name'] = name['last_name'] + name['first_name']

		return name


	def creditCard(self, card_type=None, name={}):
		'''
		:param card_type: card_type_dict: values
		:param name: [optional] self use
		:return: dict
		'''
		card_type_dict = {
			'maestro': 'Maestro',
			'discover': 'Discover',
			'jcb15': 'JCB 15 digit',
			'jcb16': 'JCB 16 digit',
			'visa13': 'VISA 13 digit',
			'visa16': 'VISA 16 digit',
			'visa19': 'VISA 19 digit',
			'mastercard': 'Mastercard',
			'amex': 'American Express',
			'diners': 'Diners Club / Carte Blanche'
		}

		card_type_dict_fa_ir = {
			'ansar': 'انصار',
			'iran_zamin': 'ایران زمین',
			'hekmat': 'حکمت',
			'keshavarzi': 'کشاورزی',
			'shahr': 'شهر',
			'mehre_ghtesad': 'مهراقتصاد',
			'sarmayeh': 'سرمایه',
			'post_bank': 'پست بانک',
			'tose': 'توسعه',
			'eghtesad_novin': 'اقتصاد نوین',
			'meli': 'ملی',
			'pasargad': 'پاسارگاد',
			'tourism_bank': 'گردشگری',
			'ghavamin': 'قوامین',
			'day': 'دی',
			'mellat': 'ملت',
			'tejarat': 'تجارت',
			'mellal': 'ملل',
			'saman': 'سامان',
			'kosar': 'کوثر',
			'refah': 'رفاه',
			'saderat': 'صادرات',
			'tat': 'تات',
			'sina': 'سینا',
			'kar_afarin': 'کار آفرین',
			'sepah': 'سپه',
			'maskan': 'مسکن',
			'parsian': 'پارسیان',
			'bim': 'صنعت و معدن'
		}

		cardData = {}
		if self.locale.lower() == 'fa_ir':
			cardData['type'] = card_type if card_type else random.choice(list(card_type_dict_fa_ir.keys()))
			cardData['type_full'] = card_type_dict_fa_ir[cardData['type']]
		else:
			cardData['type'] = card_type if card_type else random.choice(list(card_type_dict.keys()))
			cardData['type_full'] = card_type_dict[cardData['type']]

		cardTmp = self.localeUse.credit_card_full(card_type=cardData['type']).split('\n')


		if not name:
			nameTmp = self.name
			cardData['name'] = nameTmp['name']
			cardData['first_name'] = nameTmp['first_name']
			cardData['last_name'] = nameTmp['last_name']
		else:
			cardData['name'] = name['name']
			cardData['first_name'] = name['first_name']
			cardData['last_name'] = name['last_name']

		cardData['number'] = cardTmp[2].split(' ')[0]
		cardData['expire'] = cardTmp[2].split(' ')[1]
		cardData['security'] = ''.join(list(filter(str.isalpha, str(cardTmp[3]))))
		cardData['code'] = ''.join(list(filter(str.isdigit, str(cardTmp[3]))))

		return cardData


	@property
	def profile(self):
		'''
		:return: website, username, name, residence, company, address, birthDate, sex, phone, job, ssn, mail, creditCard
		'''
		profileTmp = self.localeUse.profile()
		nameTmp = self.name
		profileTmp['name'] = nameTmp['name']
		profileTmp['first_name'] = nameTmp['first_name']
		profileTmp['last_name'] = nameTmp['last_name']
		profileTmp['phone'] = self.phone
		profileTmp['website'] = profileTmp['website'][0]
		profileTmp['credit_card'] = self.creditCard(name={
			'name': profileTmp['name'],
			'first_name': profileTmp['first_name'],
			'last_name': profileTmp['last_name']
		})
		return profileTmp


	def userAgent(self, platform='desktop'):
		if platform.lower() == 'mobile':
			return random.choice(self.USER_AGENTS['Mobile'])
		else:
			return random.choice(self.USER_AGENTS['Desktop'])
