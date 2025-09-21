#!/usr/bin/env python3
"""Unit tests for the client module.

Covers:
- GithubOrgClient.org method
- GithubOrgClient._public_repos_url property
- GithubOrgClient.public_repos method
"""
import unittest
from parameterized import parameterized
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient

class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient class"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct value and calls get_json"""
        test_payload = {"login": org_name}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        result = client.org

        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)
        self.assertEqual(result, test_payload)

    def test_public_repos_url(self):
        """Test GithubOrgClient._public_repos_url property"""
        fake_payload = {"repos_url": "http://fakeurl.com/repos"}

        with patch("client.GithubOrgClient.org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = fake_payload
            client = GithubOrgClient("any_org")
            result = client._public_repos_url
            self.assertEqual(result, fake_payload["repos_url"])

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos method"""
        fake_repos_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": {"key": "mit"}},
        ]
        mock_get_json.return_value = fake_repos_payload

        with patch("client.GithubOrgClient._public_repos_url",
                   new_callable=PropertyMock) as mock_url:
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


if __name__ == "__main__":
    unittest.main()
