from dtm import version
from datetime import datetime, timedelta
import os
import pytz
import tzlocal

"""
Epoch values always represent UTC.

To convert a UTC value to a formatted local timezone:

    zone = pytz.timezone('America/New_York')
    udt = datetime.fromtimestamp(self._utc)
    return udt.astimezone(zone).strftime(format)

To convert a local time to a UTC value:

    ldt = datetime.strptime(dspec, fmt)
    utc = pytz.timezone('utc')
    udt = utc.normalize(utc.localize(ldt).astimezone(utc)
    self._utc = udt.timestamp()

To convert a non-local timezone value to a UTC value:

    ftz = pytz.timezone('PST8PDT')
    utc = pytz.timezone('UTC')
    nldt = datetime.strptime(dspec, fmt).replace(tzinfo=ftz)
    self._utc = nldt.astimezone(utc).timestamp()

The following doesn't work!

    time.mktime(time.gmtime())

Apparently, time.mktime() does a timezone adjustment that we don't want so the
result winds up being 2*utc_offset seconds into the future relative to local
time.

The following call sequences produce human-readable displays of current UTC:

    time.strftime(fmt, time.gmtime())

    datetime.utcnow().strftime(fmt)

"""


# -----------------------------------------------------------------------------
class dt(object):
    """
    This object wraps an epoch (UTC) time and a timezone with various goodies,
    like 'next_day', 'next_weekday', 'weekday_floor', etc.
    """

    _version = version._v
    _pformats = ["%Y.%m%d",
                 "%Y.%m%d %H:%M:%S",
                 "%Y/%m/%d %H:%M",
                 "%Y-%m-%d %H:%M:%S",
                 "%Y-%m-%dT%H:%M:%SZ",
                 "%Y-%m-%dT%H:%M:%S",
                 "%m/%d/%Y %H:%M:%S",
                 "%m/%d/%Y",
                 "%m/%d/%y %H:%M:%S",
                 "%m/%d/%y",
                 ]

    # -------------------------------------------------------------------------
    def __init__(self, *args, **kw):
        """
        Initialize this object. The time is stored internally as a UTC epoch
        value. If the user specifies an epoch value at construction, it will be
        stored as a UTC epoch value (I know that's somewhat redundant), without
        any timezone conversion. In this case, the user better know what
        they're doing.

        Otherwise, the incoming dtspec will be converted from the incoming
        timezone (argument 'tz') to UTC and stored as an epoch. If no incoming
        timezone is provided, the incoming dtspec will be interpreted as being
        a local time where 'local' is defined by tzlocal.get_localzone().

        Note that epoch values are always considered to be UTC values.
        """
        tzname = kw['tz'] if 'tz' in kw else None
        self._tz = dt._static_brew_tz(tzname)

        if "epoch" in kw:
            self._utc = int(kw['epoch'])
        elif len(args) == 0:
            self._utc = int(datetime.now().timestamp())
        elif len(args) == 1:
            if isinstance(args[0], dt):
                self._utc = args[0]._utc
            elif isinstance(args[0], datetime):
                self._utc = int(args[0].timestamp())
            elif isinstance(args[0], str):
                self._utc = self._from_format(args[0])
            else:
                dt._fail("single arg must be str, dt, datetime,"
                         " or epoch=<int>")
        elif all(isinstance(_, int) for _ in args):
            self._utc = self._from_ints(*args)
        else:
            dt._fail("dt.__init__ expects dt, datetime, str, ints,"
                     " or epoch=<int>")

    # -------------------------------------------------------------------------
    def __add__(self, other):
        """
        <dt> + [<int>, <td>, <timedelta>] => <dt>
        """
        if isinstance(other, td):
            return dt(epoch=self._utc + other._duration)
        elif isinstance(other, timedelta):
            return dt(epoch=self._utc + other.total_seconds())
        elif isinstance(other, (int, float)):
            return dt(epoch=self._utc + int(other))
        else:
            return NotImplemented

    # -------------------------------------------------------------------------
    def __radd__(self, other):
        """
        Handle <other> + <dt>
        """
        return self.__add__(other)

    # -------------------------------------------------------------------------
    def __sub__(self, other):
        """
        <dt> - [<dt>, <datetime>] => <td>
        <dt> - [<td>, <timedelta>, <int>] => <dt>
        """
        if isinstance(other, dt):
            return td(self._utc - other._utc)
        elif isinstance(other, datetime):
            return td(self._utc - other.timestamp())
        elif isinstance(other, td):
            return dt(epoch=self._utc - other._duration)
        elif isinstance(other, timedelta):
            return dt(epoch=self._utc - other.total_seconds())
        elif isinstance(other, (int, float)):
            return dt(epoch=self._utc - int(other))
        else:
            return NotImplemented

    # -------------------------------------------------------------------------
    def __rsub__(self, other):
        """
        <datetime> - <dt> => <td>
        [<timedelta>, <td>, <int>] - <dt> => TypeError
        """
        if isinstance(other, datetime):
            return td(other.timestamp() - self._utc)
        else:
            return NotImplemented

    # -------------------------------------------------------------------------
    def _from_format(self, spec):
        """
        Initialize from a list of my favorite date/time formats. A nice future
        feature might be a way to easily add new formats to this list, perhapss
        through a configuration file.
        """
        udfmts = self._user_defined_formats()
        if udfmts:
            udfmts.extend(self._pformats)
            self._pformats = udfmts
        formatted_dt = None
        for fmt in self._pformats:
            try:
                formatted_dt = datetime.strptime(spec, fmt)
                break
            except ValueError:
                pass
        if formatted_dt is None:
            dt._fail("None of the formats matched '{}'".format(spec))
        rval = self._norm_loc_ize(formatted_dt).timestamp()
        return rval

    # -------------------------------------------------------------------------
    def _from_ints(self, *args):
        """
        Initialize from a list of ints.
        """
        return self._norm_loc_ize(datetime(*args)).timestamp()

    # -------------------------------------------------------------------------
    @staticmethod
    def _static_brew_tz(tz):
        """
        Resolve tz to a timezone: None -> local, str -> timezone object,
        timezone object -> timezone object. This is the static method, which
        can be called from anywhere as long as the dt class is available. It is
        intended for internal use within dt(), hence the leading underscore.
        """
        if isinstance(tz, pytz.BaseTzInfo):
            rval = tz
        elif tz == 'local':
            rval = tzlocal.get_localzone()
        elif isinstance(tz, str):
            rval = pytz.timezone(tz)
        elif tz is None:
            rval = tzlocal.get_localzone()
        else:
            dt._fail("_static_brew_tz: tz must be timezone, timezone"
                     " name, or None")
        return rval

    # -------------------------------------------------------------------------
    def _brew_tz(self, tz):
        """
        Resolve *tz* to a timezone object. *tz* can be 1) None, 2) a timezone
        name, or 3) a timezone. If it's None, we're going to return the current
        object's _tz member. Otherwise, we return whatever the static method
        generates. This is the object-based method, which can only be called on
        a dt object.
        """
        if tz is None:
            rval = self._tz
        else:
            rval = dt._static_brew_tz(tz)
        return rval

    # -------------------------------------------------------------------------
    def __call__(self, *args, tz=None):
        """
        Generate the date/time in format *args[0]* (default: '%F-%T'). If tz is
        provided, show the time for that timezone. Otherwise, use the object's
        internal timezone. We just pass along the tz argument and strftime
        figures it out.
        """
        if 0 < len(args):
            fmt = args[0]
        else:
            fmt = "%F-%T"
        return self.strftime(fmt, tz=tz)

    # -------------------------------------------------------------------------
    def __eq__(self, other):
        """
        This object can be compared to another dt or a datetime obj. This
        object is equal to a datetime object if _utc is equal to the integer
        value of other.timestamp().
        """
        if isinstance(other, datetime):
            return self._utc == int(other.timestamp())
        elif isinstance(other, dt):
            return self._utc == other._utc
        else:
            return False

    # -------------------------------------------------------------------------
    def __ge__(self, other):
        """
        This object can be compared to another dt or a datetime obj.
        """
        if isinstance(other, datetime) and self._utc >= int(other.timestamp()):
            return True
        elif isinstance(other, dt) and self._utc >= other._utc:
            return True
        else:
            return False

    # -------------------------------------------------------------------------
    def __gt__(self, other):
        """
        This object can be compared to another dt or a datetime obj.
        """
        if isinstance(other, datetime) and self._utc > other.timestamp():
            return True
        elif isinstance(other, dt) and self._utc > other._utc:
            return True
        else:
            return False

    # -------------------------------------------------------------------------
    def __le__(self, other):
        """
        This object can be compared to another dt or a datetime obj.
        """
        if isinstance(other, dt) and self._utc <= other._utc:
            return True
        elif isinstance(other, datetime) and self._utc <= other.timestamp():
            return True
        else:
            return False

    # -------------------------------------------------------------------------
    def __lt__(self, other):
        """
        This object can be compared to another dt or a datetime obj.
        """
        if isinstance(other, dt) and self._utc < other._utc:
            return True
        elif isinstance(other, datetime) and self._utc < other.timestamp():
            return True
        else:
            return False

    # -------------------------------------------------------------------------
    def __str__(self):
        """
        Report the contents of the object. We return the internal epoch
        formatted for human readability.
        """
        udt = datetime.fromtimestamp(self._utc).astimezone(self._tz)
        fmt = os.getenv("DTM_STR") or "%F %T %Z"
        return udt.strftime(fmt)

    # -------------------------------------------------------------------------
    def __repr__(self):
        """
        Report the contents of the object in tuple format. The date/time
        numbers reflect the internal epoch value and we also show the object's
        internal timezone.
        """
        return "dt({}, tz='{}')".format(int(self._utc), self._tz.zone)

    # -------------------------------------------------------------------------
    def _user_defined_formats(self):
        """
        Read and parse $DTM_FORMATS if set for user defined parsing formats
        """
        rval = os.getenv("DTM_FORMATS")
        if rval:
            rval = [_.strip() for _ in rval.split(';')]
        return rval

    # -------------------------------------------------------------------------
    def datetime(self):
        """
        Return a datetime object containing the time ref and zone of *self*.
        """
        return datetime.fromtimestamp(self._utc).astimezone(self._tz)

    # -------------------------------------------------------------------------
    @staticmethod
    def _fail(msg):
        """
        Raise dt_error with *msg*
        """
        raise dt_error(msg)

    # -------------------------------------------------------------------------
    def _duration(self, *args, seconds=None, minutes=None, hours=None,
                  days=None):
        """
        Convert seconds, minutes, hours, days into a number of seconds and
        return that.

        If *args* is not empty, we expect the following:

            ([[[days,] hours,] minutes,] seconds)

        If any of the keyword args are not None, *args* must be empty.
        """
        if len(args) == 0:
            delta = days or 0
            delta = 24 * delta + (hours or 0)
            delta = 60 * delta + (minutes or 0)
            delta = 60 * delta + (seconds or 0)
        else:
            if seconds or minutes or hours or days:
                dt._fail("dt.increment expects either *args or **kw, not both")
            largs = list(args)
            mult = [24*3600, 3600, 60]
            delta = largs.pop()
            while largs:
                delta = delta + mult.pop() * largs.pop()
        return delta

    # -------------------------------------------------------------------------
    def decrement(self, *args, seconds=None, minutes=None, hours=None,
                  days=None):
        """
        Same as increment, but subtract the delta
        """
        delta = self._duration(*args, seconds=seconds, minutes=minutes,
                               hours=hours, days=days)
        return dt(epoch=self._utc - delta, tz=self._tz)

    # -------------------------------------------------------------------------
    def increment(self, *args, seconds=None, minutes=None, hours=None,
                  days=None):
        """
        If *args* is not empty, we expect one of the following:

            (seconds)
            (minutes, seconds)
            (hours, minutes, seconds)
            (days, hours, minutes, seconds)

        If any of the keyword args are not None, *args* must be empty.
        """
        delta = self._duration(*args, seconds=seconds, minutes=minutes,
                               hours=hours, days=days)
        return dt(epoch=self._utc + delta, tz=self._tz)

    # -------------------------------------------------------------------------
    def next_day(self, count=1):
        """
        Return the dt that is *count* days after the current object
        """
        prev_ts = self._utc
        prev_ldt = datetime.fromtimestamp(self._utc)
        ts = self._utc
        for day in range(count):
            ts = prev_ts + 24 * 3600
            ldt = self._norm_loc_ize(datetime.fromtimestamp(ts))
            if self._askew(prev_ldt.hour, ldt.hour):
                ts += self._delta(prev_ldt.hour, ldt.hour)
                ldt = self._norm_loc_ize(datetime.fromtimestamp(ts))
            (prev_ts, prev_ldt) = (ts, ldt)

        return dt(epoch=ts)

    # -------------------------------------------------------------------------
    def _delta(self, ahour, bhour):
        """
        Figure out the number of seconds to add to the timestamp to fix the dst
        offset
        """
        ax = (ahour + 10) % 24
        bx = (bhour + 10) % 24
        return (ax - bx) * 3600

    # -------------------------------------------------------------------------
    def _askew(self, ahour, bhour):
        """
        If there is a dst mismatch, return True, else False
        """
        return ahour != bhour

    # -------------------------------------------------------------------------
    def _norm_loc_ize(self, dtime):
        """
        Localize and normalize *dtime* into zone self._tz, returning the
        resulting datetime object
        """
        if dtime.tzinfo:
            rval = self._tz.normalize(dtime)
        else:
            rval = self._tz.normalize(self._tz.localize(dtime))
        return rval

    # -------------------------------------------------------------------------
    def last_weekday(self, trgs=None):
        """
        The argument can be a string or list of strings. Each string should be
        the lowercase abbreviated name of a weekday. The date of the last one
        preceding the current object will be returned.
        """
        if isinstance(trgs, str):
            trgs = [trgs]
        if not isinstance(trgs, list):
            dt._fail("last_weekday requires a string or list")
        wkdl = self.weekday_list()
        if any(_ not in wkdl for _ in trgs):
            dt._fail("one of the targets is not a valid weekday")
        scan = dt(self.previous_day())
        while scan.weekday() not in trgs:
            scan = scan.previous_day()
        return scan

    # -------------------------------------------------------------------------
    def next_weekday(self, trgs=None):
        """
        The argument can be a string or list of strings. Each string should be
        the lowercase abbreviated name of a weekday. The date of the next one
        following the current object will be returned.
        """
        if isinstance(trgs, str):
            trgs = [trgs]
        if not isinstance(trgs, list):
            dt._fail("next_weekday requires a string or list")
        wkdl = self.weekday_list()
        if any(_ not in wkdl for _ in trgs):
            dt._fail("one of the targets is not a valid weekday")
        scan = dt(self.next_day())
        while scan.weekday() not in trgs:
            scan = scan.next_day()
        return scan

    # -------------------------------------------------------------------------
    def previous_day(self, count=1):
        """
        Return the dt that is *count* days before current object
        """
        pts = self._utc
        pdt = datetime.fromtimestamp(pts)
        ts = self._utc
        for day in range(count):
            ts = pts - 24 * 3600
            ldt = self._norm_loc_ize(datetime.fromtimestamp(ts))
            if self._askew(pdt.hour, ldt.hour):
                ts += self._delta(pdt.hour, ldt.hour)
                ldt = self._norm_loc_ize(datetime.fromtimestamp(ts))
            (pts, pdt) = (ts, ldt)
        return dt(epoch=ts)

    # -------------------------------------------------------------------------
    def dt_range(self, last):
        """
        Yield each date from self to last, including last.
        """
        tmp = self
        while tmp <= last:
            yield tmp
            tmp = tmp.next_day()

    # -------------------------------------------------------------------------
    def strftime(self, *args, tz=None):
        """
        Pass strftime() calls down to datetime
        """
        tzobj = self._brew_tz(tz)
        when = datetime.fromtimestamp(self._utc)
        return when.astimezone(tzobj).strftime(*args)

    # -------------------------------------------------------------------------
    @staticmethod
    def strptime(*args, tz=None):
        """
        Here we've been called with a dtspec, a format, and possibly with a
        timezone. We want to parse the dtspec according to the format in the
        context of the timezone and wind up with a (UTC) epoch value suitable
        for initializing a dt object, which we then generate and return.
        """
        zone = dt._static_brew_tz(tz)
        twig = datetime.strptime(args[0], args[1])
        leaf = zone.normalize(zone.localize(twig))
        rval = dt(epoch=leaf.astimezone(zone).timestamp())
        return rval

    # -------------------------------------------------------------------------
    @staticmethod
    def version(**args):
        """
        Return the current version of this class.
        """
        return version._v

    # -------------------------------------------------------------------------
    def weekday(self, tz=None):
        """
        Return the lowercase abbreviated weekday name for the current object
        """
        return self.strftime("%a", tz=tz).lower()

    # -------------------------------------------------------------------------
    def weekday_ceiling(self, wkday):
        """
        Return a dt containing the following *wkday* unless it's today. In that
        case, return self.
        """
        if isinstance(wkday, str):
            wkday = [wkday]
        if not isinstance(wkday, list):
            self._fail("weekday_ceiling: argument must be a str or list")

        if self.weekday() in wkday:
            rval = self
        else:
            candy = self.next_day()
            while candy.weekday() not in wkday:
                candy = candy.next_day()
            rval = candy
        return rval

    # -------------------------------------------------------------------------
    def weekday_floor(self, wkday):
        """
        Return a dt containing the preceding *wkday* unless it's today. In that
        case, return self
        """
        if isinstance(wkday, str):
            wkday = [wkday]
        elif not isinstance(wkday, list):
            self._fail("weekday_floor: argument must be a str or list")

        if self.weekday() in wkday:
            rval = self
        else:
            candy = self.previous_day()
            while candy.weekday() not in wkday:
                candy = candy.previous_day()
            rval = candy
        return rval

    # -------------------------------------------------------------------------
    def weekday_list(self):
        """
        Return a list of abbreviated weekday names
        """
        return ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

    # -------------------------------------------------------------------------
    def iso(self, tz=None):
        """
        Return the object time in ISO format with optional timezone adjustment
        """
        return self.strftime("%Y-%m-%d %H:%M:%S", tz=tz)

    # -------------------------------------------------------------------------
    def ymd(self, tz=None):
        """
        Return the object time in YYYY.mmdd format with optional timezone
        adjustment
        """
        return self.strftime("%Y.%m%d", tz=tz)

    # -------------------------------------------------------------------------
    def ymdw(self, tz=None):
        """
        Return the object time in YYYY.mmdd.www format with optional timezone
        adjustment
        """
        return self.strftime("%Y.%m%d.%a", tz=tz).lower()


# -----------------------------------------------------------------------------
class dt_error(Exception):
    """
    This object is used to raise exceptions in dt().
    """
    pass


# -----------------------------------------------------------------------------
def count_in(dct, seq):
    """
    Count the number of items in *seq* that are in *dct*. This is used to
    decide whether multiple forms of keyword arguments are used in the td
    constructor. For example, the user should not provide both 's' and 'secs'.
    """
    return sum([1 for _ in seq if _ in dct])


# -----------------------------------------------------------------------------
class td(object):
    """
    This object represents a period of time, stored as a number of seconds.
    """
    # -------------------------------------------------------------------------
    def __init__(self, *args, **kw):
        """
        Argument formats:
            ([[[days,] hours,] minutes,] seconds)
            {'s': <int>,         # seconds
             'secs': <int>,
             'seconds': <int>,
             'm': <int>,         # minutes
             'mins': <int>,
             'minutes': <int>,
             'h': <int>,         # hours
             'hrs': <int>,
             'hours': <int>,
             'd': <int>,         # days
             'days': <int>,
            }
        """
        sunits = ['s', 'secs', 'seconds']
        munits = ['m', 'mins', 'minutes']
        hunits = ['h', 'hrs', 'hours']
        dunits = ['d', 'days']
        if len(args) == 0:
            if 1 < count_in(kw, sunits):
                self._fail("Mutually exclusive arguments: s, secs, seconds")
            elif 1 < count_in(kw, ['m', 'mins', 'minutes']):
                self._fail("Mutually exclusive arguments: m, mins, minutes")
            elif 1 < count_in(kw, ['h', 'hrs', 'hours']):
                self._fail("Mutually exclusive arguments: h, hrs, hours")
            elif 1 < count_in(kw, ['d', 'days']):
                self._fail("Mutually exclusive arguments: d, days")

            secs = kw.get('s') or kw.get('secs') or kw.get('seconds') or 0
            mins = kw.get('m') or kw.get('mins') or kw.get('minutes') or 0
            hours = kw.get('h') or kw.get('hrs') or kw.get('hours') or 0
            days = kw.get('d') or kw.get('days') or 0

            duration = secs + 60 * (mins + (60 * (hours + 24 * days)))
        elif any([_ in kw for _ in sunits + munits + hunits + dunits]):
            self._fail("Expected either *args or *kw, not both")
        elif isinstance(args[0], timedelta):
            duration = args[0].total_seconds()
        else:
            largs = list(args)
            mult = [24*3600, 3600, 60]
            duration = largs.pop()
            while largs:
                duration = duration + mult.pop() * largs.pop()
        self._duration = duration

    # -------------------------------------------------------------------------
    def __add__(self, other):
        """
        <td> + [<td>, <timedelta>, <int>] => <td>
        <td> + [<dt>, <datetime>] => <dt>
        """
        if isinstance(other, (int, float)):
            return td(self._duration + int(other))
        elif isinstance(other, timedelta):
            return td(self._duration + other.total_seconds())
        elif isinstance(other, td):
            return td(self._duration + other._duration)
        elif isinstance(other, datetime):
            return dt(epoch=other.timestamp() + self._duration)
        elif isinstance(other, dt):
            return dt(epoch=other._utc + self._duration)
        else:
            return NotImplemented

    # -------------------------------------------------------------------------
    def __radd__(self, other):
        """
        Handle <other> + <td>
        """
        return self.__add__(other)

    # -------------------------------------------------------------------------
    def __eq__(self, other):
        """
        True if *self*._duration == *other*._duration, otherwise False.
        """
        if isinstance(other, timedelta):
            return self._duration == other.total_seconds()
        elif isinstance(other, td):
            return self._duration == other._duration
        elif isinstance(other, (int, float)):
            return self._duration == other
        else:
            msg = ("td can be compared to number, td, or timedelta,"
                   " but not to {}".format(type(other)))
            raise ValueError(msg)

    # -------------------------------------------------------------------------
    def __repr__(self):
        """
        Show the representation of *self*.
        """
        return "<dtm.td({})>".format(self._duration)

    # -------------------------------------------------------------------------
    @staticmethod
    def _fail(msg):
        """
        Raise dt_error with *msg*
        """
        raise dt_error(msg)
