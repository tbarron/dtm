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

**dtspec**

    Any date/time specification. Such values may be in the form of an
    epoch, a dt object, a datetime object, a 3 to 9 element tuple of ints,
    or a string containing a date/time spec in a specific format.

**default local timezone (DLTZ)**

    The default timezone used by time.localtime(). That is, the default
    timezone of the local machine (LM).

**epoch**

    "The Epoch" is the beginning of time from the perspective of the
    underlying date/time software Python depends upon. For most Unix-style
    operating systems, this is 1970-01-01T00:00:00 UTC.

**epoch value**

    An epoch value is a number of seconds since "The Epoch" (see above).
    Epoch values always represent UTC, not local times.

**local machine (LM)**

    The machine on which the software is running

**UTC**

    Universal Coordinated Time. The global reference time which is
    generally the same as local time in Greenwich, England.

## dt objects

The main thing dtm exports is the 'dt' object. It contains an epoch time
(which represents UTC by definition) and a timezone.

The recommended method for importing the dt class is:

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
popular formats should work. If not timezone is provided, the input
date/time is considered to be in the local timezone. This value will be
converted to UTC and stored as an epoch value.

#### an epoch value

    myobj = dt(epoch=1426905900)
    dt("%Y.%m%d %H:%M:%S")
    >>> '2015.0320 22:45:00'

The value provided must be numeric. It can be an integer or a float, so a
value returned by time.time() or time.mktime() can be used. The value
provided is stored without any timezone adjustment.

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

The tz argument is independent of any others. Any tz argument passed to the
constructor specifies the locality of the input date/time specification.

Internally, the date/time value is converted to UTC and stored as a UTC
epoch value.

All of dt's output methods accept a tz argument and will convert the
internal UTC value to the specified output timezone. If no tz argument is
specified on output, the internal UTC value is converted to the default
local timezone (DLTZ) for the local machine (LM).

### Comparison

dt objects can be compared for ==, <, <=, >, or >= to other dt objects and
to datetime objects. The comparisons operators won't work if datetime is on
the left side because datetime objects don't know how to compare themselves
to dt objects.

### __call__([fmt,] tz=None) (Format default output time)

Adjust the stored time reference per tz (if given) and format it per fmt
(if provided). If tz is not provided, use the dt object's internal tz
value. If format is not provided, the default format is used ('%F-%T').

### dt.dt_range() (Iteration by day)

    for day in dt(2011, 10, 1).dt_range(dt(2011, 10, 31)):
        # do whatever

Unlike other Python range functions, the dt_range() function is inclusive.
That is, the above loop will process 2011-10-31 as well as the rest of the
month. Most Python range functions terminate before processing the end
value.

### dt.next_day(count=1) (Increment by day)

Return a dt object containing a time reference 24 hours later than the
value in the object on which the method is called.

### dt.previous_day(count=1) (Decrement by day)

Return a dt object containing a time reference 24 hours earlier than the
value in the object on which the method is called.

### dt.next_weekday(trgs=None) (Find the subsequent occurence of a target after today)

The argument, trgs, is one or more weekday names, either a string or a list
of strings. The method searches forward in time to find the next occurrence
of one of the entries in the list. If the target matches the weekday of the
stored time ref, the result is a week later.

### dt.strftime(fmt, tz=None) (Format output time)

The time reference in the object is adjusted based on tz (if specified) and
formatted according to fmt. If tz is not provided (or is None), the
timezone value in the object is used to determine the timezone adjustment.

### dt.strptime(spec, fmt, tz=None) [static] (Parse input time)

The string spec is parsed according to format fmt and interpreted in terms
of the timezone indicated by the tz argument. If tz is not specified, 

### dt.version() [static] (Get the package version)

Return the version of the dtm package.

### dt.weekday(tz=None) (Determine the weekday of the stored time ref)

Return the weekday name of the stored time ref.

### dt.weekday_floor(wkdays) (Determine latest preceding occurrence of a weekday)
    
Search backward in time from the stored time ref to the most recent day
matching a day in the weekday list, wkdays (may be a single string or a
list of strings). If an entry in the list matches the weekday of the stored
time ref, return self.

### dt.weekday_list() (Get a list of weekday name abbreviations)

Return a list of abbreviated, lowercase weekday names.

### dt.iso(tz=None) (Return the stored time in ISO format)

Return the stored time adjusted to the stored timezone (or tz if provided)
in ISO format (YYYY-mm-dd-HH:MM:SS).

### dt.ymd(tz=None) (Return the stored time in YYYY.mmdd format)

Return the stored time adjusted to the stored timezone (or tz if provided)
in YYYY.mmdd format.

### dt.ymdw(tz=None) (Return stored time in YYYY.mmdd.www format)

Return the stored time adjust to the stored timezone (or tz if provided) in
YYYY.mmdd.www format.


## Project setup

    dtm                         # project directory
    |
    +- .coveragerc              # parameters for test coverage
    +- .gitignore               # tell git which files to ignore
    +- LICENSE                  # license for this software
    +- Makefile                 # document command lines for tests and such
    +- README.md                # this file
    +- CHANGELOG.md             # change history
    +- pytest.ini               # parameters for pytest
    +- requirements.txt         # items this project depends on
    +- setup.py                 # configuration management
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
    +- pytest.ini*              # pytest configuration
    +- .env*                    # set env upon cd into this directory (autoenv)
    +- venv*                    # virtual environment

Files marked with * are not in git.

## Future Plans

### configuration file

Get the list of favorite parsing formats from a configuration file, perhaps
located at $HOME/.dtm/dtm.ini. The default list provided by the module
would always be present (unless the user overwrites it; perhaps we need a
way of specifying this in the config file) and the user could easily
augment the list by adding formats to the config file.

### datetime output

Provide a dt method that returns a datetime object, foo, containing the dt
object's time reference and timezone such that foo.strftime("%F %T %Z")
produces the same output as mydt.strftime("%F %T %Z").

### Timezone support (DONE)

I would like to add timezone support as follows.

At construction, an optional timezone argument can be provided to the
constructor method to indicate which timezone the new object should
represent. The zone argument can be 'UTC', 'local', or any valid timezone
name. If no zone is specified, the default will be 'local'.

If an input date/time string is provided, it will be interpreted as being in
the specified timezone. For example,

    >>> q = dt('2015.0320 14:45:00', z='CST6CDT')

Will compute the time as 2:45 pm on March 20, 2015, in the CDT zone. This
will actually store the UTC time 2015.0320 20:45:00 (the local time plus
six hours).

When this object is used to display date/time values, they will be
converted from UTC to CDT (i.e., the object will remember which zone it was
constructed in and display outputs in terms of that zone).

    >>> q.strftime('%Y.%m%d %H:%M:%S')
    '2015.0320 14:45:00'

This makes zone to zone conversions as easy as easy:

    >>> q = dt('2004.1007 18:19:17', z='Paris')
    >>> q.strftime('%Y.%m%d %H:%M:%S', z='EST')
    '2004.1007 10:19:17'

Output methods will also accept an optional zone argument, allowing for
on-the-fly conversions. For example,

    q = dt('2015.0428 00:14:00')       # local time is EST
    q.strftime('%Y.%m%d %H:%M:%S', z='MST')
    >>> 2015.0427 21:14:00
    q.strftime('%Y.%m%d %H:%M:%S', z='Paris')
    >>> 2015.0428 06:14:00
