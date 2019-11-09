# dtm - smart datetime objects
Functionality added to datetime:

  * Initialize from date/time strings, intuiting format (no need to call
    strptime() for supported formats)
  * Initialize current date/time from no arguments (no need to call .now())
  * Easy way to jump forward and backward a day at a time
  * Easy way to get date of next Monday, next Friday, etc.
  * Iterate over a range of dates
  * Easy conversion from timezone to UTC and back

## Quick Start

Import the module:

    >>> from dtm import dt

Get the current date/time:

    >>> a = dt()
    >>> a
    dt(1571952371, tz='America/New_York')
    >>> a()
    '2019-10-24-17:26:11'

Get a target date/time based on a default format:

    >>> b = dt("2004.0226 12:17:30")
    >>> b()
    '2004-02-26-12:17:30'

Jump forward or backward by one or more days:

    >>> c = b.next_day(6)
    >>> c()
    '2004-03-03-12:17:30'
    >>> d = c.previous_day(17)
    >>> d()
    '2004-02-15-12:17:30'

Get the date of the Monday after April 3, 2019, and the Friday before that:

    >>> e = d.next_weekday('mon')
    >>> e()
    '2019-04-08-12:17:30'
    >>> f = e.last_weekday('fri')
    >>> f()
    '2019-04-05-12:17:30'

Iterate over a range of dates:

    >>> for day in b.dt_range(c):
    >>>     day()
    '2004-02-26-12:17:30'
    '2004-02-27-12:17:30'
    '2004-02-28-12:17:30'
    '2004-02-29-12:17:30'
    '2004-03-01-12:17:30'
    '2004-03-02-12:17:30'
    '2004-03-03-12:17:30'
    '2004-03-04-12:17:30'

Convert between timezones:

    >>> q = dt(2019, 3, 10, 3, 0, 0)
    >>> q("%F %T %A %Z")
    '2019-03-10 03:00:00 Sunday EDT'
    >>> q("%F %T %Z %A", tz='utc')
    '2019-03-10 07:00:00 UTC Sunday'
    >>> q("%F %T %Z %A", tz='pst8pdt')
    '2019-03-09 23:00:00 PST Saturday'
    >>> q("%F %T %Z %A", tz='cet')
    '2019-03-10 08:00:00 CET Sunday'
    >>> q("%F %T %Z %A", tz='Asia/Jakarta')
    '2019-03-10 14:00:00 WIB Sunday'


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

**timeref**

    A reference to a moment in time. A timeref can be represented as a date
    and time in UTC format, a date and time localized to a specific non-UTC
    timezone, the number of seconds since the epoch (1970-01-01 00:00:00
    UTC), etc. Note that timerefs represented by a number of seconds since
    the epoch is always implicitly in the UTC frame of reference.

**UTC**

    Universal Coordinated Time. The global reference time which is
    generally the same as local time in Greenwich, England.

## Exports

The main things the dtm module exports are the 'dt' class and the 'td'
class. 'dt' objects represent moments in time. A 'dt' object's moment is
stored internally as a UTC time reference. 'td' objects represent a span or
period of time, stored internally as a number of seconds. Each object
includes the methods needed to reformat the internal information for ease
of use and understanding.

## dt objects

Objects of this class represent a moment in time, stored as an epoch time
(which represents UTC by definition). They also contain a timezone so they
can be localized to specific locations on the globe.

The recommended method for importing the dt class is:

    >>> from dtm import dt

### Constructor: \_\_init\_\_()

The dt object constructor will accept several argument schemes

#### no arguments

    >>> myobj = dt()

Create a dt object containing the current date and time. This is analogous to

    >>> myobj = datetime().now()

#### a list of ints (year, month, day, hour, minute, second)

    >>> myobj = dt(2011, 10, 9)

At least year, month, and day are required. Hour, minute, and second are
all optional, although somewhat interdependent. For example, because they
are positional, you can't provide second without providing minute.

#### a string

    >>> myobj = dt("2011-10-09 20:07:06")

The code tries to intuit the format of the provided date/time string. Most
popular formats should work. If no timezone is provided, the input
date/time is considered to be in the local timezone. This value will be
converted to UTC and stored as an epoch value.

#### an epoch value

    >>> myobj = dt(epoch=1426905900)
    >>> dt("%Y.%m%d %H:%M:%S")
    '2015.0320 22:45:00'

The value provided must be numeric. It can be an integer or a float, so a
value returned by time.time() or time.mktime() can be used. The value
provided is stored without any timezone adjustment.

#### a datetime object

If you have a datetime object and want a dt object, the dt can be
initialized directly from the datetime.

    >>> myobj = dt(datetime(2011, 10, 9))

The microsecond member will be zeroed out.

#### another dt object

Similarly, if you have a dt and want another, just pass in the one you've
got:

    >>> newobj = dt(myobj)

#### timezone

The tz argument is independent of any others. Any tz argument passed to the
constructor specifies the locality of the input date/time specification.

Internally, the date/time value is converted to UTC and stored as a UTC
epoch value.

All of dt's output methods accept a tz argument and will convert the
internal UTC value to the specified output timezone. If no tz argument is
specified on output, the internal UTC value is converted to the default
local timezone (DLTZ) for the local machine (LM).

### Comparison: \_\_eq\_\_(), \_\_gt\_\_(), \_\_ge\_\_(), \_\_lt\_\_(), \_\_le\_\_()

The standard comparison operators (==, !=, <, >, <=, >=) are supported for
dt objects, which can be compared to other dt objects and datetime objects.
A dt object, A, is less than another dt object, B, if A's UTC timeref falls
earlier in time than B's UTC timeref.

Note that if a comparison puts a datetime or other value on the left side
of the operation, the "reflection" variant of the operator method will be
called. For \_\_gt\_\_(), the reflection is \_\_lt\_\_() and vice versa
since x < y has the same truth table as y > x. Similarly, \_\_ge\_\_()
reflects to \_\_le\_\_() and vice versa. The equality operator,
\_\_eq\_\_(), is its own reflection since it is a commutative operation.

### Arithmetic: \_\_add\_\_(), \_\_sub\_\_(), \_\_radd\_\_(), \_\_rsub\_\_()

The dt object supports arithmetic with other dt objects, datetime objects,
td and timedelta objects, and simple numbers (ints or floats). The
following list summarizes what is produced by each interaction. For
operations that are not supported, a TypeError exception is raised.

  * [dt] + [dt] -> TypeError
  * [dt] - [dt] -> [td]

  * [dt] + [td] -> [dt]
  * [dt] - [td] -> [dt]
  * [td] + [dt] -> [dt]
  * [td] - [dt] -> TypeError

  * [dt] + [datetime] -> TypeError
  * [dt] - [datetime] -> [td]
  * [datetime] + [dt] -> TypeError
  * [datetime] - [dt] -> [td]

  * [dt] + [timedelta] -> [dt]
  * [dt] - [timedelta] -> [dt]
  * [timedelta] + [dt] -> [dt]
  * [timedelta] - [dt] -> TypeError

  * [dt] + [int,float] -> [dt]
  * [dt] - [int,float] -> [dt]
  * [int,float] + [dt] -> [dt]
  * [int,float] - [dt] -> TypeError

The methods \_\_radd\_\_() and \_\_rsub\_\_() are called when the left hand
operand is one of int, float, timedelta, or datetime. These "reflected"
variants of \_\_add\_\_() and \_\_sub\_\_() do what is necessary to carry
out the operation requested, so that even though int, float, datetime, and
timedelta don't know anything about the dt class, they can participate in
these operations on the left side of the operator, as one would want a
commutative operation to behave.


### \_\_call\_\_(fmt='%F-%T', tz=None) (Format default output time)

The \_\_call\_\_() method adjusts the object's internal time to the indicated
output timezone and formats it for output according to the provided format
(if any).

### dt_range() (Iteration by day)

    >>> for day in dt(2011, 10, 1).dt_range(dt(2011, 10, 31)):
    >>>     # do whatever

Unlike other Python range functions, the dt_range() function is inclusive.
That is, the above loop will process 2011-10-31 as well as the rest of the
month. Most Python range functions terminate before processing the end
value.

### next_day(count=1) (Increment by day)

Return a dt object containing a timeref 24 hours later than the value in
the object on which the method is called.

### previous_day(count=1) (Decrement by day)

Return a dt object containing a timeref 24 hours earlier than the value in
the object on which the method is called.

### next_weekday(trgs=None) (Find the subsequent occurence of a target after today)

The argument, trgs, is one or more weekday names, either a string or a list
of strings. The method searches forward in time to find the next occurrence
of one of the entries in the list. If the target matches the weekday of the
stored time ref, the result is a week later.

### strftime(fmt, tz=None) (Format output time)

The time reference in the object is adjusted based on tz (if specified) and
formatted according to fmt. If tz is not provided (or is None), the
timezone value in the object is used to determine the timezone adjustment.

### strptime(spec, fmt, tz=None) [static] (Parse input time)

The string spec is parsed according to format fmt and interpreted in terms
of the timezone indicated by the tz argument. If tz is not specified,

### version() [static] (Get the package version)

Return the version of the dtm package.

### weekday(tz=None) (Determine the weekday of the stored time ref)

Return the weekday name of the stored time ref.

### weekday_floor(wkdays) (Determine latest preceding occurrence of a weekday)

Search backward in time from the stored time ref to the most recent day
matching a day in the weekday list, wkdays (may be a single string or a
list of strings). If an entry in the list matches the weekday of the stored
time ref, return self.

### weekday_list() (Get a list of weekday name abbreviations)

Return a list of abbreviated, lowercase weekday names.

### iso(tz=None) (Return the stored time in ISO format)

Return the stored time adjusted to the stored timezone (or tz if provided)
in ISO format (YYYY-mm-dd-HH:MM:SS).

### ymd(tz=None) (Return the stored time in YYYY.mmdd format)

Return the stored time adjusted to the stored timezone (or tz if provided)
in YYYY.mmdd format.

### ymdw(tz=None) (Return stored time in YYYY.mmdd.www format)

Return the stored time adjust to the stored timezone (or tz if provided) in
YYYY.mmdd.www format.


## td objects

The dtm module also provides the 'td' class. Objects of this class
represent a period of time with a specific length. td objects can be
compared to other td objects, timedelta objects, and int or float values.
td objects can be added to or subtracted from dt objects to arrive at other
dt objects. They can be added to or subtracted from other time intervals
(td or timedelta objects).

The recommended import statement for obtaining the td class is:

    >>> from dtm import td

### Constructor: \_\_init\_\_()

td objects can be initialized from the following:

  * an int or float value,
  * another td object, or
  * a timedelta object

#### no arguments

    >>> myobj = td()

This initializes a time period of 0 length.

#### one or more int values

Int arguments are interpreted as days, hours, minutes, and seconds, in that
order. To specify minutes in this format, a seconds value must also be
provided. To specify hours, both minutes and seconds must be specified.

    >>> period = td([[[days,] hours,] minutes,] seconds)

So, for example, the following object represents 5 seconds:

    >>> short = td(5)

The following object represents 2 minutes, 5 seconds:

    >>> not_long = td(2, 5)

The following object represents 5 hours, 10 minutes, 20 seconds:

    >>> a_while = td(5, 10, 20)

Finally, the following object represents 2 days, 3 hours, 15 minutes, and
32 seconds:

    >>> longer = td(2, 3, 15, 32)

#### named arguments

The following named arguments are supported:

  * 's', 'secs', 'seconds',
  * 'm', 'mins', 'minutes',
  * 'h', 'hrs', 'hours',
  * 'd', 'days'

Examples:

    >>> ten_sec = td(seconds=10)
    >>> two_min = td(mins=2, secs=2)
    >>> six_hour = td(h=6, m=17, s=3)
    >>> week = td(d=7)

### Comparison: \_\_eq\_\_(), \_\_gt\_\_(), \_\_ge\_\_(), \_\_lt\_\_(), \_\_le\_\_()

The standard comparison operators (==, !=, <, >, <=, >=) are supported for
td objects. td objects can be compared to other td objects and timedelta
objects. Reflected operations also work because of how Python reflects
\_\_ge\_\_() to \_\_le\_\_() (and vice versa) and \_\_gt\_\_() to
\_\_lt\_\_() (and verse visa).

### Arithmetic

#### \_\_add\_\_(), \_\_sub\_\_(), \_\_radd\_\_(), \_\_rsub\_\_()

The td object supports addition and subtraction with td objects, dt and
datetime objects, timedelta objects, and ints or floats. Here's a summary
of what each interaction produces. For unsupported operations, a TypeError
exception is raised.

  * [td] + [td] -> [td]
  * [td] - [td] -> [td]

  * [td] + [datetime] -> [dt]
  * [td] - [datetime] -> TypeError
  * [datetime] + [td] -> [dt]
  * [datetime] - [td] -> [dt]

  * [td] + [timedelta] -> [td]
  * [td] - [timedelta] -> [td]
  * [timedelta] + [td] -> [td]
  * [timedelta] - [td] -> [td]

  * [td] + [int,float] -> [td]
  * [td] - [int,float] -> [td]
  * [int,float] + [td] -> [td]
  * [int,float] - [td] -> [td]

Note that the reflected variant methods, \_\_radd\_\_() and \_\_rsub\_\_()
are defined to support the commutativtity of these operations.

#### \_\_mul\_\_(), \_\_truediv\_\_(), \_\_floordiv\_\_(), \_\_mod\_\_(), divmod()

The td object can be multiplied or divided by ints or floats. Any multiply
or divide operation involving two td objects or a td with a dt, datetime,
or timedelta is unsupported and raises a TypeError exception.

  * [td] * [int,float] -> [td]
  * [int,float] * [td] -> [td]

Note that \_\_rmul\_\_() and the analogous reflection methods for the other
operations are implemented to handle reflected operations correctly (mostly
by reporting that they are not supported).

### days()

Returns the length of the period in fractional days

    >>> a = td(h=6)
    >>> a.days()
    0.25

### hours()

Returns the length of the period in fractional hours

    >>> b = td(m=105)
    >>> b.hours()
    1.75

### minutes()

Returns the length of the period in fractional minutes

    >>> c = td(s=75)
    >>> c.minutes()
    1.25

### seconds()

Returns the length of the period in int seconds

    >>> d = td(m=3)
    >>> d.seconds()
    180

### dhhmmss()

Formats the time period in the td object into a string showing days, hours,
minutes, and seconds: NdHH:MM:SS.

    >>> e = td(238796)
    >>> e.dhhmmss()
    '2d18:19:56'

### dhms()

Returns days, hours, minutes, and seconds as a tuple of ints.

    >>> e.dhms()
    (2, 18, 19, 56)

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

### configuration (DONE)

Note: I decided to use environment variables DTM_FORMATS and DTM_STR rather
than reading a file every time the dt constructor is called because this
class should not add much weight to packages that use it. Environment
variables seem like the right balance between configurability and
light-weight-ness.

The value of environment variable DTM_FORMATS will be prepended to the list
of default parseable formats. For example, the following

    $ export DTM_FORMATS="%d/%m/%Y; %d/%m/%y; %d/%m/%y %H:%M:%S"

would add European date formatting (day, month, year) in front of the
default American (month, day, year) formats. This would result in
12/11/2019 being interprested as November 12, 2019 rather than December 11,
2019.

The value will be split on ';' and leading and trailing whitespace will be
removed from each segment.

The value of environment variable DTM_STR, if set, will be used to format
dt.__str__() output. For example,

    $ export DTM_STR="%H:%M:%S %B %d, %Y"

would result in the following:

    >>> a = dt()
    >>> a()
    '09:09:29 October 26, 2019'

### datetime output (DONE)

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

Most output methods will also accept an optional zone argument, allowing
for on-the-fly conversions. For example,

    >>> q = dt('2015.0428 00:14:00')       # local time is EDT
    >>> q.strftime('%Y.%m%d %H:%M:%S', z='MST')
    2015.0427 21:14:00
    >>> q.strftime('%Y.%m%d %H:%M:%S', z='Europe/Paris')
    2015.0428 06:14:00
