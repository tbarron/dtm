import pytest
import pytz
import tzlocal


pp = pytest.param
tz_utc = pytz.timezone('utc')
tz_csdt = pytz.timezone('cst6cdt')
tz_esdt = pytz.timezone('est5edt')
tz_local = tzlocal.get_localzone()


# -----------------------------------------------------------------------------
def unsupp(opd, left, right):
    """
    Format an unsupported operand type message wrapped in a TypeError exception
    """
    msg = "unsupported operand type(s) for {}: '{}' and '{}'"
    return TypeError(msg.format(opd, left, right))
