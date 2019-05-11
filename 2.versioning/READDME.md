# How to install versioning library
**Version**: Python3.X 
```bash
$ cd versioning
$ python setup.py install
```

## Usage
After the library has been installed. You can import it and start using in your projects
Example:
```python
>>> from version import compare
>>> compare("1.3","4.5")
'1.3 < 4.5'
```
## Contributing
### Testing
The versioning library has a `tests` directory in which all testcases reside. Below is a summary

| Test file  | Usuage   |
| ----------------------|:--------------------------------------:|
| tests/test_helpers.py | Tests for helper functions reside here |
| tests/test_utils.py   | This is where all the name library function tests reside |

### How to run tests
```bash
$ cd versioning
$ python tests/test_helpers.py
$ python tests/test_utils.py
```
