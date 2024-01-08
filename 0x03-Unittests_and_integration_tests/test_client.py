#!/usr/bin/env python3

"""
Module: test_client
"""

import unittest
from typing import Dict
from unittest.mock import Mock, MagicMock, PropertyMock, patch
from parameterized import parameterized
from client import GithubOrgClient


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
