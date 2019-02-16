"""
Customizations for pytest
"""
import pdb
import pytest


# -----------------------------------------------------------------------------
def pytest_addoption(parser):
    """
    Adding pytest command line options
    """
    parser.addoption("--dbg", action='append', default=[],
                     help="start debugger on named test or all")


# -----------------------------------------------------------------------------
def pytest_runtest_setup(item):
    """
    Setting things up before running a test

    If we put '--dbg all', we'll get a debugger break at the beginning of each
    test collected and run

    If we put '--dbg TESTNAME' on the command line, we'll get a debugger break
    at the beginning of test TESTNAME.

    If we put '--dbg ..TESTNAME', we'll break in this function as it's setting
    up for TESTNAME.

    If we put '--dbg ..all', we'll break in this function as it's setting
    up for each test.
    """
    dbg_n = '..' + item.name
    dbg_l = item.config.getvalue('dbg')

    if dbg_n in dbg_l or '..all' in dbg_l:
        pdb.set_trace()

    pytest.dbgfunc = lambda: None
    if any([item.name in dbg_l, 'all' in dbg_l] +
           [x in item.name for x in dbg_l]):
        pytest.dbgfunc = pdb.set_trace
