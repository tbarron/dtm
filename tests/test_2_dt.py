from datetime import datetime
from dtm import dt, dt_error, version
import pytest
import pytz
import tzlocal


pp = pytest.param
tz_utc = pytz.timezone('utc')
tz_csdt = pytz.timezone('cst6cdt')
tz_local = tzlocal.get_localzone()


# -----------------------------------------------------------------------------
def test_attributes():
    """
    A dt object should have members _utc and _tz
    """
    pytest.dbgfunc()
    act = dt()
    assert hasattr(act, '_utc')
    assert hasattr(act, '_tz')


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("spec, itz, fmt, otz, exp", [
    pp("2019.1001", None, "%F", None, "2019-10-01",
       id="default -> default"),
    pp("2019.1001", None, "%F %T", 'utc',
       datetime(2019, 10, 1).astimezone(tz_utc).strftime("%F %T"),
       id="default -> utc"),
    pp("2019.1001 17:00:00", None, "%F %T", 'cst6cdt',
       datetime(2019, 10, 1, 17, 0, 0).astimezone(tz_csdt).strftime("%F %T"),
       id="default -> cdt"),
    pp("2019.1001 13:00:00", 'pst8pdt', "%F %T", 'cst6cdt',
       "2019-10-01 15:00:00",
       id="pdt -> cdt"),
    pp("2019.1001 13:00:00", 'pst8pdt', "%F %T", None, "2019-10-01 13:00:00",
       id="pdt -> default"),
    pp("2011.0528 16:00:00", 'cet', "%F %T", 'mst7mdt', "2011-05-28 08:00:00",
       id="cet -> mdt"),
    pp("2010.1010 10:10:10", 'NZ', None, 'Pacific/Midway',
       "2010-10-09-10:10:10",
       id="NZ -> Midway"),

    pp("2019.0310 01:00:00", 'est', "%F %T", 'utc', "2019-03-10 06:00:00",
       id=" * * * DST entry 2019.0310 * * * "),
    pp("2019.0310 01:59:59", 'est5edt', "%F %T", 'utc', "2019-03-10 06:59:59",
       id="01:59:59 est == 06:59:59 utc"),

    pp("2019.0310 02:00:00", 'est5edt', "%F %T", 'utc', "2019-03-10 07:00:00",
       id="02:00:00 est == 07:00:00 utc"),
    pp("2019.0310 02:30:00", 'est5edt', "%F %T", 'utc', "2019-03-10 07:30:00",
       id="02:30:00 est == 07:30:00 utc"),
    pp("2019.0310 02:59:59", 'est5edt', "%F %T", 'utc', "2019-03-10 07:59:59",
       id="02:59:59 est == 07:59:59 utc"),

    pp("2019.0310 03:00:00", 'est5edt', "%F %T", 'utc', "2019-03-10 07:00:00",
       id="03:00:00 EDT == 07:00:00 utc"),
    pp("2019.0310 03:00:01", 'est5edt', "%F %T", 'utc', "2019-03-10 07:00:01",
       id="03:00:01 EDT == 07:00:01 utc"),
    pp("2019.0310 03:59:59", 'est5edt', "%F %T", 'utc', "2019-03-10 07:59:59",
       id="03:59:59 EDT == 07:59:59 utc"),

    pp("2019.0310 04:00:00", 'est5edt', "%F %T", 'utc', "2019-03-10 08:00:00",
       id="04:00:00 EDT == 08:00:00 utc"),

    pp("2019.1103 00:00:00", 'est5edt', "%F %T", 'utc', "2019-11-03 04:00:00",
       id=" * * * DST exit 2019.1103 * * * "),
    pp("2019.1103 00:59:59", 'est5edt', "%F %T", 'utc', "2019-11-03 04:59:59",
       id="00:59:59 EDT == 04:59:59 utc"),
    pp("2019.1103 00:59:59", 'est', "%F %T", 'utc', "2019-11-03 05:59:59",
       id="00:59:59 est == 05:59:59 utc"),
    pp("2019.1103 01:00:00", 'est5edt', "%F %T", 'utc', "2019-11-03 06:00:00",
       id="01:00:00 est == 06:00:00 utc"),
    ])
def test_call(spec, itz, fmt, otz, exp):
    """
    A dt object initialized with *spec* and *itz* should produce *exp* when
    __call__()ed with *fmt* and *otz*.
    """
    pytest.dbgfunc()
    x = dt(spec, tz=itz) if itz else dt(spec)
    args = [fmt] if fmt else []
    kw = {'tz': otz} if otz else {}
    result = x(*args, **kw)
    assert result == exp


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("nub, exp", [
    pp(dt(2001, 2, 3, 4, 5, 6, tz='utc'),
       datetime(2001, 2, 3, 4, 5, 6, tzinfo=tz_utc), id="simple utc"),
    pp(dt(2005, 10, 7),
       datetime(2005, 10, 7, tzinfo=tz_local), id="local"),
    pp(dt(2009, 12, 31, tz='cst6cdt'),
       datetime(2009, 12, 31, tzinfo=tz_csdt), id="central"),
    ])
def test_datetime_x(nub, exp):
    """
    Given a dt object, x, we should be able to ask for x.datetime() and get a
    corresponding datetime object.
    """
    pytest.dbgfunc()
    nub.datetime() == exp


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("inp, exp", [
    pp((), None, id="no arg"),
    pp(datetime(2001, 9, 11), dt(epoch=datetime(2001, 9, 11).timestamp()),
       id="datetime epoch"),
    pp("2001.0911", dt(epoch=datetime(2001, 9, 11).timestamp()),
       id="str ymd"),
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
@pytest.mark.parametrize("inp, itz, otz, exp", [
    pp(1552197600, 'utc', 'utc', "2019-03-10 06:00:00 UTC+0000",
       id="01: * * * DST entry 2019.0310 * * * "),
    pp(1552201199, 'utc', 'est5edt', "2019-03-10 01:59:59 EST-0500",
       id="02: 1552201199 == 01:59:59 EST-0500"),
    pp(1552201200, 'utc', 'est', "2019-03-10 02:00:00 EST-0500",
       id="03: 1552201200 == 02:00:00 EST-0500"),
    pp(1552204799, 'utc', 'est', "2019-03-10 02:59:59 EST-0500",
       id="04: 1552204799 == 02:59:59 EST-0500"),
    pp(1552201200, 'utc', 'est5edt', "2019-03-10 03:00:00 EDT-0400",
       id="05: 1552201200 == 03:00:00 EDT-0400"),
    pp(1552204799, 'utc', 'est5edt', "2019-03-10 03:59:59 EDT-0400",
       id="06: 1552204799 == 03:59:59 EDT-0400"),
    pp(1552204800, 'utc', 'est', "2019-03-10 03:00:00 EST-0500",
       id="07: 1552204800 == 03:00:00 EST-0500"),
    pp(1552204800, 'utc', 'est5edt', "2019-03-10 04:00:00 EDT-0400",
       id="08: 1552204800 == 04:00:00 EDT-0400"),

    pp(1572753600, 'utc', 'est5edt', "2019-11-03 00:00:00 EDT-0400",
       id=" * * * DST exit 2019.1103 * * * "),
    pp(1572757199, 'utc', 'est5edt', "2019-11-03 00:59:59 EDT-0400",
       id="1572757199 == 00:59:59 EDT-0400"),
    pp(1572757200, 'utc', 'est5edt', "2019-11-03 01:00:00 EDT-0400",
       id="1572757200 == 01:00:00 EDT-0400"),
    pp(1572760799, 'utc', 'est5edt', "2019-11-03 01:59:59 EDT-0400",
       id="1572760799 == 01:59:59 EDT-0400"),
    pp(1572760800, 'utc', 'est5edt', "2019-11-03 01:00:00 EST-0500",
       id="1572760800 == 01:00:00 EST-0500"),
    pp(1572764399, 'utc', 'est5edt', "2019-11-03 01:59:59 EST-0500",
       id="1572764399 == 01:59:59 EST-0500"),
    pp(1572764400, 'utc', 'est5edt', "2019-11-03 02:00:00 EST-0500",
       id="1572764400 == 02:00:00 EST-0500"),

    pp(-305319600, pytz.timezone('cst6cdt'), 'est5edt',
       "1960-04-29 00:00:00 EST-0500", id="tzobj constructor input"),
    ])
def test_init_epoch(inp, itz, otz, exp):
    """
    Initializing from an epoch value will always produce the same UTC time
    reference. For the expected value on the right, we have to use tz='utc'
    since the target time reference would vary with timezone if we defaulted to
    the local timezone for the expected value.
    """
    pytest.dbgfunc()
    obj = dt(epoch=inp, tz=itz)
    actual = obj("%F %T %Z%z", tz=otz)
    assert actual == exp


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("inp, itz", [
    pp("2018.0117 08:00:00", 'US/Samoa',
       id="2018.0117 08:00:00 Samoa-1100 == 1516215600"),
    pp("2018.0117 09:00:00", 'US/Hawaii',
       id="09:00:00 Hawaii         -1000 == 1516215600"),
    pp("2018.0117 10:00:00", 'US/Alaska',
       id="10:00:00 Alaska         -0900 == 1516215600"),
    pp("2018.0117 11:00:00", 'pst8pdt',
       id="11:00:00 PST            -0800 == 1516215600"),
    pp("2018.0117 12:00:00", 'mst7mdt',
       id="12:00:00 MST            -0700 == 1516215600"),
    pp("2018.0117 13:00:00", 'cst6cdt',
       id="13:00:00 CST            -0600 == 1516215600"),
    pp("2018.0117 14:00:00", 'est5edt',
       id="14:00:00 EST            -0500 == 1516215600"),
    pp("2018.0117 15:00:00", 'Brazil/West',
       id="15:00:00 Brazil/West    -0400 == 1516215600"),
    pp("2018.0117 16:00:00", 'America/Argentina/Buenos_Aires',
       id="16:00:00 Buenos_Aires   -0300 == 1516215600"),
    pp("2018.0117 17:00:00", 'America/Noronha',
       id="17:00:00 Noronha        -0200 == 1516215600"),
    pp("2018.0117 18:00:00", 'Atlantic/Cape_Verde',
       id="18:00:00 Cape_Verde     -0100 == 1516215600"),
    pp("2018.0117 19:00:00", 'Zulu',
       id="19:00:00 Zulu           +0000 == 1516215600"),
    pp("2018.0117 20:00:00", 'Africa/Lagos',
       id="20:00:00 Lagos          +0100 == 1516215600"),
    pp("2018.0117 21:00:00", 'Africa/Cairo',
       id="21:00:00 Cairo          +0200 == 1516215600"),
    pp("2018.0117 22:00:00", 'Asia/Aden',
       id="22:00:00 Aden           +0300 == 1516215600"),
    pp("2018.0117 23:00:00", 'Asia/Baku',
       id="23:00:00 Baku           +0400 == 1516215600"),
    pp("2018.0118 00:00:00", 'Asia/Oral',
       id="2018.0118 00:00:00 Oral +0500 == 1516215600"),
    pp("2018.0118 01:00:00", 'Asia/Omsk',
       id="01:00:00 Omsk           +0600 == 1516215600"),
    pp("2018.0118 02:00:00", 'Asia/Jakarta',
       id="02:00:00 Jakarta        +0700 == 1516215600"),
    pp("2018.0118 03:00:00", 'Hongkong',
       id="03:00:00 Hong Kong      +0800 == 1516215600"),
    pp("2018.0118 04:00:00", 'Asia/Dili',
       id="04:00:00 Dili           +0900 == 1516215600"),
    pp("2018.0118 05:00:00", 'asia/ust-nera',
       id="05:00:00 Ust-Nera       +1000 == 1516215600"),
    pp("2018.0118 06:00:00", 'Asia/Magadan',
       id="06:00:00 Magadan        +1100 == 1516215600"),
    pp("2018.0118 07:00:00", 'Kwajalein',
       id="07:00:00 Kwajalein      +1200 == 1516215600"),
    pp("2018.0118 08:00:00", 'NZ',
       id="08:00:00 NZ             +1300 == 1516215600"),
    pp("2018.0118 09:00:00", 'Pacific/Apia',
       id="09:00:00 Pacific/Apia   +1400 == 1516215600"),
    ])
def test_init_tz_explicit(inp, itz):
    """
    Specifying an explicit timezone and dtspec should always produce the same
    UTC epoch value
    """
    pytest.dbgfunc()
    actual = dt(inp, tz=itz)
    assert actual._utc == 1516215600


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("locspec, expdt", [
    pp("2018.0117 10:00:00", datetime(2018, 1, 17, 10, 0, 0)),
    pp("2007.0528 07:00:00", datetime(2007, 5, 28, 7, 0, 0)),
    ])
def test_init_tz_local(locspec, expdt):
    """
    In timezone EST5EDT, the test dtspec corresponds to UTC epoch value
    1516201200. In other timezones, it will correspond to other UTC values, so
    we have to get the corresponding epoch value from datetime() to verify that
    the dt constructor with the tz='local' argument is behaving correctly.
    """
    pytest.dbgfunc()
    exp_epoch = expdt.timestamp()
    actual = dt(locspec, tz='local')
    assert actual._utc == exp_epoch


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("spec, itz, epoch", [
    pp("2018.0117 10:00:00", 'utc', 1516183200, id="random epoch"),
    pp("2019.0310 01:00:00", 'est5edt', 1552197600,
       id=" * * * DST entry 2019.0310 * * * "),
    pp("2019.0310 01:59:59", 'est5edt', 1552201199,
       id="01:59:59 est5edt == 1552201199"),
    pp("2019.0310 02:00:00", 'est5edt', 1552201200,
       id="02:00:00 est5edt == 1552201200"),
    pp("2019.0310 02:59:59", 'est5edt', 1552204799,
       id="02:59:59 est5edt == 1552204799"),
    pp("2019.0310 03:00:00", 'est5edt', 1552201200,
       id="03:00:00 est5edt == 1552201200"),
    pp("2019.0310 03:59:59", 'est5edt', 1552204799,
       id="03:59:59 est5edt == 1552204799"),
    pp("2019.0310 03:00:00", 'est', 1552204800,
       id="03:00:00 est     == 1552204800"),
    pp("2019.0310 04:00:00", 'est5edt', 1552204800,
       id="04:00:00 est5edt == 1552204800"),

    pp("2019.1103 00:00:00", 'est5edt', 1572753600,
       id=" * * * DST exit 2019.1103 * * * "),
    pp("2019.1103 00:59:59", 'est5edt', 1572757199,
       id="00:59:59 EDT == 1572757199"),
    pp("2019.1103 00:59:59", 'est', 1572760799,
       id="00:59:59 EST == 1572760799"),
    pp("2019.1103 01:00:00", 'est', 1572760800,
       id="01:00:00 EST == 1572760800"),
    ])
def test_init_tz_utc(spec, itz, epoch):
    """
    In UTC, the test dtspec corresponds to the indicated epoch value.
    """
    pytest.dbgfunc()
    obj = dt(spec, tz=itz)
    exp = dt(epoch=epoch, tz='est5edt')
    assert obj == exp


# -----------------------------------------------------------------------------
def test_init_bad_tz():
    """
    Tickle the exception when tz arg to dt constructor is not a timezone, a
    timezone name, or None.
    """
    with pytest.raises(dt_error) as err:
        dt(1960, 4, 28, 0, 0, 0, tz=17)
    msg = "_static_brew_tz: tz must be timezone, timezone name, or None"
    assert msg in str(err.value)


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("obj, otz, exp", [
    pp(dt("2019.0309 12:00:00", tz='est5edt'), None, "2019-03-09 12:00:00",
       id="0309 12 est -> 0309 12 est"),
    pp(dt("2019.0309 12:00:00", tz='est5edt'), 'utc', "2019-03-09 17:00:00",
       id="0309 12 est -> 0309 17 utc"),

    pp(dt("2019.0310 01:00:00", tz='est5edt'), 'utc', "2019-03-10 06:00:00",
       id=" * * * DST entry 2019.0310 * * * "),
    pp(dt("2019.0310 01:59:59", tz='est5edt'), 'utc', "2019-03-10 06:59:59",
       id="01:59:59 est == 06:59:59 utc"),

    pp(dt("2019.0310 02:00:00", tz='est5edt'), 'utc', "2019-03-10 07:00:00",
       id="02:00:00 est == 07:00:00 utc"),
    pp(dt("2019.0310 02:30:00", tz='est5edt'), 'utc', "2019-03-10 07:30:00",
       id="02:30:00 est == 07:30:00 utc"),
    pp(dt("2019.0310 02:59:59", tz='est5edt'), 'utc', "2019-03-10 07:59:59",
       id="02:59:59 est == 07:59:59 utc"),

    pp(dt("2019.0310 03:00:00", tz='est5edt'), 'utc', "2019-03-10 07:00:00",
       id="03:00:00 EDT == 07:00:00 utc"),
    pp(dt("2019.0310 03:00:01", tz='est5edt'), 'utc', "2019-03-10 07:00:01",
       id="03:00:01 EDT == 07:00:01 utc"),
    pp(dt("2019.0310 03:59:59", tz='est5edt'), 'utc', "2019-03-10 07:59:59",
       id="03:59:59 EDT == 07:59:59 utc"),

    pp(dt("2019.0310 04:00:00", tz='est5edt'), 'utc', "2019-03-10 08:00:00",
       id="04:00:00 EDT == 08:00:00 utc"),

    pp(dt("2019.0310 12:00:00", tz='est5edt'), 'utc', "2019-03-10 16:00:00",
       id="12:00:00 EDT == 16:00:00 utc"),

    pp(dt("2019.1103 00:00:00", tz='est5edt'), 'utc', "2019-11-03 04:00:00",
       id=" * * * DST exit 2019.1103 * * * "),
    pp(dt("2019.1103 00:59:59", tz='est5edt'), 'utc', "2019-11-03 04:59:59",
       id="00:59:59 EDT == 04:59:59 utc"),
    pp(dt("2019.1103 00:59:59", tz='est'), 'utc', "2019-11-03 05:59:59",
       id="00:59:59 est == 05:59:59 utc"),
    pp(dt("2019.1103 01:00:00", tz='est5edt'), 'utc', "2019-11-03 06:00:00",
       id="01:00:00 est == 06:00:00 utc"),
    ])
def test_iso(obj, otz, exp):
    """
    Testing
    """
    pytest.dbgfunc()
    if otz:
        assert obj.iso(tz=otz) == exp
    else:
        assert obj.iso() == exp


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
    pytest.dbgfunc()
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
            assert last.next_day() == day
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
@pytest.mark.parametrize("when, target, exp", [
    pp(dt(2001, 4, 12), 'wed', dt(2011, 4, 13)),
    pp(dt(2001, 4, 12), 'thu', dt(2011, 4, 14)),
    pp(dt(2001, 4, 12), 'fri', dt(2011, 4, 15)),
    pp(dt(2001, 4, 12), 'sat', dt(2011, 4, 16)),
    pp(dt(2001, 4, 12), 'sun', dt(2011, 4, 17)),
    pp(dt(2001, 4, 12), 'mon', dt(2011, 4, 18)),
    pp(dt(2001, 4, 12), 'tue', dt(2011, 4, 19)),
    pp(dt(2001, 4, 12), 3, dt_error("next_weekday requires a string or list")),
    pp(dt(2001, 4, 12), 'january',
       dt_error("one of the targets is not a valid weekday")),
    ])
def test_next_weekday(when, target, exp):
    """
    Test dt().next_weekday(). If today is Monday, dt().next_weekday('mon')
    should be a week from today.
    """
    pytest.dbgfunc()
    if isinstance(exp, dt_error):
        with pytest.raises(dt_error) as err:
            when.next_weekday(target)
        assert str(exp) in str(err.value)
    else:
        when.next_weekday(target) == exp


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
@pytest.mark.parametrize("when, exp", [
    pp(dt(2012, 12, 31, 1, 2, 3, tz="EST5EDT"),
       "dt(2012, 12, 31, 06, 02, 03, tz='EST5EDT')", id="EST5EDT"),
    # pp(dt(2012, 12, 31, 1, 2, 3, tz="local"),
    #    "dt(2012, 12, 31, 06, 02, 03, tz='{}')".format(tz_local),
    #    id="default"),
    pp(dt(2012, 12, 31, 1, 2, 3, tz="UTC"),
       "dt(2012, 12, 31, 01, 02, 03, tz='UTC')", id="UTC"),
    ])
def test_repr(when, exp):
    """
    repr(dt()) should produce a predictable string
    """
    pytest.dbgfunc()
    assert repr(when) == exp


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
    pp(dt(2000, 12, 1, tz='utc'), "%Y.%m%d %H:%M:%S", 'utc',
       "2000.1201 00:00:00",
       id="2000.1201 utc"),

    pp(dt(2000, 12, 1), "%s", None,
       "{}".format(int(datetime(2000, 12, 1).timestamp())), id="epoch"),

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
    pytest.dbgfunc()
    assert dt.version() == version._v
    assert dt().version() == version._v


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("when, fmt, tzone, exp", [
    pp('2016-09-28T16:46:42Z', "%Y-%m-%dT%H:%M:%SZ", None,
       dt(2016, 9, 28, 16, 46, 42), id="iso default tz"),
    pp('2020.0229', "%Y.%m%d", None, dt("2020.0229"), id="ymd default tz"),
    pp('2013.0310 00:00:00', "%Y.%m%d %H:%M:%S", 'utc',
       dt("2013.0310 00:00:00", tz='utc'), id="utc explicit"),

    pp('2013.0310 02:00:00', "%Y.%m%d %H:%M:%S", 'est5edt',
       dt("2013.0310 07:00:00", tz='utc'), id="est 2am -> utc 7am"),
    pp('2013.0310 03:00:00', "%Y.%m%d %H:%M:%S", 'est5edt',
       dt("2013.0310 07:00:00", tz='utc'), id="est 3am -> utc 7am"),

    pp('2013.0310 02:59:59', "%Y.%m%d %H:%M:%S", 'est5edt',
       dt("2013.0310 07:59:59", tz='utc'), id="est 2:59:59 -> utc 7:59:59"),
    pp('2013.0310 03:59:59', "%Y.%m%d %H:%M:%S", 'est5edt',
       dt("2013.0310 07:59:59", tz='utc'), id="est 3:59:59 -> utc 7:59:59"),

    pp('2013.0310 07:00:00', "%Y.%m%d %H:%M:%S", 'utc',
       dt("2013.0310 02:00:00", tz='est5edt'), id="utc 7am -> est 2am"),
    pp('2013.0310 07:00:00', "%Y.%m%d %H:%M:%S", 'utc',
       dt("2013.0310 03:00:00", tz='est5edt'), id="utc 7am -> est 3am"),

    pp('2013.0310 08:00:00', "%Y.%m%d %H:%M:%S", 'utc',
       dt("2013.0310 04:00:00", tz='est5edt'), id="utc 8 -> est 4am"),
    ])
def test_strptime(when, fmt, tzone, exp):
    """
    Test strptime
    """
    pytest.dbgfunc()
    assert dt.strptime(when, fmt, tz=tzone) == exp


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
