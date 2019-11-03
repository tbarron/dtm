import glob
import inspect
import pytest
import tbx
from importlib import import_module


# -----------------------------------------------------------------------------
def test_flake():
    """
    Check code quality

    Without --ignore, flake8 is happy. When we tell it to --ignore E201, it
    starts calling out the following:

        E123: closing bracket does not match indentation of opening bracket
        E226: missing whitespace around arithmetic operator
        E241: multiple spaces after ','

    I chose to add E226 and E241 to the ignore list but to adjust the trailing
    brackets to clean up the E123 occurrences.

    $FLAKE_IGNORE is defined in $DTM/.env so it's easy to adjust the ignored
    flake errors without changing the test code.
    """
    pytest.dbgfunc()
    globble = sorted(glob.glob("dtm/*.py"))
    globble.extend(sorted(glob.glob("tests/*.py")))
    cmd = "flake8 --ignore $FLAKE_IGNORE {}".format(" ".join(globble))
    result = tbx.run(tbx.expand(cmd))
    assert result == ""


# -----------------------------------------------------------------------------
def test_function_doc():
    """
    Verify that each of our functions have a __doc__ string
    """
    pytest.dbgfunc()

    importables = ['dtm', 'dtm.__main__']
    importables.extend([tbx.basename(_).replace('.py', '')
                        for _ in glob.glob('tests/*.py')])

    missing_doc = []
    for mname in importables:
        mod = import_module(mname)
        for name, obj in inspect.getmembers(mod, inspect.isclass):
            if doc_missing(obj) and name not in missing_doc:
                missing_doc.append(name)

            for mthname, mthobj in inspect.getmembers(obj, inspect.isfunction):
                if doc_missing(mthobj) and mthname not in missing_doc:
                    missing_doc.append("{}.{}".format(name, mthname))

        for name, obj in inspect.getmembers(mod, inspect.isfunction):
            if doc_missing(obj) and name not in missing_doc:
                missing_doc.append("{}.{}".format(mname, name))

    if missing_doc:
        pytest.fail("Items missing __doc__:\n   " + "\n   ".join(missing_doc))


# -----------------------------------------------------------------------------
def doc_missing(obj):
    """
    Check *obj* for a non-empty __doc__ element
    """
    if not hasattr(obj, '__doc__') or obj.__doc__ is None:
        return True
    else:
        return False
