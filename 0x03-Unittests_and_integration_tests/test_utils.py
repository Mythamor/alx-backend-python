#!/usr/bin/env python3

"""
Module: test_utils
"""


import unittest
from parameterized import parameterized
from utils import access_nested_map


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
        ({"a":1}, ("a", "b"), KeyError, "'b'")
        ])
    def test_access_nested_map_exception(self, nested_map, path, err, msg):
        """
        test for key error
        """
        with self.assertRaises(err) as context:
            access_nested_map(nested_map, path)
        
        self.assertEqual(str(context.exception), msg)


if __name__ == "__main__":
    unittest.main()
