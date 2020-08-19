# Tests

## Pytest
We are using [pytest](docs.pytest.org) and follow the [best practices](https://docs.pytest.org/en/latest/goodpractices.html#goodpractices) for tests. The test layout we follow is:
```
setup.py
chooserbot/
    __init__.py
    x.py
tests/
    test_x.py
```

## Running tests
To run tests, do the following:
```sh
pip install -e . # Install package using setup.py in editable mode
python
```