from system import System


def test_job_search_under_construction(capsys):
    system = System(loggedOn=True)
    system.jobsMenu()
    captured = capsys.readouterr()
    assert "Under Construction" in captured.out

def test_find_friend_under_construction(capsys):
    system = System(loggedOn=True)
    system.friendMenu()
    captured = capsys.readouterr()
    assert "Under Construction" in captured.out


def test_skill_a_under_construction(capsys):
    system = System(loggedOn=True)
    system.skillA()
    captured = capsys.readouterr()
    assert "Under Construction" in captured.out
