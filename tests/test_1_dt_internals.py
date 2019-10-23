from datetime import datetime
from dtm import dt, dt_error
import pytest
import pytz
import tzlocal


pp = pytest.param
tz_utc = pytz.timezone('utc')
tz_esdt = pytz.timezone('est5edt')
tz_csdt = pytz.timezone('cst6cdt')
tz_local = tzlocal.get_localzone()


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("dtspec, itz, otz, exp", [
    pp("2009.0703", None, 'est5edt', "2009-07-03 00:00:00 EDT",
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
    if isinstance(exp, dt_error):
        with pytest.raises(dt_error) as err:
            dt(dtspec, tz=itz)
        assert str(exp) in str(err.value)
    else:
        actual = dt(dtspec, tz=itz)
        assert actual("%F %T %Z", tz=otz) == exp


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("tup, itz, otz, exp", [
    pp((2009, 7, 3), None, 'est5edt', "2009-07-03 00:00:00 EDT",
       id="%Y.%m%d"),
    pp((2007, 11, 3, 1, 59, 59), 'est5edt', 'cst6cdt',
       "2007-11-03 00:59:59 CDT", id="%Y.%m%d %H:%M:%S"),
    pp((2007, 11, 3, 2, 0), 'est5edt', 'cst6cdt', "2007-11-03 01:00:00 CDT",
       id="%Y/%m/%d %H:%M"),
    pp((2007, 11, 3, 3, 0, 0), 'est5edt', 'cst6cdt', "2007-11-03 02:00:00 CDT",
       id="%Y-%m-%dT%H:%M:%SZ"),
    pp((2008, 2, 29, 23, 59, 59), 'cst6cdt', 'est5edt',
       "2008-03-01 00:59:59 EST", id="%Y-%m-%dT%H:%M:%S"),
    pp("bad dtspec", None, None,
       dt_error("dt.__init__ expects dt, datetime, str, ints, or epoch=<int>"),
       id="no match"),
    pp((2019, 3, 10, 1, 0, 0), 'est5edt', 'cst6cdt', "2019-03-10 00:00:00 CST",
       id="01:00:00"),
    pp((2019, 3, 10, 1, 59, 59), 'est5edt', 'cst6cdt',
       "2019-03-10 00:59:59 CST", id="01:59:59"),
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
    if isinstance(exp, dt_error):
        with pytest.raises(dt_error) as err:
            dt(*tup, tz=itz)
        assert str(exp) in str(err.value)
    else:
        actual = dt(*tup, tz=itz)
        assert actual("%F %T %Z", tz=otz) == exp
