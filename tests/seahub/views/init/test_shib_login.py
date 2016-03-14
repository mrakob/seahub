from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.http import urlquote

from seahub.test_utils import BaseTestCase


class ShibLoginTest(BaseTestCase):
    def test_default(self):
        assert getattr(settings, 'ENABLE_SHIB_LOGIN', False) is False

        resp = self.client.get(reverse('shib_login'))
        self.assertEqual(404, resp.status_code)

    def test_login(self):
        assert getattr(settings, 'ENABLE_SHIB_LOGIN', False) is False

        with self.settings(ENABLE_SHIB_LOGIN=True):
            assert settings.ENABLE_SHIB_LOGIN is True
            resp = self.client.get(reverse('shib_login'))
            self.assertEqual(302, resp.status_code)
            self.assertRegexpMatches(resp['Location'], r'http://testserver/home/my/')

    def test_bad_redirect(self):
        assert getattr(settings, 'ENABLE_SHIB_LOGIN', False) is False

        with self.settings(ENABLE_SHIB_LOGIN=True):
            assert settings.ENABLE_SHIB_LOGIN is True
            resp = self.client.get(reverse('shib_login') + '?next=' + urlquote('http://testserver\@example.com'))
            self.assertEqual(302, resp.status_code)
            self.assertRegexpMatches(resp['Location'], r'http://testserver' + settings.LOGIN_REDIRECT_URL)
