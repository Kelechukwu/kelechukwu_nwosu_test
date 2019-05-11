# Overlap Function
**Version**: Python3.X

This function accepts two lines (x1,x2) and (x3,x4) on the x-axis and returns whether they overlap.
As an example, (1,5) and (2,6) overlaps but not (1,5) and (6,8).

## Usage
You can import the overlap function and use it. Below is an example using 
python3 terminal

```bash
$ python3
```
```python
>>> from overlap import overlap
>>> overlap((1,5), (6,8))
False
```
## Contributing
### Testing

| Test file  | Usuage   |
| ----------------------|:--------------------------------------:|
| test_overlap.py | Tests for the overlap function reside here |

### How to run tests
```bash
$ python test_overlap.py
```
