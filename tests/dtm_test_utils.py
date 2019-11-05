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


# -----------------------------------------------------------------------------
def unsupp_a(opd, left, right):
    """
    Format an unsupported operand type message wrapped in a TypeError exception
    """
    msg = "unsupported operand type(s) for {}:  <{}> and <{}>"
    return TypeError(msg.format(opd, left, right))


# -----------------------------------------------------------------------------
def operate(op, left, right):
    """
    Apply the indicated operator to support generality in cmp_exception()
    """
    if op == '==':
        return left == right
    elif op == '!=':
        return left != right
    elif op == '<':
        return left < right
    elif op == '<=':
        return left <= right
    elif op == '>':
        return left > right
    elif op == '>=':
        return left >= right


# -----------------------------------------------------------------------------
def cmp_exception(op, left, right, exp):
    """
    Generalize tests for comparison operators with exception handling
    """
    if isinstance(exp, Exception):
        with pytest.raises(type(exp)) as err:
            operate(op, left, right)
        assert str(exp) in str(err.value)
    else:
        assert operate(op, left, right) is exp
