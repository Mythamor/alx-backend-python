#!/usr/bin/env python3

"""
Module: test_client
"""

import unittest
from typing import Dict
from unittest.mock import Mock, MagicMock, PropertyMock, patch
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """
    Class that test the client.GithubOrgClient class
    """
    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"})
        ])
    @patch("client.get_json")
    def test_org(self, org: str, expected_response: Dict,
                 mocked_function: MagicMock) -> None:
        """
        Test for the github org method
        """
        mocked_function.return_value = MagicMock(
            return_value=expected_response)
        goclient = GithubOrgClient(org)
        self.assertEqual(goclient.org(), expected_response)
        mocked_function.assert_called_once_with(
            "https://api.github.com/orgs/{}".format(org)
        )

    def test_public_repos_url(self) -> None:
        """
        unit-test GithubOrgClient._public_repos_url
        """
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {
                    'repos_url': "https://api.github.com/users/google/repos"}
            self.assertEqual(GithubOrgClient("google")._public_repos_url,
                             "https://api.github.com/users/google/repos")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json: MagicMock) -> None:
        """
        unit-test GithubOrgClient.public_repos
        """
        test_payload = {'repos': [
            {
                "name": "signet",
                "private": False,
                "owner": {"login": "googleapi", "id": 16785467},
            },
            {
                "name": "ruby-openid-apps-discovery",
                "private": False,
                "owner": {"login": "google", "id": 1342004},
            },
        ]}

        mock_get_json.return_value = test_payload['repos']

        org_client = GithubOrgClient("googleapis")

        # Mock the _public_repos_url property
        with patch("client.GithubOrgClient._public_repos_url",
                   new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = org_client
            self.assertEqual(
                GithubOrgClient("googleapis").public_repos(),
                [
                    "signet",
                    "ruby-openid-apps-discovery",
                ],
            )
            mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once()

    @parameterized.expand([
        ({'license': {'key': "bsd-3-clause"}}, "bsd-3-clause", True),
        ({'license': {'key': "bsl-1.0"}}, "bsd-3-clause", False),
    ])
    def test_has_license(self, repo: Dict, key: str, expected: bool) -> None:
        """Tests the `has_license  method"""
        gh_org_client = GithubOrgClient("google")
        client_has_licence = gh_org_client.has_license(repo, key)
        self.assertEqual(client_has_licence, expected)


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Testing for Github Integrations
    """
    @classmethod
    def setUpClass(cls) -> None:
        """
        Method to setup
        """
        route_payload = {
            'https://api.github.com/orgs/google': cls.org_payload,
            'https://api.github.com/orgs/google/repos': cls.repos_payload,
        }

        def get_payload(url):
            if url in route_payload:
                return Mock(**{'json.return_value': route_payload[url]})
            return HTTPError

        cls.get_patcher = patch("requests.get", side_effect=get_payload)
        cls.get_patcher.start()

    def test_public_repos(self) -> None:
        """_
        Test for public repos
        """
        self.assertEqual(
            GithubOrgClient("google").public_repos(),
            self.expected_repos,
        )

    def test_public_repos_with_license(self) -> None:
        """
        test for public repos license
        """
        self.assertEqual(
            GithubOrgClient("google").public_repos(license="apache-2.0"),
            self.apache2_repos,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Method to teardown
        """
        cls.get_patcher.stop()
