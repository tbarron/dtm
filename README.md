# dtm - smart datetime objects
Functionality added to datetime:

  * Initialize from date/time strings, intuiting format (no need to call
    strptime() for supported formats)
  * Initialize current date/time from no arguments (no need to call .now())
  * Easy way to jump forward and backward a day at a time
  * Easy way to get date of next Monday, next Friday, etc.
  * Iterate over a range of dates
  * Easy conversion from timezone to UTC and back

## Terms

dtspec::

    Any date/time specification. Such values may be in the form of an
    epoch, a dt object, a datetime object, a 3 to 9 element tuple of ints,
    or a string containing a date/time spec in a specific format.

default local timezone (DLTZ)::

    The default timezone used by time.localtime()

local machine (LM)::

    The machine on which the software is running

UTC::

    Universal Coordinated Time. The global reference time which is the same
    as the time in Greenwich, England.

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

Create a dt object containing the current date and time. This is analogous to
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

#### an epoch value
    myobj = dt(epoch=1426905900)
    dt("%Y.%m%d %H:%M:%S")
    >>> '2015.0320 22:45:00'

The value provided must be numeric. It can be an integer or a float, so a
value returned by time.time() or time.mktime() can be used.

#### a datetime object
If you have a datetime object and want a dt object, the dt can be
initialized directly from the datetime.

    myobj = dt(datetime(2011, 10, 9))

The microsecond member will be zeroed out.

#### another dt object
Similarly, if you have a dt and want another, just pass in the one you've
got:

    newobj = dt(myobj)

#### timezone
The tz argument is independent of the others. Any tz argument passed to the
constructor specifies the locality of the input date/time specification.

Internally, the date/time value is converted to UTC and stored as a UTC
epoch value.

All of dt's output methods accept a tz argument and will convert the
internal UTC value to the specified output timezone. If no tz argument is
specified on output, the internal UTC value is converted to the default
local timezone for the machine where the software is running.

### Comparison
dt objects can be compared for ==, <, or <= to other dt objects and to
datetime objects. The > and >= operators work for dt to dt comparisons. The
comparisons datetime > dt or datetime >= dt won't work because datetime
objects don't know about dt objects.

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
    strptime()
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


## Future Plans

### Timezone support

I would like to add timezone support as follows.

At construction, an optional timezone argument can be provided to the
constructor method to indicate which timezone the new object should
represent. The zone argument can be 'UTC', 'local', or any valid timezone
name. If no zone is specified, the default will be 'local'.

If an input date/time string is provided, it will be interpreted as being in
the specified timezone. For example,

    q = dt('2015.0320 14:45:00', z='CST6CDT')

Will compute the time as 2:45 pm on March 20, 2015, in the CDT zone. This
will actually store the UTC time 2015.0320 20:45:00 (the local time plus
six hours).

When this object is used to display date/time values, they will be
converted from UTC to CDT (i.e., the object will remember which zone it was
constructed in and display outputs in terms of that zone).

    q.strftime('%Y.%m%d %H:%M:%S')
    >>> 2015.0320 14:45:00

This makes zone to zone conversions as easy as easy:

    q = dt('2004.1007 18:19:17', z='Paris')
    q.strftime('%Y.%m%d %H:%M:%S', z='EST')
    >>> 2004.1007 10:19:17

Output methods will also accept an optional zone argument, allowing for
on-the-fly conversions. For example,

    q = dt('2015.0428 00:14:00')       # local time is EST
    q.strftime('%Y.%m%d %H:%M:%S', z='MST')
    >>> 2015.0427 21:14:00
    q.strftime('%Y.%m%d %H:%M:%S', z='Paris')
    >>> 2015.0428 06:14:00
