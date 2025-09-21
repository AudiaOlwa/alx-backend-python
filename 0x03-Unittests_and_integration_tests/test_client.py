#!/usr/bin/env python3
"""
Unittests for GithubOrgClient.
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized_class, parameterized
import fixtures
import requests
from client import GithubOrgClient


# ----------------------------------------------------------------------
# Définition des fixtures locales pour l'intégration
org_payload = {
    "login": "test_org",
    "repos_url": "https://api.github.com/orgs/test_org/repos"
}

repos_payload = [
    {"name": "repo1", "license": {"key": "apache-2.0"}},
    {"name": "repo2", "license": {"key": "mit"}},
    {"name": "repo3", "license": {"key": "apache-2.0"}}
]

expected_repos = ["repo1", "repo2", "repo3"]
apache2_repos = ["repo1", "repo3"]

# ----------------------------------------------------------------------


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

    # TASK 7
    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Test GithubOrgClient.has_license method.
        """
        client = GithubOrgClient("test_org")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)

# ----------------------------------------------------------------------
# TASK 8 & 9: Integration tests


class MockResponse:
    """
    Mock response object for requests.get().json() used in integration tests.
    """

    def __init__(self, payload):
        self._payload = payload
        
    def json(self):
        """
        Return the payload of the mock response.
        """
        return self._payload


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    [(org_payload, repos_payload, expected_repos, apache2_repos)],
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration tests for GithubOrgClient.public_repos.
    """

    @classmethod
    def setUpClass(cls):
        """
        Start patcher for requests.get and mock JSON responses.
        """
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        def side_effect(url):
            if url == "https://api.github.com/orgs/test_org":
                return MockResponse(cls.org_payload)
            if url == cls.org_payload.get("repos_url"):
                return MockResponse(cls.repos_payload)
            return None

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """
        Stop patcher for requests.get.
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        Test that public_repos returns all expected repos.
        """
        client = GithubOrgClient("test_org")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """
        Test that public_repos returns repos filtered by license.
        """
        client = GithubOrgClient("test_org")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )


if __name__ == "__main__":
    unittest.main()
