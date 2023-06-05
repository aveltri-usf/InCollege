from system import System
from unittest.mock import patch

def test_menu(capsys):
  # create an instance of system
  system = System(False)

  # provide 0 as input to exit and capture the printed menu
  with patch('builtins.input', side_effect=['0']):
    system.loginMenu()

  # capture output
  captured = capsys.readouterr()

  # check that all options are printed
  assert "Login" in captured.out
  assert "Create Account" in captured.out
  assert "Exit" in captured.out