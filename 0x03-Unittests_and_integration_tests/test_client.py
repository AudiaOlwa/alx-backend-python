#!/usr/bin/env python3
#!/usr/bin/env python3
import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient
#Task4
class TestGithubOrgClient(unittest.TestCase):
    """
    Test GithubOrgClient class.
    """

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """
        Test GithubOrgClient.org method.
        """
        mock_get_json.return_value = {"key": "value"}
        client = GithubOrgClient(org_name)
        result = client.org()
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, {"key": "value"})
