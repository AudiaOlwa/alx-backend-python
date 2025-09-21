#!/usr/bin/env python3
"""Unit tests for the client module.

Covers:
- GithubOrgClient.org method
- GithubOrgClient._public_repos_url property
- GithubOrgClient.public_repos method
"""
import unittest
from parameterized import parameterized
from parameterized import parameterized_class
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient
import requests
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos

class TestGithubOrgClient(unittest.TestCase):
    """
    Unit tests for GithubOrgClient class
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns correct value and calls get_json
        """
        test_payload = {"login": org_name}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        result = client.org

        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)
        self.assertEqual(result, test_payload)

    def test_public_repos_url(self):
        """
        Test GithubOrgClient._public_repos_url property
        """
        fake_payload = {"repos_url": "http://fakeurl.com/repos"}
        with patch(
            "client.GithubOrgClient.org",
            new_callable=PropertyMock,
        ) as mock_org:
            mock_org.return_value = fake_payload
            client = GithubOrgClient("any_org")
            result = client._public_repos_url
            self.assertEqual(result, fake_payload["repos_url"])

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """
        Test GithubOrgClient.public_repos method
        """
        fake_repos_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": {"key": "mit"}},
        ]
        mock_get_json.return_value = fake_repos_payload

        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock,
        ) as mock_url:
            mock_url.return_value = "http://fakeurl.com/repos"
            client = GithubOrgClient("any_org")

            # Test without license filter
            repos = client.public_repos()
            self.assertEqual(repos, ["repo1", "repo2", "repo3"])

            # Test with license filter
            repos_mit = client.public_repos(license="mit")
            self.assertEqual(repos_mit, ["repo1", "repo3"])

            mock_url.assert_called_once()
            mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Test GithubOrgClient.has_license static method
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)

#exercice8
org_payload = {"repos_url": "https://api.github.com/orgs/test_org/repos"}
repos_payload = [
    {"name": "repo1", "license": {"key": "apache-2.0"}},
    {"name": "repo2", "license": {"key": "mit"}}
]
expected_repos = ["repo1", "repo2"]
apache2_repos = ["repo1"]

class MockResponse:
    """Helper class to mock requests.Response with .json()"""
    def __init__(self, payload):
        self._payload = payload

    def json(self):
        return self._payload


@parameterized_class(
    ('org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'),
    [
        (org_payload, repos_payload, expected_repos, apache2_repos)
    ]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Start patcher for requests.get with side_effect based on URL"""
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        # Side effect depending on URL
        def side_effect(url, *args, **kwargs):
            if url == GithubOrgClient.ORG_URL.format(org="test_org"):
                return MockResponse(cls.org_payload)
            elif url == cls.org_payload["repos_url"]:
                return MockResponse(cls.repos_payload)
            return MockResponse({})

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns the expected repo list"""
        client = GithubOrgClient("test_org")
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test that public_repos filters correctly by license"""
        client = GithubOrgClient("test_org")
        repos = client.public_repos(license="apache-2.0")
        self.assertEqual(repos, self.apache2_repos)
if __name__ == "__main__":
    unittest.main()
