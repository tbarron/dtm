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
@pytest.mark.parametrize("inp, exp", [
    pp((), None, id="no arg"),
    pp(datetime(2001, 9, 11), dt(epoch=1000180800), id="datetime epoch"),
    pp("2001.0911", dt(epoch=1000180800), id="str ymd"),
    pp(datetime(2001, 9, 11, 0, 0, 0), dt("2001.0911"), id="datetime ymd"),
    pp(datetime(2009, 7, 23, 9, 45, 17), dt("2009.0723 09:45:17"),
       id="datetime ymdhms"),
    pp(datetime.utcnow(), dt(), id="datetime now"),
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
def test_equal():
    """
    dt(*foo) is equal to datetime(*bar) if dt(*foo)._dtobj == datetime(*bar)
    """
    pytest.dbgfunc()
    assert dt() == datetime.now().replace(microsecond=0)
    assert dt() != datetime.now().replace(microsecond=300)
    assert dt(2018, 1, 17) == dt("2018.0117")
    assert dt(2018, 1, 17, 6, 30) != dt("2018.0117")


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
def test_next_day():
    """
    Test dt().next_day()
    """
    pytest.dbgfunc()
    when = dt(2012, 12, 31)
    assert when.next_day() == dt(2013, 1, 1)
    assert when.next_day(30) == dt(2013, 1, 30)
    assert when.next_day(count=90) == dt(2013, 3, 31)


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
def test_previous_day():
    """
    Try to find a date that activates lines 97-98, where a given dt's timestamp
    minus that of the preceding day is greater than 24 hours
    """
    pytest.dbgfunc()
    pytest.skip('construction')


# -----------------------------------------------------------------------------
def test_repr():
    """
    str(dt()) should produce a predictable string
    """
    pytest.dbgfunc()
    when = dt(2012, 12, 31, 1, 2, 3)
    assert repr(when) == "dt(2012, 12, 31, 01, 02, 03)"


# -----------------------------------------------------------------------------
def test_str():
    """
    str(dt()) should produce a predictable string
    """
    pytest.dbgfunc()
    when = dt(2012, 12, 31, 1, 2, 3)
    assert str(when) == "2012.1231 01:02:03"


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("when, fmt, exp", [
    pp(dt(2000, 12, 1), "%Y.%m%d %H:%M:%S", "2000.1201 00:00:00",
       id="2000.1201"),
    pp(dt(2000, 12, 1), "%s", "975646800", id="epoch"),
    pp(dt(2000, 12, 1), "%a", "Fri", id="weekday abbrev"),
    pp(dt(2000, 11, 30), "%A", "Thursday", id="weekday name"),
    pp(dt(2000, 11, 30), "%b", "Nov", id="month abbrev"),
    pp(dt(2000, 11, 30), "%B", "November", id="month name"),
    pp(dt("2000.1130 13:25:19"), "%c", "Thu Nov 30 13:25:19 2000",
       id="locale"),
    pp(dt("2000.1130 13:25:19"), "%I:%M:%S %p", "01:25:19 PM",
       id="12 hour"),
    ])
def test_strftime(when, fmt, exp):
    """
    Test strftime
    """
    pytest.dbgfunc()
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
