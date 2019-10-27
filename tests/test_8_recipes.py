from datetime import datetime
import dtm_test_utils as dtu
import pytest
import pytz


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("isospec, tz, exp", [
    dtu.pp("2019-10-17 17:00:00", 'utc',     1571331600, id="utc 2019"),
    dtu.pp("2019-10-17 13:00:00", 'est5edt', 1571331600, id="est 2019"),
    dtu.pp("2019-10-17 12:00:00", 'cst6cdt', 1571331600, id="cst 2019"),
    dtu.pp("2019-10-17 11:00:00", 'mst7mdt', 1571331600, id="mst 2019"),
    dtu.pp("2019-10-17 10:00:00", 'pst8pdt', 1571331600, id="pst 2019"),

    dtu.pp("2017-12-17 18:00:00", 'utc',     1513533600, id="utc 2017"),
    dtu.pp("2017-12-17 13:00:00", 'est5edt', 1513533600, id="est 2017"),
    dtu.pp("2017-12-17 12:00:00", 'cst6cdt', 1513533600, id="cst 2017"),
    dtu.pp("2017-12-17 11:00:00", 'mst7mdt', 1513533600, id="mst 2017"),
    dtu.pp("2017-12-17 10:00:00", 'pst8pdt', 1513533600, id="pst 2017"),
    ])
def test_epoch_fr_dtspec_tz(isospec, tz, exp):
    """
    Given a dtspec and timezone, compute the corresponding epoch value (which
    is equivalent to a UTC time reference).
    """
    pytest.dbgfunc()
    fmt = "%Y-%m-%d %H:%M:%S"
    tzobj = pytz.timezone(tz)
    utc = pytz.timezone('utc')
    frog = tzobj.normalize(tzobj.localize(datetime.strptime(isospec, fmt)))
    assert frog.astimezone(utc).timestamp() == exp


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("epoch, tz, isospec", [
    dtu.pp(1571331600, 'utc',     "2019-10-17 17:00:00", id="e + t -> utc"),
    dtu.pp(1571331600, 'est5edt', "2019-10-17 13:00:00", id="e + t -> est"),
    dtu.pp(1571331600, 'cst6cdt', "2019-10-17 12:00:00", id="e + t -> cst"),
    dtu.pp(1571331600, 'mst7mdt', "2019-10-17 11:00:00", id="e + t -> mst"),
    dtu.pp(1571331600, 'pst8pdt', "2019-10-17 10:00:00", id="e + t -> pst"),
    ])
def test_dtspec_fr_epoch_tz(epoch, tz, isospec):
    """
    Given an epoch value and timezone, compute the isoformat dtspec reflecting
    the date and time for the timezone that matches the epoch value
    """
    pytest.dbgfunc()
    fmt = "%Y-%m-%d %H:%M:%S"
    q = datetime.fromtimestamp(epoch)
    tz = pytz.timezone(tz)
    assert q.astimezone(tz).strftime(fmt) == isospec
