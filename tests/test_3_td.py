from datetime import timedelta
from dtm import dt_error, td
import dtm_test_utils as dtu
import pytest
# import pytz
# import tbx


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("args, kw, exp", [
    dtu.pp((15, ), {}, td(secs=15), id="args: (s < 60,)"),
    dtu.pp((90, ), {}, td(mins=1, secs=30), id="args: (60 < s,)"),
    dtu.pp((1, 1), {}, td(secs=61), id="args: (m, s)"),
    dtu.pp((1, 1, 1), {}, td(secs=3661), id="args: (h, m, s)"),
    dtu.pp((1, 1, 1, 1), {}, td(secs=90061), id="args: (d, h, m, s)"),

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
    dtu.pp((-1, ), {}, ValueError("td cannot be negative"),
           id="fail: negative td"),
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
        assert actual == exp


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("left, right, exp", [
    dtu.pp(td(0), td(0), True, id="      0 ==    00:00:00"),
    dtu.pp(td(120), td(2, 0), True, id="   120s ==    00:02:00"),
    dtu.pp(td(120), td(2, 1), False, id="   120s !=    00:02:01"),
    dtu.pp(td(10921), td(3, 2, 1), True, id=" 10921s ==    03:02:01"),
    dtu.pp(td(10921), td(3, 2, 2), False, id=" 10921s !=    03:02:00"),
    dtu.pp(td(356521), td(4, 3, 2, 1), True, id="356521s == 4d+03:02:01"),
    dtu.pp(td(356500), td(4, 3, 2, 1), False, id="356500s != 4d+03:02:01"),
    dtu.pp(td(25), timedelta(0, 25), True, id="td(25) == timedelta(0, 25)"),
    dtu.pp(td(59), timedelta(0, 25), False, id="td(59) != timedelta(0, 25)"),
    dtu.pp(timedelta(0, 25), td(25), True, id="timedelta(0, 25) == td(25)"),
    dtu.pp(timedelta(0, 14), td(25), False, id="timedelta(0, 25) != td(25)"),
    dtu.pp(td(17), 17, True, id="number == td()"),
    dtu.pp(td(55), 17, False, id="number != td()"),
    dtu.pp(td(55), "17",
           ValueError("td can be compared to number, td, or timedelta,"
                      " but not to <class 'str'>"),
           id="number =/= td()"),
    dtu.pp(td(55), ["17", 19, 35],
           ValueError("td can be compared to number, td, or timedelta,"
                      " but not to <class 'list'>"),
           id="list =/= td()"),

    ])
def test_td_eq(left, right, exp):
    """
    Test td.__eq__()
    """
    pytest.dbgfunc()
    if isinstance(exp, Exception):
        with pytest.raises(type(exp)) as err:
            assert (left == right) is exp
        assert str(exp) in str(err.value)
    else:
        assert (left == right) is exp


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
