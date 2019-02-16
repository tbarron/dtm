from datetime import datetime


# -----------------------------------------------------------------------------
class dt(object):
    """
    This object wraps a datetime object and adds various goodies, like
    'next_day', 'next_weekday', 'weekday_floor', etc.
    """
    # -------------------------------------------------------------------------
    def __init__(self, *args, **kw):
        """
        Initialize this object. It contains a datetime object, which carries
        its value.
        """
        if len(args) == 0:
            self._dtobj = self._from_nothing()
        elif len(args) == 1:
            if isinstance(args[0], dt):
                self._dtobj = args[0]._dtobj
            elif isinstance(args[0], datetime):
                self._dtobj = args[0].replace(microsecond=0)
            elif isinstance(args[0], str):
                self._dtobj = self._from_format(args[0])
            else:
                raise dt_error("single arg must be str, dt, or datetime")
        elif all(isinstance(_, int) for _ in args):
            self._dtobj = self._from_ints(*args)
        else:
            raise dt_error("dt.__init__ expects dt, datetime, str, or ints")

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
                          "%Y/%m/%d %H:%M"]
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
        This object is equal to a datetime object if its _dtobj is
        """
        if self._dtobj == other:
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
        Standard format for stringifying a dt object
        """
        return self._dtobj.strftime("%Y.%m%d %H:%M:%S")

    # -------------------------------------------------------------------------
    def __repr__(self):
        """
        Debugging representation for a dt object
        """
        return self._dtobj.strftime("dt(%Y, %m, %d, %H, %M, %S)")

    # -------------------------------------------------------------------------
    def _prevday_overcome_dst(self):
        """
        Return a dt representing the previous day. Adjust the hour multiplier
        to ensure hitting the previous day.
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
        Return the dt that is *count* days after current object
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
