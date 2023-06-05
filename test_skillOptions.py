from system import System
from unittest.mock import patch


def test_skill(capsys):
  # create an instance of system
  system = System(True)

  # provide 0 as input to exit and capture output
  with patch('builtins.input', side_effect=['0']):
    system.mainMenu()

  # capture output
  captured = capsys.readouterr()

  # check skill option is available
  assert "Learn a Skill" in captured.out


def test_numOfSkills(capsys):
  # create an instance of system
  system = System(True)

  # provide sequence of input to print the skills menu and     exit
  with patch('builtins.input', side_effect=['3', '0', '0']):
    system.mainMenu()

  # capture output
  captured = capsys.readouterr()

  # check that 5 skills are available
  assert "Skill A" in captured.out
  assert "Skill B" in captured.out
  assert "Skill C" in captured.out
  assert "Skill D" in captured.out
  assert "Skill E" in captured.out


""" The following functions test to make sure 
that each of the skills in the menu print the 'Under Construction' message """


def test_skillA(capsys):
  system = System(True)
  system.skillA()
  captured = capsys.readouterr()
  assert "Under Construction" in captured.out


def test_skillB(capsys):
  system = System(True)
  system.skillB()
  captured = capsys.readouterr()
  assert "Under Construction" in captured.out


def test_skillC(capsys):
  system = System(True)
  system.skillC()
  captured = capsys.readouterr()
  assert "Under Construction" in captured.out


def test_skillD(capsys):
  system = System(True)
  system.skillD()
  captured = capsys.readouterr()
  assert "Under Construction" in captured.out


def test_skillE(capsys):
  system = System(True)
  system.skillE()
  captured = capsys.readouterr()
  assert "Under Construction" in captured.out