#!/usr/bin/env python3
"""
Unittests for GithubOrgClient.
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """
    Test GithubOrgClient class.
    """

    # TASK 4
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """
        Test GithubOrgClient.org method.
        """
        mock_get_json.return_value = {"key": "value"}
        client = GithubOrgClient(org_name)
        result = client.org
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, {"key": "value"})

    # TASK 5
    def test_public_repos_url(self):
        """
        Test GithubOrgClient._public_repos_url property.
        """
        payload = {"repos_url": "https://api.github.com/orgs/test_org/repos"}
        client = GithubOrgClient("test_org")
        with patch.object(
            GithubOrgClient,
            "org",
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = payload
            result = client._public_repos_url
            self.assertEqual(result, payload["repos_url"])

    # TASK 6
    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """
        Test GithubOrgClient.public_repos method.
        """
        # Payload que get_json renverra
        repo_payload = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_json.return_value = repo_payload

        # Valeur mockée pour _public_repos_url
        mock_url = "https://api.github.com/orgs/test_org/repos"
        client = GithubOrgClient("test_org")

        # Patch de la propriété _public_repos_url
        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock
        ) as mock_repos_url:
            mock_repos_url.return_value = mock_url
            result = client.public_repos()

            # Vérifications
            self.assertEqual(result, ["repo1", "repo2"])
            mock_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(mock_url)
