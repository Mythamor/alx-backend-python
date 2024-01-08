#!/usr/bin/env python3

"""
Module: test_utils
"""


import unittest
from unittest.mock import Mock, patch
import requests
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


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

    # Parametize output
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])

    def test_get_json(self, url, expected_output):
        """
        Tests for utils get json method
        """
        # Create  Mock object with a json method
        mock_json = Mock()
        mock_json.json.return_value = expected_output

        with patch('requests.get', return_value = mock_json):
            # Call get_json with the url
            result = get_json("url")

            # Assert get_json output is equal to expected payload
            self.assertEqual(result, expected_output)

            # Reset mock for next iteration
            mock_json.reset_mock()


class TestMemoize(unittest.TestCase):
    """
    Parameterize and patch with memoize
    """
    def test_memoize(self):
        """
        Test the memoize decorator
        """
        class TestClass:

            def a_method(self):
                """
                a_method returns 42
                """
                return 42

            @memoize
            def a_property(self):
                """
                a_property returns a_method
                """
                return self.a_method()
        
        test_instance = TestClass()
        
        # Use patch.object to mock a_method
        with patch.object(test_instance, 'a_method', 
                return_value=42) as mock_a_method:
            
            # Call a_property twice
            result1 = test_instance.a_property
            result2 = test_instance.a_property

            # Assert a_method was only called once
            mock_a_method.assert_called_once()

            # Assert that results are correct
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)


if __name__ == "__main__":
    unittest.main()
