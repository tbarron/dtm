from datetime import datetime, timedelta
from dtm import dt, dt_error, td
import dtm_test_utils as dtu
import pytest


# -----------------------------------------------------------------------------
def test_td_attrs():
    """
    Check that a new td object has all the right attributes
    """
    a = td()
    assert hasattr(a, '_duration')


# -----------------------------------------------------------------------------
# test_td_init()
@pytest.mark.parametrize("args, kw, exp", [
    dtu.pp((15, ), {}, td(secs=15), id="args: (s < 60,)"),
    dtu.pp((90, ), {}, td(mins=1, secs=30), id="args: (60 < s,)"),
    dtu.pp((1, 1), {}, td(secs=61), id="args: (m, s)"),
    dtu.pp((1, 1, 1), {}, td(secs=3661), id="args: (h, m, s)"),
    dtu.pp((1, 1, 1, 1), {}, td(secs=90061), id="args: (d, h, m, s)"),
    dtu.pp((-1, ), {}, td(secs=-1), id="negative td okay"),
    dtu.pp((-3, 10, 7), {}, td(secs=-10193), id="net negative"),

    dtu.pp((), {'s': 95}, td(1, 35), id="kw: {s}"),
    dtu.pp((), {'m': 75}, td(4500), id="kw: {m}"),
    dtu.pp((), {'m': 5, 's': 105}, td(405), id="kw: {m, s}"),
    dtu.pp((), {'h': 3}, td(10800), id="kw: {h}"),
    dtu.pp((), {'h': 3, 's': 5}, td(10805), id="kw: {h, s}"),
    dtu.pp((), {'h': 3, 'm': 7}, td(11220), id="kw: {h, m}"),
    dtu.pp((), {'h': 5, 'm': 3, 's': 1}, td(18181), id="kw: {h, m, s}"),
    dtu.pp((), {'d': 2}, td(172800), id="kw: {d}"),
    dtu.pp((), {'d': 2, 's': 15}, td(172815), id="kw: {d, s}"),
    dtu.pp((), {'d': 2, 'm': 15}, td(173700), id="kw: {d, m}"),
    dtu.pp((), {'d': 2, 'h': 3}, td(183600), id="kw: {d, h}"),
    dtu.pp((), {'d': 3, 'h': 2, 'm': 1}, td(266460), id="kw: {d, h, m}"),
    dtu.pp((), {'d': 4, 'h': 3, 's': 1}, td(356401), id="kw: {d, h, s}"),
    dtu.pp((), {'d': 4, 'h': 3, 'm': 2, 's': 1}, td(356521),
           id="kw: {d, h, m, s}"),

    dtu.pp((timedelta(0, 17, 0), ), {}, td(17), id="args: (timedelta())"),

    dtu.pp((), {'s': 5, 'secs': 32},
           dt_error("Mutually exclusive arguments: s, secs, seconds"),
           id="fail: seconds"),
    dtu.pp((), {'s': 5, 'secs': 32},
           dt_error("Mutually exclusive arguments: s, secs, seconds"),
           id="fail: seconds"),
    dtu.pp((), {'mins': 4, 'minutes': 8, 'seconds': 55},
           dt_error("Mutually exclusive arguments: m, mins, minutes"),
           id="fail: minutes"),
    dtu.pp((), {'s': 0, 'm': 0, 'h': 2, 'hours': 17},
           dt_error("Mutually exclusive arguments: h, hrs, hours"),
           id="fail: hours"),
    dtu.pp((), {'d': 1, 'days': 5, 's': 12, 'm': 5, 'h': 17},
           dt_error("Mutually exclusive arguments: d, days"),
           id="fail: days"),
    dtu.pp((1, 2, 3), {'h': 1, 'm': 2, 's': 3},
           dt_error("Expected either *args or *kw, not both"),
           id="fail: not both"),
])
def test_td_init(args, kw, exp):
    """
    Tests for td.__init__()
    """
    pytest.dbgfunc()
    if isinstance(exp, Exception):
        with pytest.raises(type(exp)) as err:
            actual = td(*args, **kw)
        assert str(exp) in str(err.value)
    else:
        actual = td(*args, **kw)
        assert actual == exp, "exp - act = {}".format(exp._secs() -
                                                      actual._secs())


# -----------------------------------------------------------------------------
# test_td_add()
@pytest.mark.parametrize("left, right, exp", [
    dtu.pp(td(300), td(7), td(307), id="td+01: <td> + <td> => <td>"),
    dtu.pp(td(300), td(-25), td(275), id="td+02: <td> + (-)<td> => <td>"),
    dtu.pp(td(-300), td(7), td(-293), id="td+03: (-)<td> + <td> => <td>"),
    dtu.pp(td(-300), td(-25), td(-325), id="td+04: (-)<td> + (-)<td> => <td>"),

    dtu.pp(td(300), timedelta(0, 15), td(315),
           id="td+03: <td> + <timedelta> => <td>"),
    dtu.pp(td(300), timedelta(0, -72), td(228),
           id="td+04: <td> + (-)<timedelta> => <td>"),
    dtu.pp(td(-300), timedelta(0, 15), td(-285),
           id="td+03: (-)<td> + <timedelta> => <td>"),
    dtu.pp(td(-300), timedelta(0, -72), td(-372),
           id="td+04: (-)<td> + (-)<timedelta> => <td>"),

    dtu.pp(timedelta(0, 35), td(75), td(110),
           id="td+05: <timedelta> + <td> => <td>"),
    dtu.pp(timedelta(0, 35), td(-75), td(-40),
           id="td+06: <timedelta> + (-)<td> => <td>"),
    dtu.pp(timedelta(0, -35), td(75), td(40),
           id="td+07: (-)<timedelta> + <td> => <td>"),
    dtu.pp(timedelta(0, -35), td(-75), td(-110),
           id="td+08: (-)<timedelta> + (-)<td> => <td>"),

    dtu.pp(td(400), 750, td(1150), id="td+09: <td> + <int> => <td>"),
    dtu.pp(td(400), -75, td(325), id="td+10: <td> + <int> => <td>"),
    dtu.pp(td(-430), 750, td(320), id="td+11: <td> + <int> => <td>"),
    dtu.pp(td(-800), -750, td(-1550), id="td+12: <td> + <int> => <td>"),

    dtu.pp(234, td(822), td(1056), id="td+13: <int> + <td> => <td>"),
    dtu.pp(283, td(-876), td(-593), id="td+14: <int> + <td> => <td>"),
    dtu.pp(-677, td(285), td(-392), id="td+15: <int> + <td> => <td>"),
    dtu.pp(-848, td(-180), td(-1028), id="td+16: <int> + <td> => <td>"),

    dtu.pp(td(17), datetime(2015, 1, 1, 8, 0, 0), dt("2015.0101 08:00:17"),
           id="dt+17: <td> + <datetime> => <dt>"),
    dtu.pp(td(-552), datetime(2009, 4, 5, 6, 7, 8), dt("2009.0405 05:57:56"),
           id="dt+18: <td> + <datetime> => <dt>"),

    dtu.pp(datetime(1986, 6, 2, 13, 42, 40), td(910), dt("1986.0602 13:57:50"),
           id="dt+19: <datetime> + <td> => <dt>"),
    dtu.pp(datetime(1977, 9, 14, 12, 17, 2), td(-2655),
           dt("1977.0914 11:32:47"), id="dt+20: <datetime> + <td> => <dt>"),

    dtu.pp(td(), [1, 2, 3], dtu.unsupp('+', 'td', 'list'),
           id="dt+21: <td> + <list> => TypeError"),
    dtu.pp({}, td(), dtu.unsupp('+', 'dict', 'td'),
           id="dt+22: <dict> + <td> => TypeError"),
])
def test_td_add(left, right, exp):
    """
    Test td.__add__()
    """
    pytest.dbgfunc()
    if isinstance(exp, Exception):
        with pytest.raises(type(exp)) as err:
            actual = left + right
        assert str(exp) in str(err.value)
    else:
        actual = left + right
        assert actual == exp, "exp - act = {}".format(exp._secs() -
                                                      actual._secs())


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("left, right, exp", [
    dtu.pp(td(1, 15, 0), td(450), td(h=1, m=7, s=30),
           id="td-01: <td> - <td> => +<td>"),
    dtu.pp(td(m=36, s=46), td(-12, -54), td(2980),
           id="td-02: <td> - <td> => -<td>"),

    dtu.pp(td(6735), timedelta(0, 804), td(h=1, m=38, s=51),
           id="td-03: <td> - <timedelta> => +<td>"),
    dtu.pp(td(6496), timedelta(0, -128), td(6624),
           id="td-04: <td> - <timedelta> => -<td>"),

    dtu.pp(timedelta(0, 2453), td(923), td(1530),
           id="td-05: <timedelta> - <td> => +<td>"),
    dtu.pp(timedelta(0, 6000), td(-851), td(6851),
           id="td-06: <timedelta> - <td> => -<td>"),

    dtu.pp(datetime(1972, 12, 16, 20, 16, 44), td(9, 33, 41),
           dt("1972.1216 10:43:03"), id="td-07: <datetime> - <td> => <dt>"),
    dtu.pp(datetime(2021, 4, 8, 1, 21, 14), td(-48311),
           dt("2021.0408 14:46:25"), id="td-08: <datetime> - (-)<td> => <dt>"),

    dtu.pp(td(32194), 18611, td(13583), id="td-09: <td> - <int> => <td>"),
    dtu.pp(70684, td(-1401), td(72085), id="td-10: <int> - <td> => <td>"),

    dtu.pp(td(77055), dt("1978.0120 17:54:38"), dtu.unsupp('-', 'td', 'dt'),
           id="td-11: <td> - <dt> => TypeError"),
    dtu.pp(td(56725), datetime(1997, 3, 3, 18, 49, 27),
           dtu.unsupp('-', 'td', 'datetime.datetime'),
           id="td-12: <td> - <datetime> => TypeError"),
])
def test_td_sub(left, right, exp):
    """
    Tests for td.__sub__()
    """
    pytest.dbgfunc()
    if isinstance(exp, Exception):
        with pytest.raises(type(exp)) as err:
            actual = left - right
        assert str(exp) in str(err.value)
    else:
        actual = left - right
        assert actual == exp, "exp - act = {}".format(exp._secs() -
                                                      actual._secs())


# -----------------------------------------------------------------------------
# td.__mul__
@pytest.mark.parametrize("left, right, exp", [
    dtu.pp(td(25), 3, td(75), id="td(25) * 3 == td(75)"),
    dtu.pp(3, td(25), td(75), id="3 * td(25) == td(75)"),
    dtu.pp(td(30), 5.25, td(round(30*5.25)), id="td(30) * 5.25 == td(158)"),
    dtu.pp(5.75, td(30), td(round(5.75*30)), id="5.75 * td(30) == td(172)"),
    dtu.pp(td(7), td(5), dtu.unsupp('*', 'td', 'td'),
           id="td * td => TypeErr"),
    dtu.pp(td(7), dt(), dtu.unsupp('*', 'td', 'dt'),
           id="td * dt => TypeErr"),
    dtu.pp(dt(), td(7), dtu.unsupp('*', 'dt', 'td'),
           id="dt * td => TypeErr"),
    dtu.pp(td(7), timedelta(), dtu.unsupp('*', 'td', 'datetime.timedelta'),
           id="td * timedelta => TypeErr"),
    dtu.pp(timedelta(), td(7), dtu.unsupp('*', 'datetime.timedelta', 'td'),
           id="timedelta * td => TypeErr"),
    dtu.pp(td(7), datetime.now(), dtu.unsupp('*', 'td', 'datetime.datetime'),
           id="td * datetime => TypeErr"),
    dtu.pp(datetime.now(), td(7), dtu.unsupp('*', 'datetime.datetime', 'td'),
           id="datetime * td => TypeErr"),
])
def test_td_mul(left, right, exp):
    """
    Test td.__mul__()
    """
    pytest.dbgfunc()
    if isinstance(exp, Exception):
        with pytest.raises(type(exp)) as err:
            left * right
        assert str(exp) in str(err.value)
    else:
        actual = left * right
        assert actual == exp, "{} != {}".format(actual, exp)


# -----------------------------------------------------------------------------
# td.__floordiv__
@pytest.mark.parametrize("left, right, exp", [
    dtu.pp(td(45), 3, td(15), id="td(45) // 3 == td(15)"),
    dtu.pp(35, td(7), dtu.unsupp('//', 'int', 'td'),
           id="35 // td(7) => TypeErr"),
    dtu.pp(td(17), 3.5, td(4), id="td(17) // 3.5 == td(4)"),
    dtu.pp(47.85, td(17), dtu.unsupp('//', 'float', 'td'),
           id="47.85 // td(17) => TypeErr"),
    dtu.pp(td(17), dt(), dtu.unsupp('//', 'td', 'dt'),
           id="td() // dt() => TypeErr"),
    dtu.pp(td(17), timedelta(), dtu.unsupp('//', 'td', 'datetime.timedelta'),
           id="td() // timedelta() => TypeErr"),
    dtu.pp(timedelta(), td(17), dtu.unsupp('//', 'datetime.timedelta', 'td'),
           id="timedelta() // td() => TypeErr"),
    dtu.pp(td(17), datetime.now(), dtu.unsupp('//', 'td', 'datetime.datetime'),
           id="td() // datetime() => TypeErr"),
    dtu.pp(datetime.now(), td(17), dtu.unsupp('//', 'datetime.datetime', 'td'),
           id="datetime() // td() => TypeErr"),
])
def test_td_floordiv(left, right, exp):
    """
    Test td.__floordiv__()
    """
    pytest.dbgfunc()
    if isinstance(exp, Exception):
        with pytest.raises(type(exp)) as err:
            left // right
        assert str(exp) in str(err.value)
    else:
        actual = left // right
        assert actual == exp, "{} != {}".format(actual, exp)


# -----------------------------------------------------------------------------
# td.__truediv__
@pytest.mark.parametrize("left, right, exp", [
    dtu.pp(td(45), 3, td(15), id=ppf("td(45) / 3 == td(15)", "T", w=44)),
    dtu.pp(td(9), 10, td(1), id=ppf("td(9) / 10 == td(1)", "T", w=44)),
    dtu.pp(35, td(7), dtu.unsupp('/', 'int', 'td'),
           id=ppf("35 / td(7) => TypeErr", "X", w=44)),
    dtu.pp(td(17), 3.5, td(5), id=ppf("td(17) / 3.5 == td(5)", "T", w=44)),
    dtu.pp(47.85, td(17), dtu.unsupp('/', 'float', 'td'),
           id=ppf("47.85 / td(17) => TypeErr", "X", w=44)),
    dtu.pp(td(17), dt(), dtu.unsupp('/', 'td', 'dt'),
           id=ppf("td() / dt() => TypeErr", "X", w=44)),
    dtu.pp(td(17), timedelta(), dtu.unsupp('/', 'td', 'datetime.timedelta'),
           id=ppf("td() / timedelta() => TypeErr", "X", w=44)),
    dtu.pp(timedelta(), td(17), dtu.unsupp('/', 'datetime.timedelta', 'td'),
           id=ppf("timedelta() / td() => TypeErr", "X", w=44)),
    dtu.pp(td(17), datetime.now(), dtu.unsupp('/', 'td', 'datetime.datetime'),
           id=ppf("td() / datetime() => TypeErr", "X", w=44)),
    dtu.pp(datetime.now(), td(17), dtu.unsupp('/', 'datetime.datetime', 'td'),
           id=ppf("datetime() / td() => TypeErr", "X", w=44)),
])
def test_td_truediv(left, right, exp):
    """
    Test td.__truediv__()
    """
    pytest.dbgfunc()
    if isinstance(exp, Exception):
        with pytest.raises(type(exp)) as err:
            left / right
        assert str(exp) in str(err.value)
    else:
        actual = left / right
        assert actual == exp, "{} != {}".format(actual, exp)


    pytest.fail('construction')


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("left, right, exp", [
    dtu.pp(td(0), td(0), True, id=dtu.F("0 == 00:00:00", "T")),
    dtu.pp(td(120), td(2, 0), True, id=dtu.F("120s == 00:02:00", "T")),
    dtu.pp(td(120), td(2, 1), False, id=dtu.F("120s == 00:02:01", "F")),
    dtu.pp(td(10921), td(3, 2, 1), True, id=dtu.F("10921s == 03:02:01", "T")),
    dtu.pp(td(10921), td(3, 2, 2), False, id=dtu.F("10921s == 03:02:00", "F")),
    dtu.pp(td(356521), td(4, 3, 2, 1), True,
           id=dtu.F("356521s == 4d+03:02:01", "T")),
    dtu.pp(td(356500), td(4, 3, 2, 1), False,
           id=dtu.F("356500s == 4d+03:02:01", "F")),
    dtu.pp(td(25), timedelta(0, 25), True,
           id=dtu.F("td(25) == timedelta(0), 25)", "T")),
    dtu.pp(td(59), timedelta(0, 25), False,
           id=dtu.F("td(59) == timedelta(0), 25)", "F")),
    dtu.pp(timedelta(0, 25), td(25), True,
           id=dtu.F("timedelta(0), 25) == td(25)", "T")),
    dtu.pp(timedelta(0, 14), td(25), False,
           id=dtu.F("timedelta(0), 25) == td(25)", "F")),
    dtu.pp(td(17), 17, True, id=dtu.F("td(17) == 17", "T")),
    dtu.pp(td(55), 17, False, id=dtu.F("td(55) == 17", "F")),
    dtu.pp(17, td(17), True, id=dtu.F("17 == td(17)", "T")),
    dtu.pp(17, td(55), False, id=dtu.F("17 == td(55)", "F")),

    dtu.pp(td(55), "17", dtu.unsupp_cmp('td', "class 'str'"),
           id=dtu.F("td() == str", "X")),
    dtu.pp("17", td(55), dtu.unsupp_cmp('td', "class 'str'"),
           id=dtu.F("str == td", "X")),
    dtu.pp(td(55), ["17", 19, 35], dtu.unsupp_cmp('td', "class 'list'"),
           id=dtu.F("td() == list", "X")),
    dtu.pp(["17", 19, 35], td(32), dtu.unsupp_cmp('td', "class 'list'"),
           id=dtu.F("list == td()", "X")),
    dtu.pp(td(17), dt(), dtu.unsupp_cmp('td', "class 'dtm.dt'"),
           id=dtu.F("td() == dt", "X")),
])
def test_td_cmp_eq(left, right, exp):
    """
    Test td.__eq__()
    """
    pytest.dbgfunc()
    dtu.cmp_exception('==', left, right, exp)


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("left, right, exp", [
    dtu.pp(td(1, 1), td(60), True, id=dtu.F("td(61) != td(60)", "T")),
    dtu.pp(td(1, 1), td(61), False, id=dtu.F("td(61) != td(61)", "F")),

    dtu.pp(td(1, 1), timedelta(0, 60), True,
           id=dtu.F("td(61) != timedelta(60)", "T")),
    dtu.pp(td(1, 1), timedelta(0, 61), False,
           id=dtu.F("td(61) != timedelta(61)", "F")),
    dtu.pp(timedelta(0, 60), td(1, 1), True,
           id=dtu.F("timedelta(60) != td(61)", "T")),
    dtu.pp(timedelta(0, 61), td(1, 1), False,
           id=dtu.F("timedelta(61) != td(61)", "F")),

    dtu.pp(td(1, 1), 60, True, id=dtu.F("td(61) != 60", "T")),
    dtu.pp(td(1, 1), 61, False, id=dtu.F("td(61) != 61", "F")),
    dtu.pp(58, td(1, 1), True, id=dtu.F("60 != td(61)", "T")),
    dtu.pp(31 + 30, td(1, 1), False, id=dtu.F("61 != td(61)", "F")),

    dtu.pp(td(55), "17", dtu.unsupp_cmp('td', "class 'str'"),
           id=dtu.F("td() != str", "X")),
    dtu.pp("17", td(55), dtu.unsupp_cmp('td', "class 'str'"),
           id=dtu.F("str != td()", "X")),
    dtu.pp(td(55), ["17", 19, 35], dtu.unsupp_cmp('td', "class 'list'"),
           id=dtu.F("td() != list", "X")),
    dtu.pp(["17", 19, 35], td(55), dtu.unsupp_cmp('td', "class 'list'"),
           id=dtu.F("list != td()", "X")),
    dtu.pp(td(55), dt(), dtu.unsupp_cmp('td', "class 'dtm.dt'"),
           id=dtu.F("td() != dt", "X")),
])
def test_td_cmp_ne(left, right, exp):
    """
    Test td != something else
    """
    pytest.dbgfunc()
    dtu.cmp_exception('!=', left, right, exp)


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("left, right, exp", [
    dtu.pp(td(0), td(0), True, id=dtu.F("0 >= 00:00:00", "T")),
    dtu.pp(td(120), td(2, 0), True, id=dtu.F("120s >= 00:02:00", "T")),
    dtu.pp(td(120), td(2, 1), False, id=dtu.F("120s >= 00:02:01", "F")),
    dtu.pp(td(2, 1), td(120), True, id=dtu.F("00:02:01 >= 120s", "T")),
    dtu.pp(td(10921), td(3, 2, 1), True, id=dtu.F("10921s >= 03:02:01", "T")),
    dtu.pp(td(10921), td(3, 2, 2), False, id=dtu.F("10921s >= 03:02:02", "F")),
    dtu.pp(td(356521), td(4, 3, 2, 1), True,
           id=dtu.F("356521s >= 4d+03:02:01", "T")),
    dtu.pp(td(356500), td(4, 3, 2, 1), False,
           id=dtu.F("356500s >= 4d+03:02:01", "F")),
    dtu.pp(td(25), timedelta(0, 25), True,
           id=dtu.F("td(25) >= timedelta(0, 25)", "T")),
    dtu.pp(td(59), timedelta(0, 25), True,
           id=dtu.F("td(59) >= timedelta(0, 25)", "T")),
    dtu.pp(timedelta(0, 25), td(25), True,
           id=dtu.F("timedelta(0,25) >= td(25)", "T")),
    dtu.pp(timedelta(0, 14), td(25), False,
           id=dtu.F("timedelta(0,14) >= td(25)", "F")),
    dtu.pp(td(12), 17, False, id=dtu.F("td(12) >= 17", "F")),
    dtu.pp(td(17), 17, True, id=dtu.F("td(17) >= 17", "T")),
    dtu.pp(td(55), 17, True, id=dtu.F("td(55) >= 17", "T")),
    dtu.pp(95, td(96), False, id=dtu.F("95 >= td(96)", "F")),
    dtu.pp(25, td(25), True, id=dtu.F("25 >= td(25)", "T")),
    dtu.pp(56, td(55), True, id=dtu.F("56 >= td(55)", "T")),

    dtu.pp(td(55), "17", dtu.unsupp_cmp('td', "class 'str'"),
           id=dtu.F("td() >= str", "X")),
    dtu.pp("17", td(55), dtu.unsupp_cmp('td', "class 'str'"),
           id=dtu.F("str >= td()", "X")),
    dtu.pp(td(55), ["17", 19, 35], dtu.unsupp_cmp('td', "class 'list'"),
           id=dtu.F("td() >= list", "X")),
    dtu.pp(["17", 19, 35], td(55), dtu.unsupp_cmp('td', "class 'list'"),
           id=dtu.F("list >= td()", "X")),
    dtu.pp(td(19), dt("2002.0407"), dtu.unsupp_cmp('td', "class 'dtm.dt'"),
           id=dtu.F("td() >= dt()", "X")),
])
def test_td_cmp_ge(left, right, exp):
    """
    Test td.__ge__()
    """
    pytest.dbgfunc()
    dtu.cmp_exception('>=', left, right, exp)


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("left, right, exp", [
    dtu.pp(td(0), td(0), False, id=dtu.F("0 > 00:00:00", "F")),
    dtu.pp(td(120), td(2, 0), False, id=dtu.F("120s > 00:02:00", "F")),
    dtu.pp(td(120), td(2, 1), False, id=dtu.F("120s > 00:02:01", "T")),
    dtu.pp(td(2, 1), td(120), True, id=dtu.F("00:02:01 > 120s", "T")),
    dtu.pp(td(10921), td(3, 2, 1), False,     id=dtu.F("10921s > 03:02:01",
                                                       "F")),
    dtu.pp(td(10921), td(3, 2, 2), False,     id=dtu.F("10921s > 03:02:02",
                                                       "F")),
    dtu.pp(td(356521), td(4, 3, 2, 1), False, id=dtu.F("356521s > 4d+03:02:01",
                                                       "F")),
    dtu.pp(td(356500), td(4, 3, 2, 1), False, id=dtu.F("356500s > 4d+03:02:01",
                                                       "F")),
    dtu.pp(td(25), timedelta(0, 25), False,
           id=dtu.F("td(25)  > timedelta(0, 25)", "F")),
    dtu.pp(td(59), timedelta(0, 25), True,
           id=dtu.F("td(59)  > timedelta(0, 25)", "T")),
    dtu.pp(timedelta(0, 25), td(25), False,
           id=dtu.F("timedelta(0, 25) !> td(25)", "F")),
    dtu.pp(timedelta(0, 14), td(25), False,
           id=dtu.F("timedelta(0, 14) !> td(25)", "F")),
    dtu.pp(td(17), 17, False, id=dtu.F("td(17) > 17", "F")),
    dtu.pp(td(25), 25, False, id=dtu.F("td(25) > 25", "F")),
    dtu.pp(td(55), 17, True, id=dtu.F("td(55) > 17", "T")),
    dtu.pp(17, td(25), False, id=dtu.F("17 > td(25)", "F")),
    dtu.pp(25, td(25), False, id=dtu.F("25 > td(25)", "F")),
    dtu.pp(37, td(25), True, id=dtu.F("37 > td(25)", "T")),

    dtu.pp(td(55), "17", dtu.unsupp_cmp('td', "class 'str'"),
           id=dtu.F("td() > str", "X")),
    dtu.pp("17", td(55), dtu.unsupp_cmp('td', "class 'str'"),
           id=dtu.F("str > td()", "X")),
    dtu.pp(td(55), ["17", 19, 35], dtu.unsupp_cmp('td', "class 'list'"),
           id=dtu.F("td() > list", "X")),
    dtu.pp(["17", 19, 35], td(55), dtu.unsupp_cmp('td', "class 'list'"),
           id=dtu.F("list > td()", "X")),
    dtu.pp(td(19), dt("2002.0407"), dtu.unsupp_cmp('td', "class 'dtm.dt'"),
           id=dtu.F("td() > dt()", "X")),
])
def test_td_cmp_gt(left, right, exp):
    """
    Test td.__gt__()
    """
    pytest.dbgfunc()
    dtu.cmp_exception('>', left, right, exp)


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("left, right, exp", [
    dtu.pp(td(0), td(0), False, id=dtu.F("0 < 00:00:00", "F")),
    dtu.pp(td(120), td(2, 0), False, id=dtu.F("120s < 00:02:00", "F")),
    dtu.pp(td(120), td(2, 1), True, id=dtu.F("120s < 00:02:01", "T")),
    dtu.pp(td(2, 1), td(120), False, id=dtu.F("00:02:01 < 120s", "F")),
    dtu.pp(td(10921), td(3, 2, 1), False, id=dtu.F("10921s < 03:02:01", "F")),
    dtu.pp(td(10921), td(3, 2, 2), True, id=dtu.F("10921s < 03:02:02", "T")),
    dtu.pp(td(93783), td(1, 2, 3, 4), True,
           id=dtu.F("93783s < 1d+02:03:04", "F")),
    dtu.pp(td(93784), td(1, 2, 3, 4), False,
           id=dtu.F("93784s < 1d+02:03:04", "F")),
    dtu.pp(td(93785), td(1, 2, 3, 4), False,
           id=dtu.F("93785s < 1d+02:03:04", "F")),
    dtu.pp(td(25), timedelta(0, 25), False,
           id=dtu.F("td(25) < timedelta(0, 25)", "F")),
    dtu.pp(td(59), timedelta(0, 25), False,
           id=dtu.F("td(59) < timedelta(0, 25)", "F")),
    dtu.pp(timedelta(0, 25), td(25), False,
           id=dtu.F("timedelta(0, 25) < td(25)", "F")),
    dtu.pp(timedelta(0, 14), td(25), True,
           id=dtu.F("timedelta(0, 14) < td(25)", "T")),
    dtu.pp(td(12), 17, True, id=dtu.F("td(12) < 17", "T")),
    dtu.pp(td(17), 17, False, id=dtu.F("td(17) < 17", "F")),
    dtu.pp(td(55), 17, False, id=dtu.F("td(55) < 55", "F")),
    dtu.pp(98, td(97), False, id=dtu.F("98 < td(97)", "F")),
    dtu.pp(98, td(98), False, id=dtu.F("98 < td(98)", "F")),
    dtu.pp(98, td(99), True, id=dtu.F("98 < td(99)", "T")),

    dtu.pp(td(55), "17",
           dtu.unsupp_cmp('td', "class 'str'"), id=dtu.F("td() < str", "X")),
    dtu.pp("17", td(55),
           dtu.unsupp_cmp('td', "class 'str'"), id=dtu.F(" str < td()", "X")),
    dtu.pp(td(55), ["17", 19, 35],
           dtu.unsupp_cmp('td', "class 'list'"), id=dtu.F("td() < list", "X")),
    dtu.pp(["17", 19, 35], td(55),
           dtu.unsupp_cmp('td', "class 'list'"), id=dtu.F("list < td()", "X")),
    dtu.pp(td(19), dt("2002.0407"),
           dtu.unsupp_cmp('td', "class 'dtm.dt'"),
           id=dtu.F("td() < dt()", "X")),
])
def test_td_cmp_lt(left, right, exp):
    """
    Test td.__lt__()
    """
    pytest.dbgfunc()
    dtu.cmp_exception('<', left, right, exp)


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("left, right, exp", [
    dtu.pp(td(0), td(0), True, id=dtu.F("0 <= 00:00:00", "T")),
    dtu.pp(td(120), td(2, 0), True, id=dtu.F("120s <= 00:02:00", "T")),
    dtu.pp(td(120), td(2, 1), True, id=dtu.F("120s <= 00:02:01", "T")),
    dtu.pp(td(2, 1), td(120), False, id=dtu.F("00:02:01 <= 120s", " F")),
    dtu.pp(td(10921), td(3, 2, 1), True, id=dtu.F("10921s <= 03:02:01", "T")),
    dtu.pp(td(10921), td(3, 2, 2), True, id=dtu.F("10921s <= 03:02:02", "T")),
    dtu.pp(td(356521), td(4, 3, 2, 1), True, id=dtu.F("356521s <= 4d03:02:01",
                                                      "T")),
    dtu.pp(td(356500), td(4, 3, 2, 1), True,
           id=dtu.F("356500s <= 4d03:02:01", "T")),
    dtu.pp(td(93785), td(1, 2, 3, 4), False,
           id=dtu.F("93785s <= 1d02:03:04", "F")),
    dtu.pp(td(25), timedelta(0, 25), True,
           id=dtu.F("td(25) <= timedelta(0, 25)", "T")),
    dtu.pp(td(59), timedelta(0, 25), False,
           id=dtu.F("td(59) <= timedelta(0, 25)", "F")),
    dtu.pp(timedelta(0, 25), td(25), True,
           id=dtu.F("timedelta(0, 25) <= td(25)", "T")),
    dtu.pp(timedelta(0, 14), td(25), True,
           id=dtu.F("timedelta(0, 14) <= td(25)", "T")),
    dtu.pp(td(12), 17, True, id=dtu.F("td(12) <= 17", "T  ")),
    dtu.pp(td(17), 17, True, id=dtu.F("td(17) <= 17", "T  ")),
    dtu.pp(td(55), 17, False, id=dtu.F("td(55) <= 55", "F ")),
    dtu.pp(17, td(19), True, id=dtu.F("17 < td(19)", "T  ")),
    dtu.pp(19, td(19), True, id=dtu.F("19 < td(19)", "T  ")),
    dtu.pp(21, td(19), False, id=dtu.F("21 < td(19)", "F ")),

    dtu.pp(td(55), "17", dtu.unsupp_cmp('td', "class 'str'"),
           id=dtu.F("td() <= str", "X")),
    dtu.pp("17", td(55), dtu.unsupp_cmp('td', "class 'str'"),
           id=dtu.F("str <= td()", "X")),
    dtu.pp(td(55), ["17", 19, 35], dtu.unsupp_cmp('td', "class 'list'"),
           id=dtu.F("td() <= list", "X")),
    dtu.pp(["17", 19, 35], td(55), dtu.unsupp_cmp('td', "class 'list'"),
           id=dtu.F("list <= td()", "X")),
    dtu.pp(td(19), dt("2002.0407"), dtu.unsupp_cmp('td', "class 'dtm.dt'"),
           id=dtu.F("td() <= dt()", "X")),
])
def test_td_cmp_le(left, right, exp):
    """
    Test td.__le__()
    """
    pytest.dbgfunc()
    dtu.cmp_exception('<=', left, right, exp)


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("obj, exp", [
    dtu.pp(td(27), "<dtm.td(27)>", id="27"),
    dtu.pp(td(7, 13), "<dtm.td(433)>", id="433"),
    dtu.pp(td(1, 0, 0), "<dtm.td(3600)>", id="3600"),
    dtu.pp(td(1, -1, 0), "<dtm.td(3540)>", id="3540"),
    dtu.pp(td(1, 0, -1), "<dtm.td(3599)>", id="3599"),
])
def test_td_repr(obj, exp):
    """
    Test td.__repr__()
    """
    assert repr(obj) == exp


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("obj, exp", [
    dtu.pp(td(43), "0d00:00:43", id="< minute"),
    dtu.pp(td(143), "0d00:02:23", id="< hour"),
    dtu.pp(td(72015), "0d20:00:15", id="< day"),
    dtu.pp(td(937231), "10d20:20:31", id="day <"),
    dtu.pp(dt("2010.1231 11:59:59") - dt("2010.0101"), "364d11:59:59",
           id="str(dt() - dt())"),
])
def test_td_str(obj, exp):
    """
    Test td.__str__()
    """
    assert str(obj) == exp


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("inp, exp", [
    dtu.pp(0, 0, id="0 seconds => 0 days"),
    dtu.pp(1, 1/(24*3600), id="1 seconds => {} days".format(1/(24*3600))),
    dtu.pp(60, 1/(24*60), id="60 seconds => {} days".format(1/(24*60))),
    dtu.pp(3600, 1/24, id="3600 seconds => {} days".format(1/24)),
    dtu.pp(6*3600, 0.25, id="21600 seconds => 0.25 days"),
    dtu.pp(12*3600, 0.50, id="43200 seconds => 0.5 days"),
    dtu.pp(24*3600, 1, id="86400 seconds => 1 days"),
])
def test_td_days(inp, exp):
    """
    Test td.days()
    """
    obj = td(inp)
    assert obj.days() == exp


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("inp, exp", [
    dtu.pp(0, 0, id="0 seconds => 0 hours"),
    dtu.pp(1, 1/3600, id="1 seconds => {} hours".format(1/3600)),
    dtu.pp(60, 1/60, id="60 seconds => {} hours".format(1/(60))),
    dtu.pp(3600, 1, id="3600 seconds => 1 hours"),
    dtu.pp(6*3600, 6, id="21600 seconds => 6 hours"),
    dtu.pp(12*3600, 12, id="43200 seconds => 12 hours"),
    dtu.pp(24*3600, 24, id="86400 seconds => 24 hours"),
])
def test_td_hours(inp, exp):
    """
    Test td.hours()
    """
    obj = td(inp)
    assert obj.hours() == exp


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("inp, exp", [
    dtu.pp(0, 0, id="0 seconds => 0 minutes"),
    dtu.pp(1, 1/60, id="1 seconds => {} minutes".format(1/60)),
    dtu.pp(63, 1.05, id="63 seconds => {} minutes".format(63/60)),
    dtu.pp(3239, 3239/60, id="3239 seconds => {} minutes".format(3239/60)),
    dtu.pp(17991, 17991/60, id="17991 seconds => {} minutes".format(17991/60)),
    dtu.pp(42299, 42299/60, id="42299 seconds => {} minutes".format(42299/60)),
    dtu.pp(56914, 56914/60, id="56914 seconds => {} minutes".format(56914/60)),
])
def test_td_minutes(inp, exp):
    """
    Test td.minutes()
    """
    obj = td(inp)
    assert obj.minutes() == exp


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("inp, exp", [
    dtu.pp((1, 0), 60, id="(1, 0) => 60 seconds"),
    dtu.pp((2, 3), 123, id="(2, 3) => 123 seconds"),
    dtu.pp((1, 2, 3), 3723, id="(1, 2, 3) => 3723"),
    dtu.pp((1, 2, 3, 4), 93784, id="(1, 2, 3, 4) => {}".format(93784)),
    dtu.pp((4, 3, 2, 1), 356521, id="(4, 3, 2, 1) => {}".format(356521)),
    dtu.pp((10, 17), 617, id="(10, 17) => 617 seconds"),
    dtu.pp((16, 3), 963, id="(16, 3) => 963"),
])
def test_td_seconds(inp, exp):
    """
    Test td.minutes()
    """
    obj = td(*inp)
    assert obj.seconds() == exp


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("inp, exp", [
    dtu.pp(-928385,   "-10d17:53:05", id="-10d17:53:05"),
    dtu.pp(-756914,    "-8d18:15:14", id=" -8d18:15:14"),
    dtu.pp( -17991,    "-0d04:59:51", id=" -0d04:59:51"),
    dtu.pp(      0,     "0d00:00:00", id="  0d00:00:00"),
    dtu.pp(      1,     "0d00:00:01", id="  0d00:00:01"),
    dtu.pp(     63,     "0d00:01:03", id="  0d00:01:03"),
    dtu.pp(   3239,     "0d00:53:59", id="  0d00:53:59"),
    dtu.pp(  17991,     "0d04:59:51", id="  0d04:59:51"),
    dtu.pp(  42299,     "0d11:44:59", id="  0d11:44:59"),
    dtu.pp( 756914,     "8d18:15:14", id="  8d18:15:14"),
])
def test_td_dhhmmss(inp, exp):
    """
    test td.dhhmmss()
    """
    pytest.dbgfunc()
    obj = td(inp)
    assert obj.dhhmmss() == exp


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("inp, exp", [
    dtu.pp(-928385,   (-10, -17, -53, -5), id="-10d17:53:05"),
    dtu.pp(-756914,   (-8, -18, -15, -14), id=" -8d18:15:14"),
    dtu.pp( -17991,     (0, -4, -59, -51), id=" -0d04:59:51"),
    dtu.pp(      0,          (0, 0, 0, 0), id="  0d00:00:00"),
    dtu.pp(      1,          (0, 0, 0, 1), id="  0d00:00:01"),
    dtu.pp(     63,          (0, 0, 1, 3), id="  0d00:01:03"),
    dtu.pp(   3239,        (0, 0, 53, 59), id="  0d00:53:59"),
    dtu.pp(  17991,        (0, 4, 59, 51), id="  0d04:59:51"),
    dtu.pp(  42299,       (0, 11, 44, 59), id="  0d11:44:59"),
    dtu.pp( 756914,       (8, 18, 15, 14), id="  8d18:15:14"),
])
def test_td_dhms(inp, exp):
    """
    test td.dhhmmss()
    """
    pytest.dbgfunc()
    obj = td(inp)
    assert obj.dhms() == exp


"""
==TAGGABLE==
"""
