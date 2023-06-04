from system import System
# all these functions are under contructions
# search for a job or internship
def test_job_search_under_construction(capsys):
    system = System(loggedOn=True)
    system.jobsMenu()
    captured = capsys.readouterr()
    assert "Under Construction" in captured.out
#find someone the user knows friend
def test_find_friend_under_construction(capsys):
    system = System(loggedOn=True)
    system.friendMenu()
    captured = capsys.readouterr()
    assert "Under Construction" in captured.out


