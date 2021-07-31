import re
import validators
from unittest import TestCase
import sys

url_regex = re.compile(
        r'^(?:(?:http|ftp)s?://)?' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

social_media_handle_regex = re.compile("^\s*(@?[A-Za-z0-9-_]+(?![@]))\s*$")

phone_regex = re.compile("^1?([0-9]{3})?[0-9]{7}$")

def any_in(possible_vals, container):
    for val in possible_vals:
        if val in container:
            return True
    return False


def fail(message):
    print(message, file=sys.stderr)
    exit(-1)


def normalize_phone(phone):
    translation_table = dict.fromkeys(map(ord, "+.-() \t"), None)
    return phone.translate(translation_table)


def validate_url(url):
    match = re.match(url_regex, url) is not None
    return match


def validate_email(email):
    result = validators.email(email)
    if isinstance(result, validators.ValidationFailure):
        result = False
    return result


def validate_phone(phone):
    phone = normalize_phone(phone)
    match = re.match(phone_regex, phone) is not None
    return match


def validate_handle(handle):
    match = re.match(social_media_handle_regex, handle) is not None
    return match


def validate_url_default(url, default=''):
    return validate_default(validate_url, url, default)


def validate_email_default(email, default=''):
    return validate_default(validate_email, email, default)


def validate_handle_default(handle, default=''):
    return validate_default(validate_handle, handle, default)


def validate_phone_default(phone, default=''):
    return validate_default(validate_phone, phone, default)


def validate_default(validator, s, default):
    if validator(s):
        return s
    else:
        return default


class _UrlValidatorTest(TestCase):
    def test_http(self):
        url = "http://google.com"
        self.assertEqual(validate_url(url), True)

    def test_www(self):
        url = "http://www.yourmom.com"
        self.assertEqual(validate_url(url), True)

    def test_no_http(self):
        url = "hi.com"
        self.assertEqual(validate_url(url), True)

    def test_subdomain(self):
        url = "hi.there.com"
        self.assertEqual(validate_url(url), True)

    def test_subdomain_resource(self):
        url = "hi.there.com/specific_resource?sfjdd=8&fddd=2"
        self.assertEqual(validate_url(url), True)

    def test_reject_whitespace(self):
        url = "hi.com/ rejected"
        self.assertEqual(validate_url(url), False)

    def test_non_url(self):
        url = "notawebsite/hello"
        self.assertEqual(validate_url(url), False)


class _EmailValidatorTest(TestCase):
    def test_email(self):
        email = "myname.jeff@gmail.com"
        self.assertEqual(validate_email(email), True)

    def test_nonemail(self):
        email = "notanemail.com"
        self.assertEqual(validate_email(email), False)


class _PhoneValidatorTest(TestCase):
    def test_phone(self):
        phone = "+1 (801).888.8888"
        self.assertEqual(validate_phone(phone), True)

    def test_notphone(self):
        phone = "888 888 8888 hi"
        self.assertEqual(validate_phone(phone), False)


class _HandleValidatorTest(TestCase):
    def test_handle_no_at(self):
        handle = "somehandle"
        self.assertEqual(validate_handle(handle), True)

    def test_handle_with_at(self):
        handle = "@twitteruser"
        self.assertEqual(validate_handle(handle), True)

    def test_handle_reject_email(self):
        handle = "not_a_handle@gmail.com"
        self.assertEqual(validate_handle(handle), False)

    def test_handle_reject_url(self):
        handle = "website.com"
        self.assertEqual(validate_handle(handle), False)