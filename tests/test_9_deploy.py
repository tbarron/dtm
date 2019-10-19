from dtm import dt
import pytest
import tbx


# -----------------------------------------------------------------------------
def test_deployable():
    """
    Check that 1) no untracked files are hanging out, 2) no staged but
    uncommitted updates are outstanding, 3) no unstaged, uncommitted changes
    are outstanding, 4) the most recent git tag matches HEAD, and 5) the most
    recent git tag matches the current version.
    """
    pytest.dbgfunc()
    staged, changed, untracked = tbx.git_status()
    assert untracked == [], "You have untracked files"
    assert changed == [], "You have unstaged updates"
    assert staged == [], "You have updates staged but not committed"

    if tbx.git_current_branch() != 'master':
        return True

    last_tag = tbx.git_last_tag()
    msg = "Version ({}) does not match tag ({})".format(tbx.version(),
                                                        last_tag)
    assert dt.version() == last_tag, msg
    assert tbx.git_hash() == tbx.git_hash(last_tag), "Tag != HEAD"
