"""
Tests for code in dtm/__main__.py
"""
from dtm import dt
import pytest
import re
import dtm.__main__
import dtm_test_utils as dtu


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
