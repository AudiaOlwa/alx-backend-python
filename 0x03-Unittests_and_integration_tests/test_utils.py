#!/usr/bin/env python3

#Unit tests for utils.access_nested_map

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map
from utils import access_nested_map, get_json, memoize



class TestAccessNestedMap(unittest.TestCase):
   # """Unit tests for access_nested_map function"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
       # """Test that access_nested_map returns expected result"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test that access_nested_map raises KeyError for invalid path"""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        # Check that the exception message is the last key in the path
        self.assertEqual(str(cm.exception), f"'{path[-1]}'")

class TestGetJson(unittest.TestCase):
    """Unit tests for get_json function"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch("utils.requests.get")
    def test_get_json(self, test_url, test_payload, mock_get):
        """Test get_json returns expected payload without making HTTP calls"""
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = get_json(test_url)

        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)



class TestMemoize(unittest.TestCase):
    """Unit tests for memoize decorator"""

    def test_memoize(self):
        """Test that memoize caches method results"""

        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        obj = TestClass()
        with patch.object(obj, 'a_method', return_value=42) as mocked_method:
            # Call a_property twice
            result1 = obj.a_property
            result2 = obj.a_property

            # Ensure a_method is called only once
            mocked_method.assert_called_once()

            # Ensure both results are correct
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)



if __name__ == "__main__":
    unittest.main()
