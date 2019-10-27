from datetime import datetime
from dtm import dt, dt_error
import dtm_test_utils as dtu
import pytest
import pytz
import tzlocal


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("dtspec, itz, otz, exp", [
    pp("2009.0703", 'est5edt', 'est5edt', "2009-07-03 00:00:00 EDT",
       id="%Y.%m%d"),
    pp("2007.1103 01:59:59", 'est5edt', 'cst6cdt', "2007-11-03 00:59:59 CDT",
       id="%Y.%m%d %H:%M:%S"),
    pp("2007/11/03 02:00", 'est5edt', 'cst6cdt', "2007-11-03 01:00:00 CDT",
       id="%Y/%m/%d %H:%M"),
    pp("2007-11-03T03:00:00Z", 'est5edt', 'cst6cdt', "2007-11-03 02:00:00 CDT",
       id="%Y-%m-%dT%H:%M:%SZ"),
    pp("2008-02-29T23:59:59", 'cst6cdt', 'est5edt', "2008-03-01 00:59:59 EST",
       id="%Y-%m-%dT%H:%M:%S"),
    pp("bad dtspec", None, None,
       dt_error("None of the formats matched 'bad dtspec'"), id="no match"),
    pp("2019.0310 01:00:00", 'est5edt', 'cst6cdt', "2019-03-10 00:00:00 CST",
       id="01:00:00"),
    pp("2019.0310 01:59:59", 'est5edt', 'cst6cdt', "2019-03-10 00:59:59 CST",
       id="01:59:59"),
    pp("2019.0310 02:00:00", 'est5edt', 'cst6cdt', "2019-03-10 01:00:00 CST",
       id="02:00:00"),
    pp("2019.0310 02:59:59", 'est5edt', 'cst6cdt', "2019-03-10 01:59:59 CST",
       id="02:59:59"),
    pp("2019.0310 03:00:00", 'est5edt', 'cst6cdt', "2019-03-10 01:00:00 CST",
       id="02:00:00"),
    pp("2019.0310 03:59:59", 'est5edt', 'cst6cdt', "2019-03-10 01:59:59 CST",
       id="02:59:59"),
    ])
def test_from_format(dtspec, itz, otz, exp):
    """
    Exercise each of the supported formats and fail on at least one unsupported
    one
    """
    pytest.dbgfunc()
    if isinstance(exp, dt_error):
        with pytest.raises(dt_error) as err:
            dt(dtspec, tz=itz)
        assert str(exp) in str(err.value)
    else:
        actual = dt(dtspec, tz=itz)
        assert actual("%F %T %Z", tz=otz) == exp


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("tup, itz, otz, exp", [
    pp((2009, 7, 3), 'est5edt', 'est5edt', "2009-07-03 00:00:00 EDT",
       id="(2009, 7, 3)"),
    pp((2007, 11, 3, 1, 59, 59), 'est5edt', 'cst6cdt',
       "2007-11-03 00:59:59 CDT", id="(2007, 11, 3, 1, 59, 59)"),
    pp((2007, 11, 3, 2, 0), 'est5edt', 'cst6cdt', "2007-11-03 01:00:00 CDT",
       id="2007, 11, 3, 2, 0"),
    pp((2007, 11, 3, 3, 0, 0), 'est5edt', 'cst6cdt', "2007-11-03 02:00:00 CDT",
       id="2007, 11, 3, 3, 0, 0"),
    pp((2008, 2, 29, 23, 59, 59), 'cst6cdt', 'est5edt',
       "2008-03-01 00:59:59 EST", id="(2008, 2, 29, 23, 59, 59)"),
    pp("bad dtspec", None, None,
       dt_error("dt.__init__ expects dt, datetime, str, ints, or epoch=<int>"),
       id="no match"),
    pp((2019, 3, 10, 1, 0, 0), 'est5edt', 'cst6cdt', "2019-03-10 00:00:00 CST",
       id="2019, 3, 10, 1, 0, 0"),
    pp((2019, 3, 10, 1, 59, 59), 'est5edt', 'cst6cdt',
       "2019-03-10 00:59:59 CST", id="(2019, 3, 10, 1, 59, 59)"),
    pp((2019, 3, 10, 2, 0, 0), 'est5edt', 'cst6cdt',
       "2019-03-10 01:00:00 CST", id="2 est == 1 cst"),
    pp((2019, 3, 10, 2, 59, 59), 'est5edt', 'cst6cdt',
       "2019-03-10 01:59:59 CST", id="02:59:59 est = 1:59:59 cst"),
    pp((2019, 3, 10, 3, 0, 0), 'est5edt', 'cst6cdt',
       "2019-03-10 01:00:00 CST", id="3 est == 1 cdt"),
    pp((2019, 3, 10, 3, 59, 59), 'est5edt', 'cst6cdt',
       "2019-03-10 01:59:59 CST", id="02:59:59"),
    ])
def test_from_ints(tup, itz, otz, exp):
    """
    Exercise each of the supported formats and fail on at least one unsupported
    one
    """
    pytest.dbgfunc()
    if isinstance(exp, dt_error):
        with pytest.raises(dt_error) as err:
            dt(*tup, tz=itz)
        assert str(exp) in str(err.value)
    else:
        actual = dt(*tup, tz=itz)
        assert actual("%F %T %Z", tz=otz) == exp


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("inp, exp", [
    pp(pytz.timezone('est5edt'), pytz.timezone('est5edt'), id="tz -> tz"),
    pp('local', tzlocal.get_localzone(), id="'local' -> local tz"),
    pp('est5edt', pytz.timezone('est5edt'), id="tz name -> tz"),
    pp(None, tzlocal.get_localzone(), id="None -> local tz"),
    pp(17,
       dt_error("tz must be timezone, timezone name, or None"),
       id="invalid timezone")
    ])
def test_static_brew_tz(inp, exp):
    """
    This function can take a pytz.BaseTzInfo object, a string containing
    'local' or the name of a timezone, or None.

        tz == pytz.BaseTzInfo        => return tz
        tz == 'local'                => return tzlocal.get_localzone()
        tz == timezone name          => return pytz.timezone(tz)
        tz is None                   => return tzlocal.get_localzone()
        something else               => dt_error( msg )
    """
    pytest.dbgfunc()
    if isinstance(exp, dt_error):
        with pytest.raises(dt_error) as err:
            dt._static_brew_tz(inp)
        assert str(exp) in str(err.value)
    else:
        assert dt._static_brew_tz(inp) == exp


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("obj, itz, exp", [
    pp(dt(), pytz.timezone('est5edt'), pytz.timezone('est5edt'),
       id="tz -> tz"),
    pp(dt(), 'local', tzlocal.get_localzone(),
       id="'local' -> local tz"),
    pp(dt(), 'est5edt', pytz.timezone('est5edt'),
       id="tz name -> tz"),
    pp(dt(), None, tzlocal.get_localzone(),
       id="None -> local tz"),
    pp(dt(), 17,
       dt_error("tz must be timezone, timezone name, or None"),
       id="invalid timezone")
    ])
def test_brew_tz(obj, itz, exp):
    """
    This function can take a pytz.BaseTzInfo object, a string containing
    'local' or the name of a timezone, or None.

        tz is None                   => self._tz
        something else               => _static_brew_tz()
    """
    pytest.dbgfunc()
    if isinstance(exp, dt_error):
        with pytest.raises(dt_error) as err:
            obj._brew_tz(itz)
        assert str(exp) in str(err.value)
    else:
        assert obj._brew_tz(itz) == exp


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("left, right, exp", [
    pp(10, 9, 3600, id="positive ordered"),
    pp(9, 10, -3600, id="negative ordered"),
    pp(0, 23, 3600, id="positive reversed"),
    pp(23, 0, -3600, id="negative reversed"),
    ])
def test_delta(left, right, exp):
    """
    Tests for _delta
    """
    pytest.dbgfunc()
    q = dt()
    assert q._delta(left, right) == exp


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("input, itz, exp", [
    pp(datetime(2019, 3, 10, 1, 59, 59), 'est5edt',
       datetime(2019, 3, 10, 1, 59, 59, tzinfo=tz_esdt),
       id="non-local before"),
    pp(datetime(2019, 3, 10, 2, 0, 0), 'est5edt',
       datetime(2019, 3, 10, 2, 0, 0, tzinfo=tz_esdt), id="non-local after"),

    pp(datetime(2019, 3, 10, 1, 59, 59, tzinfo=tz_esdt), None,
       datetime(2019, 3, 10, 1, 59, 59, tzinfo=tz_esdt), id="local before"),
    pp(datetime(2019, 3, 10, 2, 0, 0, tzinfo=tz_esdt), None,
       datetime(2019, 3, 10, 2, 0, 0, tzinfo=tz_esdt), id="local after"),
    ])
def test_norm_loc(input, itz, exp):
    """
    input: dtspec
    output: normalized and localized datetime object
    """
    pytest.dbgfunc()
    if itz:
        nub = dt(input, tz=itz)
    else:
        nub = dt(input)

    actual = nub._norm_loc_ize(input)
    assert actual == exp
