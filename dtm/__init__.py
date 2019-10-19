from dtm import version
from datetime import datetime
import pytz
import tzlocal

"""
Epoch values always represent UTC.

To convert a UTC value to a local timezone:

    zone = pytz.timezone('America/New_York')
    udt = datetime.fromtimestamp(self._utc)
    loc_tm = pytz.utc.localize(udt).astimezone(zone)
    return loc_tm

To convert a local time to a UTC value:

    ldt = datetime.strptime(dspec, fmt)
    utc = pytz.timezone('utc')
    udt = ldt.astimezone(utc)
    self._utc = udt.timestamp()

To convert a non-local timezone value to a UTC value:

    ftz = pytz.timezone('PST8PDT')
    utc = pytz.timezone('UTC')
    nldt = datetime.strptime(dspec, fmt).replace(tzinfo=ftz)
    self._utc = nldt.astimezone(utc).timestamp()

The following doesn't work!

    time.mktime(time.gmtime())

Apparently, time.mktime() does a timezone adjustment that we don't want.

The following call sequences that produce human-readable displays of current
UTC:

    time.strftime(fmt, time.gmtime(time.time()))

    time.strftime(fmt, time.gmtime())

    datetime.utcfromtimestamp(datetime.now().timestamp()).strftime(fmt)

    datetime.fromtimestamp(datetime.utcnow().timestamp()).strftime(fmt)
"""


# -----------------------------------------------------------------------------
class dt(object):
    _version = version._v

    """
    This object wraps a datetime object and adds various goodies, like
    'next_day', 'next_weekday', 'weekday_floor', etc.
    """
    # -------------------------------------------------------------------------
    def __init__(self, *args, **kw):
        """
        Initialize this object. The time is stored internally as a UTC epoch
        value. If you specify an epoch value at construction, it will be stored
        without any timezone conversion as UTC. In this case, you better know
        what you're doing.

        Otherwise, the incoming dtspec will be converted from the incoming
        timezone (argument 'tz') to UTC and stored as an epoch.

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
                tmp = self._from_format(args[0])
                tmp = self._tz.normalize(self._tz.localize(tmp))
                self._utc = tmp.timestamp()
            else:
                msg = "single arg must be str, dt, datetime, or epoch=<int>"
                raise dt_error(msg)
        elif all(isinstance(_, int) for _ in args):
            tmp = self._from_ints(*args)
            tmp = self._tz.normalize(self._tz.localize(tmp))
            self._utc = tmp.timestamp()
        else:
            msg = "dt.__init__ expects dt, datetime, str, ints, or epoch=<int>"
            raise dt_error(msg)

    # -------------------------------------------------------------------------
    def _from_epoch(self, val):
        """
        Initialize the object from epoch value *val*
        """
        return datetime.fromtimestamp(val)

    # -------------------------------------------------------------------------
    def _from_nothing(self):
        """
        Initialize to the present time with microseconds zeroed out
        """
        return datetime.now().replace(microsecond=0)

    # -------------------------------------------------------------------------
    def _from_format(self, spec):
        """
        Initialize from a list of popular date/time formats
        """
        fmt_candidates = ["%Y.%m%d",
                          "%Y.%m%d %H:%M:%S",
                          "%Y/%m/%d %H:%M",
                          "%Y-%m-%dT%H:%M:%SZ",
                          "%Y-%m-%dT%H:%M:%S",
                          ]
        rval = None
        for fmt in fmt_candidates:
            try:
                rval = datetime.strptime(spec, fmt)
                break
            except ValueError:
                pass
        if rval is None:
            raise dt_error("None of the formats matched '{}'".format(spec))
        return rval

    # -------------------------------------------------------------------------
    def _from_ints(self, *args):
        """
        Initialize from a list of ints
        """
        return datetime(*args)

    # -------------------------------------------------------------------------
    @staticmethod
    def _static_brew_tz(tz):
        """
        Resolve tz to a timezone: None -> local, str -> timezone object,
        timezone object -> timezone object. This is the static method, which
        can be called from anywhere as long as the dt class is available.
        However, it is intended for internal use within dt().
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
            raise dt_error("tz_fromname: tz must be timezone,"
                           " timezone name, or None")
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
        provided, show the time in that timezone. Otherwise, use the object's
        internal timezone.
        """
        if 0 < len(args):
            fmt = args[0]
        else:
            fmt = "%F-%T"
        return self.strftime(fmt, tz=tz)

    # -------------------------------------------------------------------------
    def __eq__(self, other):
        """
        This object is equal to a datetime object if _utc is equal to the
        integer value of other.timestamp()
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
        Show the contents of the object as a string
        """
        udt = datetime.fromtimestamp(self._utc)
        utc = pytz.timezone('utc')
        return udt.astimezone(utc).strftime("%Y.%m%d %H:%M:%S")

    # -------------------------------------------------------------------------
    def __repr__(self):
        """
        Report the raw utc time in the object and associated timezone
        """
        udt = datetime.utcfromtimestamp(self._utc)
        fmt = "dt(%Y, %m, %d, %H, %M, %S, tz='{}')".format(self._tz.zone)
        return udt.strftime(fmt)

    # -------------------------------------------------------------------------
    def next_day(self, count=1):
        """
        Return the dt that is *count* days after current object
        """
        prev_ts = self._utc
        prev_ldt = datetime.fromtimestamp(self._utc)
        for day in range(count):
            ts = prev_ts + 24 * 3600
            ldt = self.norm_loc_dt(self._tz, ts)
            if self.askew(prev_ldt.hour, ldt.hour):
                ts += self.delta(prev_ldt.hour, ldt.hour)
                ldt = self.norm_loc_dt(self._tz, ts)
            (prev_ts, prev_ldt) = (ts, ldt)

        return dt(epoch=ts)

    # -------------------------------------------------------------------------
    def delta(self, ahour, bhour):
        """
        Figure out the number of seconds to add to the timestamp to fix the dst
        offset
        """
        ax = (ahour + 10) % 24
        bx = (bhour + 10) % 24
        return (ax - bx) * 3600

    # -------------------------------------------------------------------------
    def askew(self, ahour, bhour):
        """
        If there is a dst mismatch, return True, else False
        """
        return ahour != bhour

    # -------------------------------------------------------------------------
    def norm_loc_dt(self, tz, ts):
        """
        Given timestamp *ts*, localize and normalize to timezone *tz* and
        return the result
        """
        tmp = datetime.fromtimestamp(ts)
        return tz.normalize(tz.localize(tmp))

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
            raise dt_error("next_weekday requires a string or list")
        wkdl = self.weekday_list()
        if any(_ not in wkdl for _ in trgs):
            raise dt_error("one of the targets is not a valid weekday")
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
        for day in range(count):
            ts = pts - 24 * 3600
            ldt = self.norm_loc_dt(self._tz, ts)
            if self.askew(pdt.hour, ldt.hour):
                ts += self.delta(pdt.hour, ldt.hour)
                ldt = self.norm_loc_dt(self._tz, ts)
            (pts, pdt) = (ts, ldt)
        return dt(epoch=ts)

    # -------------------------------------------------------------------------
    def dt_range(self, last):
        """
        Yield each date from self to last
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
        Pass strptime() calls down to datetime
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
        Return the lowercase abbreviated weekday name for the current object
        """
        return version._v

    # -------------------------------------------------------------------------
    def weekday(self, tz=None):
        """
        Return the lowercase abbreviated weekday name for the current object
        """
        return self.strftime("%a", tz=tz).lower()

    # -------------------------------------------------------------------------
    def weekday_floor(self, wkday):
        """
        Return a dt containing the preceding *wkday* unless it's today. In that
        case, return self
        """
        if wkday == self.weekday():
            rval = self
        else:
            candy = self.previous_day()
            while candy.weekday() != wkday:
                candy = candy.previous_day()
            rval = candy
        return rval

    # -------------------------------------------------------------------------
    def weekday_list(self):
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
    pass
