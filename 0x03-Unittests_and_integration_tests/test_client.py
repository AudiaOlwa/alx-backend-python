import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    @parameterized.expand([
        ('google', {'name': 'Google LLC'}),
        ('abc', {'name': 'ABC Corporation'})
    ])
    @patch('client.get_json', autospec=True)
    def test_org(self, org_name, expected_data, mock_get_json):
        """
        Test que GithubOrgClient.org retourne les données correctes pour différentes organisations
        
        Args:
            org_name (str): Nom de l'organisation à tester
            expected_data (dict): Données attendues
            mock_get_json (Mock): Mock du client HTTP
        """
        # Configuration du mock
        mock_get_json.return_value = expected_data
        
        # Création du client et appel de la méthode testée
        github_org_client = GithubOrgClient(org_name)
        result = github_org_client.org
        
        # Vérifications
        self.assertEqual(result, expected_data)
        mock_get_json.assert_called_once()
        url = f'https://api.github.com/orgs/{org_name}'
        mock_get_json.assert_called_with(url)