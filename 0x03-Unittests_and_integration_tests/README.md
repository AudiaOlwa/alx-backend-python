# Unittests and Integration Tests

## Project Overview
This project introduces **unit testing** and **integration testing** in Python.  
You will learn how to:
- Differentiate between unit tests and integration tests
- Apply common testing patterns such as mocking, parametrization, and fixtures
- Write clean and maintainable test files using the `unittest` framework

All tasks must follow Python’s `pycodestyle` and include proper documentation.

---

## Requirements
- Python 3.7, Ubuntu 18.04 LTS
- All files must be executable
- All modules, classes, and functions must have documentation
- All functions and coroutines must include type annotations
- Tests should be run with:

```bash
python -m unittest path/to/test_file.py


# 0x03. Unittests and Integration Tests

This project covers the concepts of **unit testing**, **integration testing**, **mocking**, **parameterization**, and **memoization** in Python.

## Project Overview

Python `unittest` framework is used along with `unittest.mock` for mocking external calls. Parameterization is done with `parameterized.expand`. The project is structured to ensure:

- Functions return expected results for standard and edge cases.
- External HTTP or database calls are **mocked**.
- Memoization caches results to avoid repeated computation.

---

## 1. Unit Testing `access_nested_map`

**File:** `test_utils.py`  
**Function tested:** `utils.access_nested_map`

- Tests that `access_nested_map` returns the expected value for a given nested map and path.
- Uses `@parameterized.expand` to test multiple inputs.
- Handles cases where the path does not exist using `assertRaises` to ensure a `KeyError` is raised.
- Example inputs:
  - `{"a": 1}, ("a",)` → `1`
  - `{"a": {"b": 2}}, ("a", "b")` → `2`
  - `{"a": 1}, ("a", "b")` → raises `KeyError`

---

## 2. Unit Testing `get_json`

**File:** `test_utils.py`  
**Function tested:** `utils.get_json`

- Tests that `get_json` returns the expected JSON payload.
- Uses `unittest.mock.patch` to mock `requests.get`.
- Parameterized test with different URLs and payloads:
  - `"http://example.com", {"payload": True}`
  - `"http://holberton.io", {"payload": False}`
- Ensures `requests.get` is called **exactly once** per input.
- No real HTTP requests are made.

---

## 3. Testing `memoize` decorator

**File:** `test_utils.py`  
**Function tested:** `utils.memoize`

- Tests that the `memoize` decorator caches the result of a method.
- Uses a test class with a method `a_method` and a memoized property `a_property`.
- Mocks `a_method` to ensure it is called only **once** even when `a_property` is accessed multiple times.

---

## 4. Testing `GithubOrgClient`

**File:** `test_client.py`  
**Class tested:** `client.GithubOrgClient`

- Tests the `org` property of `GithubOrgClient`.
- Uses `@parameterized.expand` to run the test for multiple organization names:
  - `"google"`
  - `"abc"`
- Uses `@patch("client.get_json")` as a decorator to mock the external HTTP request.
- Verifies that:
  - `get_json` is called **once** with the correct URL.
  - The `org` property returns the mocked payload.
- No real HTTP calls are made.

---

## How to Run Tests

From the root directory:

```bash
# Discover and run all tests in the folder
python -m unittest discover -s 0x03-Unittests_and_integration_tests -p "*.py" -v
