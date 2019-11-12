import pytest
import pytz
import tzlocal


pp = pytest.param
ppf = pytest.test_id_formatter
tz_utc = pytz.timezone('utc')
tz_csdt = pytz.timezone('cst6cdt')
tz_esdt = pytz.timezone('est5edt')
tz_local = tzlocal.get_localzone()


# -----------------------------------------------------------------------------
def lrx_exc_test(op, left, right, exp):
    """
    General test structure for carrying out an operation, catching and checking
    an exception if it should be raised, and validating the result of the
    operation otherwise.
    """
    if isinstance(exp, Exception):
        with pytest.raises(type(exp)) as err:
            eval(op)
        assert str(exp) in str(err.value)
    else:
        actual = eval(op)
        assert actual == exp, "{} != {}".format(actual, exp)


# -----------------------------------------------------------------------------
def unsupp(opd, left, right):
    """
    Format an unsupported operand type message wrapped in a TypeError exception
    """
    msg = "unsupported operand type(s) for {}: '{}' and '{}'"
    return TypeError(msg.format(opd, left, right))


# -----------------------------------------------------------------------------
def unsupp_cmp(left, right):
    """
    Format an unsupported operand type message wrapped in a TypeError exception
    specifically for comparison routines
    """
    msg = "unsupported operand type(s) for comparison:  <{}> and <{}>"
    return TypeError(msg.format(left, right))


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
        assert str(exp) in str(err.value), ("\n'{}'\n    not in\n'{}'"
                                            .format(str(exp), str(err.value)))
    else:
        result = operate(op, left, right)
        assert result is exp, "{} is not {}".format(result, exp)


"""
==TAGGABLE==
"""
