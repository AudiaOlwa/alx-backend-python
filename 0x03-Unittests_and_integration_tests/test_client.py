#!/usr/bin/env python3
"""
Unit tests for the client module.

Covers:
- GithubOrgClient.org method
"""
import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
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
        result = client.org

        # Ensure get_json was called once with the correct URL
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

        # Ensure the org property returns the mocked payload
        self.assertEqual(result, test_payload)


if __name__ == "__main__":
    unittest.main()
