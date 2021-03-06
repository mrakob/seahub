import json

from constance import config
from seaserv import seafile_api, ccnet_threaded_rpc

from seahub.test_utils import BaseTestCase


class RepoPublicTest(BaseTestCase):
    def setUp(self):
        self.repo_id = self.create_repo(name='test-admin-repo', desc='',
                                        username=self.admin.username,
                                        passwd=None)
        self.url = '/api2/repos/%s/public/' % self.repo_id
        self.user_repo_url = '/api2/repos/%s/public/' % self.repo.id

        config.ENABLE_USER_CREATE_ORG_REPO = 1

    def tearDown(self):
        self.remove_repo(self.repo_id)
        # clear cache between every test case to avoid config option cache issue
        self.clear_cache()

    def test_admin_can_set_pub_repo(self):
        self.login_as(self.admin)

        resp = self.client.post(self.url)
        self.assertEqual(200, resp.status_code)
        json_resp = json.loads(resp.content)
        assert json_resp['success'] is True

    def test_admin_can_unset_pub_repo(self):
        seafile_api.add_inner_pub_repo(self.repo_id, "r")

        self.login_as(self.admin)

        resp = self.client.delete(self.url)
        self.assertEqual(200, resp.status_code)
        json_resp = json.loads(resp.content)
        assert json_resp['success'] is True

    def test_user_can_set_pub_repo(self):
        self.login_as(self.user)

        resp = self.client.post(self.user_repo_url)
        self.assertEqual(200, resp.status_code)
        json_resp = json.loads(resp.content)
        assert json_resp['success'] is True

    def test_admin_can_set_pub_repo_when_setting_disalbed(self):
        assert bool(config.ENABLE_USER_CREATE_ORG_REPO) is True
        config.ENABLE_USER_CREATE_ORG_REPO = False
        assert bool(config.ENABLE_USER_CREATE_ORG_REPO) is False

        self.login_as(self.admin)

        resp = self.client.post(self.url)
        self.assertEqual(200, resp.status_code)
        json_resp = json.loads(resp.content)
        assert json_resp['success'] is True

    def test_user_can_not_set_pub_repo_when_setting_disalbed(self):
        assert bool(config.ENABLE_USER_CREATE_ORG_REPO) is True
        config.ENABLE_USER_CREATE_ORG_REPO = False
        assert bool(config.ENABLE_USER_CREATE_ORG_REPO) is False

        self.login_as(self.user)

        resp = self.client.post(self.user_repo_url)
        self.assertEqual(403, resp.status_code)
        json_resp = json.loads(resp.content)
        assert json_resp['error_msg'] == 'Permission denied.'
