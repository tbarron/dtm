from dtm import version
from datetime import datetime
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
        if 'tz' in kw:
            if kw['tz'] == 'local':
                self._tz = tzlocal.get_localzone()
            else:
                self._tz = pytz.timezone(kw['tz'])
        else:
            self._tz = tzlocal.get_localzone()

        utc = pytz.timezone('utc')

        if "epoch" in kw:
            self._utc = int(kw['epoch'])
        elif len(args) == 0:
            self._utc = int(datetime.utcnow().timestamp())
        elif len(args) == 1:
            if isinstance(args[0], dt):
                self._utc = args[0]._utc
            elif isinstance(args[0], datetime):
                self._utc = int(args[0].astimezone(utc).timestamp())
            elif isinstance(args[0], str):
                tmp = self._from_format(args[0])
                tmp = self._tz.normalize(self._tz.localize(tmp))
                self._utc = tmp.astimezone(utc).timestamp()
            else:
                msg = "single arg must be str, dt, datetime, or epoch=<int>"
                raise dt_error(msg)
        elif all(isinstance(_, int) for _ in args):
            tmp = self._from_ints(*args)
            tmp = self._tz.normalize(self._tz.localize(tmp))
            self._utc = tmp.astimezone(utc).timestamp()
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
    def __eq__(self, other):
        """
        This object is equal to a datetime object if _utc is equal to the
        integer value of other.timestamp()
        """
        if self._dtobj == other:
            return True
        else:
            return False

    # -------------------------------------------------------------------------
    def __ge__(self, other):
        """
        This object can be compared to another dt or a datetime obj.
        """
        if isinstance(other, datetime) and self._dtobj >= other:
            return True
        elif isinstance(other, dt) and self._dtobj >= other._dtobj:
            return True
        else:
            return False

    # -------------------------------------------------------------------------
    def __gt__(self, other):
        """
        This object can be compared to another dt or a datetime obj.
        """
        if isinstance(other, datetime) and self._dtobj > other:
            return True
        elif isinstance(other, dt) and self._dtobj > other._dtobj:
            return True
        else:
            return False

    # -------------------------------------------------------------------------
    def __le__(self, other):
        """
        This object can be compared to another dt or a datetime obj.
        """
        if isinstance(other, dt) and self._dtobj <= other._dtobj:
            return True
        elif isinstance(other, datetime) and self._dtobj <= other:
            return True
        else:
            return False

    # -------------------------------------------------------------------------
    def __lt__(self, other):
        """
        This object can be compared to another dt or a datetime obj.
        """
        if isinstance(other, dt) and self._dtobj < other._dtobj:
            return True
        elif isinstance(other, datetime) and self._dtobj < other:
            return True
        else:
            return False

    # -------------------------------------------------------------------------
    def __str__(self):
        """
        Convert stored utc to local time and display in standard format
        """
        return self._dtobj.strftime("%Y.%m%d %H:%M:%S")

    # -------------------------------------------------------------------------
    def __repr__(self):
        """
        Report the raw utc time in the object and associated timezone
        """
        return self._dtobj.strftime("dt(%Y, %m, %d, %H, %M, %S)")

    # -------------------------------------------------------------------------
    def _prevday_overcome_dst(self):
        """
        Return the dt that is *count* days after current object
        """
        mult = 24
        candy = datetime.fromtimestamp(self._dtobj.timestamp() - mult * 3600)
        # as best I can tell the following lines are not needed
        # while candy.day == self._dtobj.day:
        #     mult += 1
        #     candy = datetime.fromtimestamp(self._dtobj.timestamp()
        #                                    - mult * 3600)
        return dt(candy)

    # -------------------------------------------------------------------------
    def next_day(self, count=1):
        """
        Figure out the number of seconds to add to the timestamp to fix the dst
        offset
        """
        scan = self._dtobj
        for day in range(count):
            mult = 24
            fore = datetime.fromtimestamp(scan.timestamp() + mult * 3600)
            # as best I can tell, the following lines are not needed
            # while fore.day == scan.day:
            #     mult += 1
            #     fore = datetime.fromtimestamp(scan.timestamp() + mult * 3600)
            scan = fore
        fore = dt(fore.year, fore.month, fore.day)
        return fore

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
        prev = self
        for day in range(count):
            prev = prev._prevday_overcome_dst()
        return prev

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
    def strftime(self, *args):
        """
        Pass strftime() calls down to datetime
        """
        return self._dtobj.strftime(*args)

    # -------------------------------------------------------------------------
    @staticmethod
    def strptime(*args):
        """
        Pass strptime() calls down to datetime
        """
        twig = datetime.now()
        return dt(twig.strptime(*args))

    # -------------------------------------------------------------------------
    @staticmethod
    def version(**args):
        """
        Return the lowercase abbreviated weekday name for the current object
        """
        return version._v

    # -------------------------------------------------------------------------
    def weekday(self):
        """
        Return the lowercase abbreviated weekday name for the current object
        """
        return self._dtobj.strftime("%a").lower()

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
    def ymd(self):
        return self._dtobj.strftime("%Y.%m%d")

    # -------------------------------------------------------------------------
    def ymdw(self):
        return self._dtobj.strftime("%Y.%m%d.%a").lower()


# -----------------------------------------------------------------------------
class dt_error(Exception):
    pass
