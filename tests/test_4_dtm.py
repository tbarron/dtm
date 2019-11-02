"""
Tests for code in dtm/__main__.py
"""
from dtm import dt, td
import dtm.__main__ as dtmain
import dtm_test_utils as dtu
import pytest
import pytz
import re


# -----------------------------------------------------------------------------
# There are 28 month calendars:
#     length: [28, 29, 30, 31]
#     start: ['mo', 'tu', 'we', 'th', 'fr', 'sa', 'su']
@pytest.mark.parametrize("inp, wkday, length", [
    dtu.pp("1971.0201", "mo", 28),
    dtu.pp("1977.0201", "tu", 28),
    dtu.pp("1978.0201", "we", 28),
    dtu.pp("1973.0208", "th", 28),
    dtu.pp("1974.0208", "fr", 28),
    dtu.pp("1975.0208", "sa", 28),
    dtu.pp("1970.0208", "su", 28),

    dtu.pp("1988.0201", "mo", 29),
    dtu.pp("1972.0201", "tu", 29),
    dtu.pp("1984.0201", "we", 29),
    dtu.pp("1996.0208", "th", 29),
    dtu.pp("1980.0208", "fr", 29),
    dtu.pp("1992.0208", "sa", 29),
    dtu.pp("1976.0208", "su", 29),

    dtu.pp("2019.0428", "mo", 30),
    dtu.pp("2016.1119", "tu", 30),
    dtu.pp("2017.1118", "we", 30),
    dtu.pp("2018.1117", "th", 30),
    dtu.pp("2019.1107", "fr", 30),
    dtu.pp("2019.0606", "sa", 30),
    dtu.pp("2019.0905", "su", 30),

    dtu.pp("2018.0131", "mo", 31),
    dtu.pp("2019.0130", "tu", 31),
    dtu.pp("2018.0808", "we", 31),
    dtu.pp("2018.0331", "th", 31),
    dtu.pp("2017.1212", "fr", 31),
    dtu.pp("2018.1219", "sa", 31),
    dtu.pp("2018.0704", "su", 31),
    ])
def test_calendar(inp, wkday, length, capsys):
    """
    Test for 'dtm calendar DTSPEC', which should produce the calendar for the
    month indicated by DTSPEC.
    """
    kw = {'d': False, 'DTSPEC': inp}
    dtmain.calendar(**kw)
    (out, err) = capsys.readouterr()
    exp = month_ref(wkday, length)
    pytest.dbgfunc()
    assert exp in out, "\n{} \n  not in \n\n{}".format(exp, out)


# -----------------------------------------------------------------------------
def test_calendar_now(capsys):
    """
    Test 'dtm calendar' for the current month
    """
    kw = {'d': False, 'DTSPEC': None}
    when = dt()
    mday = int(when("%d"))
    start = when.previous_day(mday - 1)
    end = when.next_day(32 - mday)
    while end("%b") != start("%b"):
        end = end.previous_day()

    exp = month_ref(start.weekday(), int(end("%d")))
    dtmain.calendar(**kw)
    (out, err) = capsys.readouterr()
    pytest.dbgfunc()
    assert exp in out, "\n{} \n  not in \n\n{}".format(exp, out)


# -----------------------------------------------------------------------------
def month_ref(wkday, length):
    """
    This function provides a reference for each of the 28 possible months.
    *wkday* is the starting day of the month ('sun', 'mon', 'tue', etc.) and
    *length* is the number of days in the month [28 ... 31].
    """
    head = "mo tu we th fr sa su"
    ref = " " + head + "\n"
    lspaces = dtmain.weekday_ordinal(wkday) - 1
    slot = 0
    for q in range(lspaces):
        ref += "   "
        slot += 1
    for day in range(length):
        ref += " {:2d}".format(day + 1)
        slot += 1
        if slot % 7 == 0:
            ref += "\n"
    while slot % 7 != 0:
        ref += "   "
        slot += 1
    return ref


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
    dtmain.utc_fr_local_tz(**kw)
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
    dtmain.local_fr_utc_tz(**kw)
    (out, err) = capsys.readouterr()
    assert re.search(exp, out), "'{}' not found in '{}'".format(
        exp, out)


# -----------------------------------------------------------------------------
# @pytest.mark.parametrize
def test_rdt(capsys):
    """
    Test dtm_rdt
    """
    inp = 1947230258
    kw = {'EPOCH': inp, 'd': False}
    foo = dt(epoch=inp)
    dtmain.dtm_rdt(**kw)
    (out, err) = capsys.readouterr()
    exp = "{} (epoch = {})".format(foo("%F-%T"), inp)
    assert exp in out


# -----------------------------------------------------------------------------
def test_rtd(capsys):
    """
    Test dtm_rtd
    """
    inp = 28299
    kw = {'SECONDS': inp, 'd': False}
    nub = td(inp)
    dtmain.dtm_rtd(**kw)
    (out, err) = capsys.readouterr()
    exp = "{} (seconds = {})".format(str(nub), nub._duration)
    assert exp in out


# -----------------------------------------------------------------------------
def test_splat(capsys):
    """
    Code to determine real UTC
    """
    pytest.dbgfunc()
    kw = {'d': False}
    dtmain.splat(**kw)
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
    dtmain.zdetails(**kw)
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
    dtmain.zones(**kw)
    (out, err) = capsys.readouterr()
    assert all([_ in out for _ in exp])


# -----------------------------------------------------------------------------
def test_zones_raw(capsys):
    """
    Verify that all the timezones show up in 'dtm zones -r' output
    """
    pytest.dbgfunc()
    kw = {'d': False, 'r': True, 'SEARCH': None}
    dtmain.zones(**kw)
    (out, err) = capsys.readouterr()
    assert all([_ in out for _ in pytz.all_timezones])
    for critical in ['CET', 'EET']:
        assert critical in out


# -----------------------------------------------------------------------------
def test_zones_noargs(capsys):
    """
    Code to display and browse timezones
    """
    pytest.dbgfunc()
    kw = {'d': False, 'r': False, 'SEARCH': None}
    dtmain.zones(**kw)
    (out, err) = capsys.readouterr()

    names = {}
    for tz in pytz.all_timezones:
        for name in tz.split('/'):
            names[name] = 1
    for name in names:
        assert name in out


# -----------------------------------------------------------------------------
def test_westeast(capsys):
    """
    Each line should be '<name> ... <hh:mm>'. The hhmm value should constantly
    increase from -12:00 up to 14:00.
    """
    kw = {'d': False}
    dtmain.westeast(**kw)
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
