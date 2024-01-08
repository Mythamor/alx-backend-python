#!/usr/bin/env python3

"""
Module: test_utils
"""


import unittest
from unittest.mock import Mock, patch
import requests
from parameterized import parameterized
from utils import access_nested_map, get_json


class TestAccessNestedMap(unittest.TestCase):
    """
    unittest for tests utils.access_nested_map
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
        ])
    def test_access_nested_map(self, nested_map, path, expected_result):
        """
        method to test that the method returns
        what it is supposed to
        """
        self.assertEqual(access_nested_map(nested_map, path), expected_result)

    @parameterized.expand([
        ({}, ("a",), KeyError, "'a'"),
        ({"a": 1}, ("a", "b"), KeyError, "'b'")
        ])
    def test_access_nested_map_exception(self, nested_map, path, err, msg):
        """
        test for key error
        """
        with self.assertRaises(err) as context:
            access_nested_map(nested_map, path)

        self.assertEqual(str(context.exception), msg)


class TestGetJson(unittest.TestCase):
    """
    Tests getting a json file
    """
    @patch('utils.requests.get')
    def test_get_json(self, mock_get):
        """
        Tests for utils get json method
        """

        # Define test data
        test_data = [
            {"url": "http://example.com", "payload": {"payload": True}},
            {"url": "http://holberton.io", "payload": {"payload": False}},
        ]

        for data in test_data:
            # Configure mock to return a Mock object with a json mehod
            mock_json = Mock(return_value=data["payload"])
            mock_response = Mock(json=mock_json)
            mock_get.return_value = mock_response

            # Call get_json with the test_data
            result = get_json(data["url"])

            # Assert mocked get method was called exactly once
            mock_get.assert_called_once_with(data["url"])

            # Assert get_json output is equal to expected payload
            self.assertEqual(result, data["payload"])

            # Reset mock for next iteration
            mock_get.reset_mock()


if __name__ == "__main__":
    unittest.main()
