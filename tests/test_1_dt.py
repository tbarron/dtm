from datetime import datetime
from dtm import dt, dt_error, version
import pytest
import tbx


pp = pytest.param


# -----------------------------------------------------------------------------
def test_attributes():
    """
    A dt object should have members _utc and _tz
    """
    act = dt()
    assert hasattr(act, '_utc')
    assert hasattr(act, '_tz')


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("spec, itz, fmt, otz, exp", [
    pp("2019.1001", None,
       "%F", None, "2019-10-01", id="default -> default"),
    pp("2019.1001", None,
       "%F %T", 'utc', "2019-10-01 04:00:00", id="default -> utc"),
    pp("2019.1001 17:00:00", None,
       "%F %T", 'cst6cdt', "2019-10-01 16:00:00", id="default -> cdt"),
    pp("2019.1001 13:00:00", 'pst8pdt',
       "%F %T", 'cst6cdt', "2019-10-01 15:00:00", id="pdt -> cdt"),
    pp("2019.1001 13:00:00", 'pst8pdt',
       "%F %T", None, "2019-10-01 13:00:00", id="pdt -> default"),
    pp("2011.0528 16:00:00", 'cet',
       "%F %T", 'mst7mdt', "2011-05-28 08:00:00", id="cet -> mdt"),
    pp("2010.1010 10:10:10", 'NZ',
       "%F %T", 'Pacific/Midway', "2010-10-09 10:10:10", id="NZ -> Midway"),
    ])
def test_call(spec, itz, fmt, otz, exp):
    """
    """
    if itz:
        x = dt(spec, tz=itz)
    else:
        x = dt(spec)
    if otz:
        assert x(fmt, tz=otz) == exp
    else:
        assert x(fmt) == exp


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("inp, exp", [
    pp((), None, id="no arg"),
    pp(datetime(2001, 9, 11), dt(epoch=1000180800), id="datetime epoch"),
    pp("2001.0911", dt(epoch=1000180800), id="str ymd"),
    pp(datetime(2001, 9, 11, 0, 0, 0), dt("2001.0911"), id="datetime ymd"),
    pp(datetime(2009, 7, 23, 9, 45, 17), dt("2009.0723 09:45:17"),
       id="datetime ymdhms"),
    pp(datetime.now(), dt(), id="datetime now"),
    pp((2008, 7, 5), dt("2008.0705"), id="tup ymd"),
    pp((2008, 7, 5, 7), dt("2008.0705 07:00:00"), id="tup ymdh"),
    pp((2008, 7, 5, 7, 38), dt("2008.0705 07:38:00"), id="tup ymdhm"),
    pp((2008, 7, 5, 7, 38, 19), dt("2008.0705 07:38:19"), id="tup ymdhms"),
    pp("2018.0107", dt(2018, 1, 7), id="str ymd"),
    pp("2001/3/24 19:35", dt(2001, 3, 24, 19, 35), id="str ymdhm"),
    pp("1978-12-13T11:45:27Z", dt("1978.1213 11:45:27"),
       id="isoformat with Z"),
    pp("1978-12-13T11:45:27", dt("1978.1213 11:45:27"), id="isoformat"),
    pp([1], dt_error("single arg must be str, dt, datetime, or epoch=<int>"),
       id="dterr single"),
    pp(["abc", "def"],
       dt_error("dt.__init__ expects dt, datetime, str, ints, or epoch=<int>"),
       id="dterr multi"),
    pp("2018.0731 17", dt_error("None of the formats matched"),
       id="dterr format"),
    ])
def test_init(inp, exp):
    """
    test dt() with no args -- should be now
    """
    pytest.dbgfunc()
    if exp is None:
        exp = dt(datetime.now())
    if isinstance(inp, tuple):
        assert dt(*inp) == exp
    elif isinstance(exp, dt_error):
        with pytest.raises(dt_error) as err:
            if isinstance(inp, list):
                dt(*inp)
            else:
                dt(inp)
        assert str(exp) in str(err.value)
    else:
        assert dt(inp) == exp


# -----------------------------------------------------------------------------
def test_init_epoch():
    """
    Initializing from an epoch value will always produce the same UTC time
    reference. For the expected value on the right, we have to use tz='utc'
    since the target time reference would vary with timezone if we defaulted to
    the local timezone for the expected value.
    """
    pytest.dbgfunc()
    assert dt(epoch=1570000000) == dt("2019.1002 07:06:40", tz='utc')


# -----------------------------------------------------------------------------
def test_init_tz_explicit():
    """
    Specifying an explicit timezone and dtspec should always produce the same
    UTC epoch value
    """
    pytest.dbgfunc()
    actual = dt("2018.0117 10:00:00", tz='America/Boise')
    exp = dt(epoch=1516208400)
    assert actual == exp


# -----------------------------------------------------------------------------
def test_init_tz_local():
    """
    In timezone EST5EDT, the test dtspec corresponds to UTC epoch value
    1516201200. In other timezones, it will correspond to other UTC values, so
    we have to get the corresponding epoch value from datetime() to verify that
    the dt constructor with the tz='local' argument is behaving correctly.
    """
    pytest.dbgfunc()
    ldt = datetime(2018, 1, 17, 10, 0, 0)
    exp_epoch = ldt.timestamp()
    actual = dt("2018.0117 10:00:00", tz='local')
    assert actual._utc == exp_epoch


# -----------------------------------------------------------------------------
def test_init_tz_utc():
    """
    In UTC, the test dtspec corresponds to the indicated epoch value.
    """
    pytest.dbgfunc()
    assert dt("2018.0117 10:00:00", tz='utc') == dt(epoch=1516183200)


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("left, right, exp", [
    pp(dt(), datetime.now(), True, id="dt eq datetime"),
    pp(dt(epoch=1571315783), datetime.fromtimestamp(1571315784), False,
       id="dt ne datetime"),
    pp(dt(2018, 1, 17), dt("2018.0117"), True, id="dt(ints) eq dt(str)"),
    pp(dt(2018, 1, 17, 6, 30), dt("2018.0117"), False,
       id="dt(ints) ne dt(str)"),
    pp(dt(2018, 1, 17), 17, False, id="dt ne number"),
    ])
def test_equal(left, right, exp):
    """
    Test the equality operator for dt()
    """
    assert (left == right) is exp


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("inp, bench, exp", [
    pp("2012.0101", dt("2012.0102"), False, id="ge-n-s-i-f"),
    pp("2011.1231", dt("2012.0101"), False, id="ge-n-s-y-f"),
    pp("2012.0102", dt("2012.0101"), True, id="ge-n-s-i-t"),
    pp("2012.0102", dt("2011.1231"), True, id="ge-n-s-y-t"),
    pp("2012.0102", dt("2012.0102"), True, id="ge-n-e-i-t"),

    pp("2012.0101", datetime(2012, 1, 2), False, id="ge-d-s-i-f"),
    pp("2011.1231", datetime(2012, 1, 1), False, id="ge-d-s-y-f"),
    pp("2012.0102", datetime(2012, 1, 1), True, id="ge-d-s-i-t"),
    pp("2012.0102", datetime(2011, 12, 31), True, id="ge-d-s-y-t"),
    pp("2012.0102", datetime(2012, 1, 2), True, id="ge-d-e-i-t"),
    ])
def test_ge(inp, bench, exp):
    """
    dt(*foo) is le datetime(*bar) if dt(*foo)._dtobj >= datetime(*bar)
    dt(*foo) is le dt(*bar) if dt(*foo)._dtobj >= dt(*bar)._dtobj
    """
    pytest.dbgfunc()
    assert (dt(inp) >= bench) is exp


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("inp, bench, exp", [
    pp("2012.0101", dt("2012.0102"), False, id="gt-n-s-i-f"),
    pp("2011.1231", dt("2012.0101"), False, id="gt-n-s-y-f"),
    pp("2012.0102", dt("2012.0101"), True, id="gt-n-s-i-t"),
    pp("2012.0102", dt("2011.1231"), True, id="gt-n-s-y-t"),
    pp("2012.0102", dt("2012.0102"), False, id="gt-n-e-i-f"),

    pp("2012.0101", datetime(2012, 1, 2), False, id="gt-d-s-i-f"),
    pp("2011.1231", datetime(2012, 1, 1), False, id="gt-d-s-y-f"),
    pp("2012.0102", datetime(2012, 1, 1), True, id="gt-d-s-i-t"),
    pp("2012.0102", datetime(2011, 12, 31), True, id="gt-d-s-y-t"),
    pp("2012.0102", datetime(2012, 1, 2), False, id="gt-d-e-i-f"),
    ])
def test_gt(inp, bench, exp):
    """
    dt(*foo) is le datetime(*bar) if dt(*foo)._dtobj <= datetime(*bar)
    dt(*foo) is le dt(*bar) if dt(*foo)._dtobj <= dt(*bar)._dtobj
    """
    pytest.dbgfunc()
    assert (dt(inp) > bench) is exp


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("inp, bench, exp", [
    pp("2012.0101", dt("2012.0102"), True, id="le-n-s-i-t"),
    pp("2011.1231", dt("2012.0101"), True, id="le-n-s-y-t"),
    pp("2012.0102", dt("2012.0101"), False, id="le-n-s-i-f"),
    pp("2012.0102", dt("2011.1231"), False, id="le-n-s-y-f"),
    pp("2012.0102", dt("2012.0102"), True, id="le-n-e-i-t"),

    pp("2012.0101", datetime(2012, 1, 2), True, id="le-d-s-i-t"),
    pp("2011.1231", datetime(2012, 1, 1), True, id="le-d-s-y-t"),
    pp("2012.0102", datetime(2012, 1, 1), False, id="le-d-s-i-f"),
    pp("2012.0102", datetime(2011, 12, 31), False, id="le-d-s-y-f"),
    pp("2012.0102", datetime(2012, 1, 2), True, id="le-d-e-i-t"),
    ])
def test_le(inp, bench, exp):
    """
    dt(*foo) is le datetime(*bar) if dt(*foo)._dtobj <= datetime(*bar)
    dt(*foo) is le dt(*bar) if dt(*foo)._dtobj <= dt(*bar)._dtobj
    """
    pytest.dbgfunc()
    assert (dt(inp) <= bench) is exp


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("inp, bench, exp", [
    pp("2012.0101", dt("2012.0102"), True, id="lt-n-s-i-t"),
    pp("2011.1231", dt("2012.0101"), True, id="lt-n-s-y-t"),
    pp("2012.0102", dt("2012.0101"), False, id="lt-n-s-i-f"),
    pp("2012.0102", dt("2011.1231"), False, id="lt-n-s-y-f"),
    pp("2012.0102", dt("2012.0102"), False, id="lt-n-e-i-f"),

    pp("2012.0101", datetime(2012, 1, 2), True, id="lt-d-s-i-t"),
    pp("2011.1231", datetime(2012, 1, 1), True, id="lt-d-s-y-t"),
    pp("2012.0102", datetime(2012, 1, 1), False, id="lt-d-s-i-f"),
    pp("2012.0102", datetime(2011, 12, 31), False, id="lt-d-s-y-f"),
    pp("2012.0102", datetime(2012, 1, 2), False, id="lt-d-e-i-f"),
    ])
def test_lt(inp, bench, exp):
    """
    dt(*foo) is less than datetime(*bar) if dt(*foo)._dtobj < datetime(*bar)
    dt(*foo) is less than dt(*bar) if dt(*foo)._dtobj < dt(*bar)._dtobj
    """
    pytest.dbgfunc()
    assert (dt(inp) < bench) is exp


# -----------------------------------------------------------------------------
def test_dt_range():
    """
    Test dt().dt_range()
    """
    pytest.dbgfunc()
    last = None
    for day in dt("2011.1230").dt_range(dt("2012.0107")):
        if last:
            assert day.previous_day() == last
        last = day


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("nub, ndargs, exp", [
    pp(dt(2012, 12, 31), (), dt(2013, 1, 1), id="year"),
    pp(dt(2012, 12, 31), (30,), dt(2013, 1, 30), id="30 days"),
    pp(dt(2012, 12, 31), (90,), dt(2013, 3, 31), id="90 days"),
    pp(dt(2013, 3, 8), (5,), dt(2013, 3, 13), id="rising DST"),
    pp(dt(2013, 11, 1), (5,), dt(2013, 11, 6), id="falling DST"),
    pp(dt(1960, 2, 28), (), dt(1960, 2, 29), id="leap year"),
    pp(dt(1800, 2, 28), (), dt(1800, 3, 1), id="century non-leap year"),
    pp(dt(2000, 2, 28), (), dt(2000, 2, 29), id="quad century leap year"),
    ])
def test_next_day(nub, ndargs, exp):
    """
    Test dt().next_day()
    """
    pytest.dbgfunc()
    assert nub.next_day(*ndargs) == exp


# -----------------------------------------------------------------------------
def test_next_weekday():
    """
    Test dt().next_weekday(). If today is Monday, dt().next_weekday('mon')
    should be a week from today.
    """
    pytest.dbgfunc()
    when = dt(2011, 4, 12)
    assert when.next_weekday('wed') == dt(2011, 4, 13)
    assert when.next_weekday('thu') == dt(2011, 4, 14)
    assert when.next_weekday('fri') == dt(2011, 4, 15)
    assert when.next_weekday('sat') == dt(2011, 4, 16)
    assert when.next_weekday('sun') == dt(2011, 4, 17)
    assert when.next_weekday('mon') == dt(2011, 4, 18)
    assert when.next_weekday('tue') == dt(2011, 4, 19)
    with pytest.raises(dt_error) as err:
        when.next_weekday(3)
    assert "next_weekday requires a string or list" in str(err.value)
    with pytest.raises(dt_error) as err:
        when.next_weekday('january')
    assert "one of the targets is not a valid weekday" in str(err.value)


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("nub, pvargs, exp", [
    pp(dt(2013, 3, 13), (5,), dt(2013, 3, 8), id="rising dst range"),
    pp(dt(2013, 11, 6), (5,), dt(2013, 11, 1), id="falling dst range"),
    pp(dt(2016, 3, 14), (), dt(2016, 3, 13), id="one-day rising dst"),
    pp(dt(2016, 11, 7), (), dt(2016, 11, 6), id="one-day falling dst"),
    pp(dt(2009, 1, 1), (), dt(2008, 12, 31), id="year"),
    pp(dt(2008, 3, 1), (), dt(2008, 2, 29), id="leap year"),
    pp(dt(1900, 3, 1), (), dt(1900, 2, 28), id="century year"),
    pp(dt(2000, 3, 1), (), dt(2000, 2, 29), id="quad century year"),
    ])
def test_previous_day_pp(nub, pvargs, exp):
    """
    Tests for previous_day()
    """
    pytest.dbgfunc()
    assert nub.previous_day(*pvargs) == exp


# -----------------------------------------------------------------------------
def test_repr():
    """
    repr(dt()) should produce a predictable string
    """
    pytest.dbgfunc()
    when = dt(2012, 12, 31, 1, 2, 3, tz="EST5EDT")
    assert repr(when) == "dt(2012, 12, 31, 06, 02, 03, tz='EST5EDT')"
    when = dt(2012, 12, 31, 1, 2, 3, tz="UTC")
    assert repr(when) == "dt(2012, 12, 31, 01, 02, 03, tz='UTC')"


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("inp, exp", [
    pp(dt(2012, 12, 31, 1, 2, 3, tz="est5edt"), "2012.1231 06:02:03",
       id="est"),
    pp(dt(2012, 12, 31, 1, 2, 3, tz='America/Boise'), "2012.1231 08:02:03",
       id="mst"),
    ])
def test_str(inp, exp):
    """
    str(dt()) should produce a predictable string. It should generate the time
    ref in utc to show the actual contents of the object.
    """
    pytest.dbgfunc()
    assert str(inp) == exp


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("when, fmt, tzone, exp", [
    pp(dt(2000, 12, 1), "%Y.%m%d %H:%M:%S", None, "2000.1201 00:00:00",
       id="2000.1201"),
    pp(dt(2000, 12, 1), "%Y.%m%d %H:%M:%S", 'utc', "2000.1201 05:00:00",
       id="2000.1201 utc"),
    pp(dt(2000, 12, 1), "%s", None, "975646800", id="epoch"),
    pp(dt(2000, 12, 1), "%a", None, "Fri", id="weekday abbrev"),
    pp(dt(2000, 12, 1), "%a", "Pacific/Midway", "Thu",
       id="weekday abbrev transition"),
    pp(dt(2000, 11, 30), "%A", None, "Thursday", id="weekday name"),
    pp(dt(2000, 11, 30), "%b", None, "Nov", id="month abbrev"),
    pp(dt(2000, 11, 30), "%B", None, "November", id="month name"),
    pp(dt(2001, 11, 1, tz='NZ'), "%b", "Pacific/Midway", "Oct",
       id="prev month"),
    pp(dt("2000.1130 13:25:19"), "%c", None, "Thu Nov 30 13:25:19 2000",
       id="locale"),
    pp(dt("2000.1130 13:25:19"), "%I:%M:%S %p", None, "01:25:19 PM",
       id="12 hour"),
    pp(dt(2015, 3, 20, 14, 45, 0, tz='cst6cdt'), "%Y.%m%d %H:%M:%S", None,
       "2015.0320 14:45:00", id="output localized to timezone")
    ])
def test_strftime(when, fmt, tzone, exp):
    """
    Test strftime
    """
    pytest.dbgfunc()
    if tzone:
        assert when.strftime(fmt, tz=tzone) == exp
    else:
        assert when.strftime(fmt) == exp


# -----------------------------------------------------------------------------
def test_version():
    """
    Verify that dt.version() returns what is expected. It can be called as a
    static method on the class (dt.version()) or as a method on a dt object:

        q = dt()
        q.version()
    """
    assert dt.version() == version._v
    assert dt().version() == version._v


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("when, fmt, exp", [
    pp('2016-09-28T16:46:42Z', "%Y-%m-%dT%H:%M:%SZ",
       dt(2016, 9, 28, 16, 46, 42)),
    pp('2020.0229', "%Y.%m%d", dt("2020.0229"))
    ])
def test_strptime(when, fmt, exp):
    """
    Test strptime
    """
    pytest.dbgfunc()
    assert dt.strptime(when, fmt) == exp


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("obj, otz, exp", [
    pp(dt("2012.0704"), None, "wed", id="wed -> wed"),
    pp(dt("2012.0704"), 'Pacific/Midway', "tue", id="wed -> tue"),
    pp(dt("2012.0704 16:00:00", tz='Pacific/Midway'), 'Pacific/Auckland',
       'thu', id="wed -> thu"),
    ])
def test_weekday(obj, otz, exp):
    """
    Test dt.weekday()
    """
    pytest.dbgfunc()
    assert obj.weekday(tz=otz) == exp


# -----------------------------------------------------------------------------
def test_weekday_floor():
    """
    Test dt().weekday_floor(). If today is Monday, dt().weekday_floor('mon') is
    today, dt().weekday_floor('sun') is yesterday, and
    dt().weekday_floor('tue') is last Tuesday
    """
    pytest.dbgfunc()
    when = dt(2000, 12, 1)
    assert when.weekday_floor('sat') == dt(2000, 11, 25)
    assert when.weekday_floor('sun') == dt(2000, 11, 26)
    assert when.weekday_floor('mon') == dt(2000, 11, 27)
    assert when.weekday_floor('tue') == dt(2000, 11, 28)
    assert when.weekday_floor('wed') == dt(2000, 11, 29)
    assert when.weekday_floor('thu') == dt(2000, 11, 30)
    assert when.weekday_floor('fri') == dt(2000, 12, 1)


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("when", [
    ("2001.0719"),
    ("2007.0917"),
    ("2005.0313"),
    ])
def test_ymd(when):
    """
    Test dt().ymd().
    """
    pytest.dbgfunc()
    assert dt(when).ymd() == when


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("when, exp", [
    ("2001.0719", "2001.0719.thu"),
    ("2007.0917", "2007.0917.mon"),
    ("2005.0313", "2005.0313.sun"),
    ])
def test_ymdw(when, exp):
    """
    Test dt().ymd().
    """
    pytest.dbgfunc()
    assert dt(when).ymdw() == exp


# -----------------------------------------------------------------------------
def test_deployable():
    """
    Check that 1) no untracked files are hanging out, 2) no staged but
    uncommitted updates are outstanding, 3) no unstaged, uncommitted changes
    are outstanding, 4) the most recent git tag matches HEAD, and 5) the most
    recent git tag matches the current version.
    """
    pytest.dbgfunc()
    staged, changed, untracked = tbx.git_status()
    assert untracked == [], "You have untracked files"
    assert changed == [], "You have unstaged updates"
    assert staged == [], "You have updates staged but not committed"

    if tbx.git_current_branch() != 'master':
        return True

    last_tag = tbx.git_last_tag()
    msg = "Version ({}) does not match tag ({})".format(tbx.version(),
                                                        last_tag)
    assert dt.version() == last_tag, msg
    assert tbx.git_hash() == tbx.git_hash(last_tag), "Tag != HEAD"
