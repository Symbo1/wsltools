from .. import Provider as InternetProvider


class Provider(InternetProvider):

    user_name_formats = (
        '{{last_name}}.{{first_name_female}}',
        '{{last_name}}.{{first_name_male}}',
        '{{first_name_female}}.{{last_name}}',
        '{{first_name_male}}.{{last_name}}',
        '{{first_name}}##',
    )

    email_formats = ('{{user_name}}@{{free_email_domain}}', )

    free_email_domains = (
        'gmail.com', 'siol.net', 'email.si', 'volja.net',
    )

    tlds = ('si', 'com')
