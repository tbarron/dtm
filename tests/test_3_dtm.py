"""
Tests for code in dtm/__main__.py
"""
from dtm import dt
import dtm.__main__
import dtm_test_utils as dtu
import pytest
import pytz
import re


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("dtspec, zone, expi, expf, expz", [
    dtu.pp("now", "local", None, "%F %T %Z", 'utc', id="ltu now local"),
    dtu.pp("now", "",  None, "%F %T %Z", 'utc', id="ltu now <empty>"),
    dtu.pp("", "local",  None, "%F %T %Z", 'utc', id="ltu <empty> local"),
    dtu.pp("", "",  None, "%F %T %Z", 'utc', id="ltu <empty> <empty>"),
    dtu.pp("2019.1003", "est5edt", ("2019.1003 04:00:00",), "%F %T %Z", 'utc',
           id="ltu 2019.1003 edt"),
    dtu.pp("2019.0101 02:00:00", "cet", ("2019.0101 01:00:00",), "%F %T %Z",
           'utc', id="ltu 2019.0101 cet"),
    ])
def test_ltu(dtspec, zone, expi, expf, expz, capsys):
    """
    Test function to convert local time to UTC
    """
    pytest.dbgfunc()
    expi = expi or ()
    exp = dt(*expi, tz=expz)(expf, tz=expz)
    kw = {'LOC_DTSPEC': dtspec, 'TIMEZONE': zone, 'd': False}
    dtm.__main__.utc_fr_local_tz(**kw)
    (out, err) = capsys.readouterr()
    assert exp in out, "'{}' not found in '{}'".format(exp, out)


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("dtspec, zone, expi, expf, expz", [
    dtu.pp("", "", None, "%F %T %Z", 'local', id="utl <emtpy> <empty>"),
    dtu.pp("now", "", None, "%F %T %Z", 'local', id="utl now <empty>"),
    dtu.pp("", "local", None, "%F %T %Z", 'local', id="utl <empty> local"),
    dtu.pp("now", "local", None, "%F %T %Z", 'local', id="utl now local"),
    dtu.pp("2019.1003 08:00:00", "est5edt", ("2019.1003 04:00:00",),
           "%F %T %Z", 'est5edt', id="utl 2019.1003 edt"),
    dtu.pp("2019.0101 01:00:00", "cet", ("2019.0101 02:00:00",), "%F %T %Z",
           'cet', id="utl 2019.0101 cet"),
    ])
def test_utl(dtspec, zone, expi, expf, expz, capsys):
    """
    Test function to convert UTC time to another timezone
    """
    pytest.dbgfunc()
    expi = expi or ()
    exp = dt(*expi, tz=expz)(expf, tz=expz)
    kw = {'UTC_DTSPEC': dtspec, 'TIMEZONE': zone, 'd': False}
    dtm.__main__.local_fr_utc_tz(**kw)
    (out, err) = capsys.readouterr()
    assert re.search(exp, out), "'{}' not found in '{}'".format(
        exp, out)


# -----------------------------------------------------------------------------
def test_splat(capsys):
    """
    Code to determine real UTC
    """
    pytest.dbgfunc()
    kw = {'d': False}
    dtm.__main__.splat(**kw)
    (out, err) = capsys.readouterr()
    exps = []
    pytest.dbgfunc()
    for label in ['t', 'n', 'u']:
        exps.append(r"{}: \d+".format(label))
        for x in range(3):
            exps.append(r"\d{4}\.\d{4} \d{2}:\d{2}:\d{2}")
        exps.append(r"\d+\.0")
    for line in out.strip().split("\n"):
        rgx = exps.pop(0)
        assert re.search(rgx, line), "{} doesn't match {}".format(rgx, line)


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("tzname, exp", [
    dtu.pp("EET", ["tzname: EET", "utcoffset: 02:00"]),
    dtu.pp("America/Port_of_Spain", ["utcoffset: -4:00", "tzname: AST"]),
    ])
def test_zdetails(tzname, exp, capsys):
    """
    """
    pytest.dbgfunc()
    kw = {'d': False, 'TIMEZONE': tzname}
    dtm.__main__.zdetails(**kw)
    (out, err) = capsys.readouterr()
    assert all([_ in out for _ in exp])


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("inp, exp", [
    dtu.pp("Guay", ["America/Guayaquil"], id="match 'Guay'"),
    dtu.pp("St_", ["America/St_Barthelemy", "America/St_Johns",
                   "America/St_Kitts", "America/St_Lucia", "America/St_Thomas",
                   "America/St_Vincent", "Atlantic/St_Helena", ],
           id="match 'St_'"),
    dtu.pp("Rio_", ["America/Argentina/Rio_Gallegos", "America/Rio_Branco"],
           id="match 'Rio_'"),
    dtu.pp("ton", ["America/Creston",
                   "America/Edmonton",
                   "America/Moncton",
                   "Pacific/Johnston",
                   "Pacific/Rarotonga"],
           id="match 'ton'")
    ])
def test_zones_search(inp, exp, capsys):
    """
    Testing for 'dtm zones SEARCH'
    """
    pytest.dbgfunc()
    kw = {'d': False, 'SEARCH': inp}
    dtm.__main__.zones(**kw)
    (out, err) = capsys.readouterr()
    assert all([_ in out for _ in exp])
# -----------------------------------------------------------------------------
def test_westeast(capsys):
    """
    Each line should be '<name> ... <hh:mm>'. The hhmm value should constantly
    increase from -12:00 up to 14:00.
    """
    kw = {'d': False}
    dtm.__main__.westeast(**kw)
    (out, err) = capsys.readouterr()
    last = None
    pytest.dbgfunc()
    for line in out.strip().split("\n"):
        (names, hhmms) = line.split()
        (hhs, mms) = hhmms.split(':')
        hh = int(hhs)
        mm = int(mms)
        current = 60*hh + mm
        if last:
            assert last <= current
        last = current
    assert "Etc/GMT+12" in out
    assert "America/Chihuahua" in out
    assert "MST" in out
    assert "America/Inuvik" in out
    assert "Pacific/Kiritimati" in out
