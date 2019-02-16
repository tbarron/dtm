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

#### a list of ints (year, month, day, hour, minute, second)
    myobj = dt(2011, 10, 9)

At least year, month, and day are required. Hour, minute, and second are
all optional, although somewhat interdependent. For example, because they
are positional, you can't provide second without providing minute.

#### a string
    myobj = dt("2011-10-09 20:07:06")

The code tries to intuit the format of the provided date/time string. Most
popular formats should work.

#### a datetime object
If you have a datetime object and want a dt object, the dt can be
initialized directly from the datetime.

    myobj = dt(datetime(2011, 10, 9))

The microsecond member will be zeroed out.

#### another dt object
Similarly, if you have a dt and want another, just pass in the one you've
got:

    newobj = dt(myobj)

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
