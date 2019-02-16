# dtm
Smart datetime objects

## dt objects
The main thing dtm exports is the 'dt' object. It wraps a standard Python
datetime object so that we can effectively add functionality to the
datetime class.

We wrap datetime rather than inheriting from it because we ran into issues
with the inheritance strategy.

The recommended method of import is:

    from dtm import dt

### constructor
The dt object constructor will accept several argument schemes

#### no arguments

    myobj = dt()

Create a dt object containing the current date and time. Effectively the same as

    myobj = datetime().now()

#### a datetime object
    myobj = dt(datetime(2011, 10, 9))

#### a list of ints
    myobj = dt(2011, 10, 9)


## My setup

    dtm                         # project directory
    |
    +- .coveragerc              # parameters for test coverage
    +- .env                     # set env upon cd into this directory (autoenv)
    +- .gitignore               # tell git which files to ignore
    +- LICENSE                  # license for this software
    +- Makefile                 # document command lines for tests and such
    +- README.md                # this file
    +- pytest.ini               # parameters for pytest
    +- requirements.txt         # items this project depends on
    |
    +- dtm                      # source directory
    |   |
    |   +- __init__.py          # the payload source code
    |
    +- tests                    # tests directory
    |   |
    |   +- conftest.py          # test configurations
    |   +- test_0_quality.py    # code quality tests
    |   +- test_1_dt.py         # functionality tests
    |
    +- venv                     # virtual environment
