import glob
import pytest
import tbx


# -----------------------------------------------------------------------------
def test_flake():
    """
    Check code quality
    """
    pytest.dbgfunc()
    globble = sorted(glob.glob("tests/test*.py"))
    cmd = "flake8 dtm/__init__.py {}".format(" ".join(globble))
    result = tbx.run(cmd)
    assert result == ""
