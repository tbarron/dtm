# dtm - smart datetime objects
Functionality added to datetime:

  * Initialize from date/time strings, intuiting format (no need to call
    strptime())
  * Initialize current date/time from no arguments (no need to call .now())
  * Easy way to jump forward and backward a day at a time
  * Easy way to get date of next Monday, next Friday, etc.
  * Iterate over a range of dates

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

### Comparison
dt objects can be compared for ==, <, or <= to other dt objects and to
datetime objects.

### Iteration by day
    for day in dt(2011, 10, 1).dt_range(dt(2011, 10, 31)):
        # do whatever

Unlike other Python range functions, the dt_range() function is inclusive.
That is, the above loop will process 2011-10-31 as well as the rest of the
month. Most Python range functions terminate before processing the end
value.

dt also provides next_day() and previous_day() functions so you can do your
own iteration in special circumstances.

### Other methods

    strftime()
    weekday()
    weekday_floor()
    ymd()
    ymdw()


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
