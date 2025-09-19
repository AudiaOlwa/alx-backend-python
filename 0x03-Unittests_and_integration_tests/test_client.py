#!/usr/bin/env python3
"""
Unit tests for the client module.

Covers:
- GithubOrgClient.org method
"""

import unittest
from parameterized import parameterized
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """
    Unit tests for GithubOrgClient class
    """

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value and
        calls get_json once with the expected URL.
        """
        # Configure the mock to return a test payload
        test_payload = {"login": org_name}
        mock_get_json.return_value = test_payload

        # Instantiate the client and access the org property
        client = GithubOrgClient(org_name)
        result = client.org  # org is a @memoize property

        # Ensure get_json was called once with the correct URL
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

        # Ensure the org property returns the mocked payload
        self.assertEqual(result, test_payload)

    def test_public_repos_url(self):
        """Test GithubOrgClient._public_repos_url property"""
        fake_payload = {"repos_url": "http://fakeurl.com/repos"}

        # Patch la propriété 'org' avec PropertyMock
        with patch("client.GithubOrgClient.org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = fake_payload
            client = GithubOrgClient("any_org")
            result = client._public_repos_url
            self.assertEqual(result, fake_payload["repos_url"])

if __name__ == "__main__":
    unittest.main()
