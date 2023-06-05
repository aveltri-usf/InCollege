import pytest
from unittest import mock
from system import System


# creates an instance of the system class to be used for testing
@pytest.fixture
def system_instance():
    return System(False)


# tests the return/exit option in the skills menu
# allowing users to return to the main/top level menu
def test_return_option(system_instance, capfd):
    exit_opt = "[0] Exit\n"
    main_menu_opts = ['Job/Internship Search', 'Find A Friend', 'Learn a Skill']
    skills = ['Skill A', 'Skill B', 'Skill C', 'Skill D', 'Skill E']
    # construct options for main and skill menus
    skill_choices = [f"[{i+1}] Learn {skill}\n" for i, skill in enumerate(skills)]
    main_choices = [f"[{i+1}] {name}\n" for i, name in enumerate(main_menu_opts)]
    main_choices += exit_opt
    skill_choices += exit_opt
    # construct full prompts for main and skill menu
    main_prompt = ''.join(main_choices)
    skill_prompt = ''.join(skill_choices)
    expected_output = main_prompt + skill_prompt + main_prompt + "Exiting"

    # simulated inputs: learn a skill, return to main menu, exit app
    inputs = ['3', '0', '0']

    # run the main menu with the simulated inputs
    with mock.patch('builtins.input', side_effect=inputs):
        system_instance.mainMenu()

    # confirm output matches with expected
    std = capfd.readouterr()
    assert std.out.strip() == expected_output
