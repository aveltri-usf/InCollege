import pytest
import string
import random
from unittest import mock
from system import System

# validate password 
def test_validate_valid_password():
      system = System(loggedOn=False)
      # Call the validate function with a valid password
      valid_password = "ValidPas123!"
      valid_password_again = "ValidPas123!"
      result = system.validatePassword(valid_password,valid_password_again)
      # Assert that the result is True
      assert result is True


# test invalid password 
def test_validate_invalid_password():
        system = System(loggedOn=False)
        # Call the validate function with an invalid password
        invalid_password = "invalid"
        retry = "invalid1"
        result = system.validatePassword(invalid_password,retry)
        # Assert that the result is False
        assert result is False  


def test_login_successful(capsys):
    # Instantiate the System class
    system = System(loggedOn=True)

    # Set up a test user account
    test_username = "user"
    test_password = "Testpassword1*"
    system.cursor.execute("INSERT INTO accounts (username, password) VALUES (?, ?)", (test_username, system.encryption(test_password)))
    system.conn.commit()

    # Call the login method with the correct credentials
    result = system.login(test_username, test_password)

    # Assert the expected behavior

    captured = capsys.readouterr()
    assert "You have successfully logged in!" in captured.out
    assert result is True
    assert system.loggedOn is True

    # Clean up the test user account
    system.cursor.execute("DELETE FROM accounts WHERE username=?", (test_username,))
    system.conn.commit()


def test_login_account_not_found():
    # Instantiate the System class
    system = System(loggedOn=False)

    # Call the login method with non-existent credentials
    result = system.login("nonexistentuser", "password")

    # Assert the expected behavior
    assert result is False


def test_invalid_credentials(capsys):
    # Instantiate the System class
    system = System(loggedOn=False)

    # Set up a test user account
    test_username = "user"
    test_password = "Testpassword1*"
    system.cursor.execute("INSERT INTO accounts (username, password) VALUES (?, ?)", (test_username, system.encryption(test_password)))
    system.conn.commit()

    # Call the login method with the correct credentials
    invalidpass= "NoWorkng!*"
    result= system.login(test_username, invalidpass)
     
    # Assert the expected behavior
    assert result is False
    captured = capsys.readouterr()
    assert "Invalid username/password, try again!" in captured.out
    
    # Clean up the test user account
    system.cursor.execute("DELETE FROM accounts WHERE username=?", (test_username,))
    system.conn.commit()


def test_menu(capsys):
  # create an instance of system
  system = System(False)

  # provide 0 as input to exit and capture the printed menu
  with mock.patch('builtins.input', side_effect=['0']):
    system.loginMenu()

  # capture output
  captured = capsys.readouterr()

  # check that all options are printed
  assert "Login" in captured.out
  assert "Create Account" in captured.out
  assert "Exit" in captured.out


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


def test_skill(capsys):
  # create an instance of system
  system = System(True)

  # provide 0 as input to exit and capture output
  with mock.patch('builtins.input', side_effect=['0']):
    system.mainMenu()

  # capture output
  captured = capsys.readouterr()

  # check skill option is available
  assert "Learn a Skill" in captured.out


def test_numOfSkills(capsys):
  # create an instance of system
  system = System(True)

  # provide sequence of input to print the skills menu and     exit
  with mock.patch('builtins.input', side_effect=['3', '0', '0']):
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


# creates an instance of the system class to be used for testing
@pytest.fixture
def system_instance():
    return System(False)


# setup and teardown style method that
# temporarily removes existing accounts from DB when testing
@pytest.fixture
def temp_remove_accounts(system_instance):
    # save and remove all existing accounts
    system_instance.cursor.execute("SELECT * FROM accounts")
    saved_accounts = system_instance.cursor.fetchall()
    if len(saved_accounts) > 0:
        system_instance.cursor.execute("DELETE FROM accounts")
        system_instance.conn.commit()
    yield
    # remove any test accounts and restore saved accounts
    system_instance.cursor.execute("DELETE FROM accounts")
    if len(saved_accounts) > 0:
        system_instance.cursor.executemany("INSERT INTO accounts (username, password) VALUES (?, ?)", saved_accounts)
    system_instance.conn.commit()


# generates a random string based on the provided parameters
# @param length - the total number of characters in the string
# @param num_upper - the number of uppercase characters in the string
# @param num_digits - the number of digits in the string
# @param num_special - the number of special characters in the string
def generate_random_string(length, num_upper, num_digits, num_special):
    special = r'[\!@#\$%\^&\*\(\)_\+\-\=\[\]\{\}\|\;\:\,\.\<\>\/\?\`\~\'\"\\]'
    selected_chars = []
    # exception sum of number of uppercase, digits, and specials must not exceed string length
    if length < (num_upper + num_digits + num_special):
        raise Exception("Total number of uppercase, digits, and special characters exceeds length.")
    # add special characters
    for i in range(num_special):
        selected_chars.append(random.choice(special))
    # add digits
    for i in range(num_digits):
        selected_chars.append(random.choice(string.digits))
    # add uppercase letter
    for i in range(num_upper):
        selected_chars.append(random.choice(string.ascii_uppercase))
    # add remaining lowercase letters
    length = length - num_digits - num_special - num_upper
    for i in range(length):
        selected_chars.append(random.choice(string.ascii_lowercase))
    # shuffle password and return as string
    random.shuffle(selected_chars)
    return ''.join(selected_chars)


# tests that passwords are validated according to the appropriate criteria
def test_validate_password(system_instance, capfd):
    msg_pass_length = "Password must be 8-12 Characters in Length"
    msg_pass_upper = "Password must contain at least one upper case letter"
    msg_pass_digit = "Password must contain at least one number"
    msg_pass_special = "Password must contain at least one special character"
    # empty password must fail
    password = generate_random_string(0, 0, 0, 0)
    assert system_instance.validatePassword(password, password) is False
    std = capfd.readouterr()
    assert std.out.strip() == msg_pass_length
    # less than 8 characters must fail
    password = generate_random_string(3, 1, 1, 1)
    assert system_instance.validatePassword(password, password) is False
    std = capfd.readouterr()
    assert std.out.strip() == msg_pass_length
    # more than 12 characters must fail
    password = generate_random_string(13, 1, 1, 1)
    assert system_instance.validatePassword(password, password) is False
    std = capfd.readouterr()
    assert std.out.strip() == msg_pass_length
    # no uppercase letters must fail
    password = generate_random_string(8, 0, 1, 1)
    assert system_instance.validatePassword(password, password) is False
    std = capfd.readouterr()
    assert std.out.strip() == msg_pass_upper
    # no digits must fail
    password = generate_random_string(10, 1, 0, 1)
    assert system_instance.validatePassword(password, password) is False
    std = capfd.readouterr()
    assert std.out.strip() == msg_pass_digit
    # no special characters must fail
    password = generate_random_string(12, 1, 1, 0)
    assert system_instance.validatePassword(password, password) is False
    std = capfd.readouterr()
    assert std.out.strip() == msg_pass_special
    # valid password containing 8-12 chars including
    # at least 1 digit, special, and uppercase char
    for i in range(8, 13):
        password = generate_random_string(i, 1, 1, 1)
        assert system_instance.validatePassword(password, password) is True


# test that usernames are properly validated based on their length
def test_validate_username_length(system_instance, capfd):
    usr_length_msg = "Username must be 1-25 Characters in Length"
    min_len, max_len = 1, 25
    # no username / too short
    username = ''
    system_instance.conn.commit()
    result = system_instance.validateUserName(username)
    std = capfd.readouterr()
    assert result is False and std.out.strip() == usr_length_msg
    # username exceeds max length
    length = random.randint(max_len + 1, 100)
    username = generate_random_string(length, 1, 0, 0)  # contains upper character
    result = system_instance.validateUserName(username)
    std = capfd.readouterr()
    assert result is False and std.out.strip() == usr_length_msg
    # username of acceptable length
    while True:  # generate username and ensure uniqueness
        length = random.randint(min_len, max_len)
        username = generate_random_string(length, 0, 1, 0)  # contains digit character
        system_instance.cursor.execute("SELECT * FROM accounts WHERE username = ?", (username,))
        account = system_instance.cursor.fetchone()
        if account is None:
            break
    # confirm username is validated successfully
    result = system_instance.validateUserName(username)
    capfd.readouterr()
    assert result is True


# tests that usernames are validated based on uniqueness
def test_validate_username_not_unique(system_instance, capfd):
    # username not unique (already taken)
    usr_taken_msg = "Username has been taken."
    system_instance.cursor.execute('SELECT username FROM accounts LIMIT 1')
    username = system_instance.cursor.fetchone()
    test_user = True
    if not username:  # no accounts, create a test user
        length = random.randint(5, 25)
        username = generate_random_string(length, 1, 0, 0)
        length = random.randint(8, 12)
        password = generate_random_string(length, 1, 1, 1)
        registered = system_instance.register(username, password, password)
        capfd.readouterr()  # discard account register success msg
        assert registered is True
    else:
        test_user = False
    # confirm non-unique username is rejected and appropriate message displayed
    result = system_instance.validateUserName(username[0])
    std = capfd.readouterr()
    assert result is False and std.out.strip() == usr_taken_msg
    if test_user:  # delete test user
        system_instance.cursor.execute('DELETE FROM accounts where username = (?)', (username,))
        system_instance.conn.commit()


# tests that the maximum number of accounts can be registered and stored in the database
# also tests that new account are rejected once the account limit is reached
def test_register_success(system_instance, capfd, temp_remove_accounts):
    account_limit = 5
    msg_max_accounts = "Maximum number of accounts created!"
    msg_reg_success = "Account created successfully."

    # register max number of accounts
    temp_accounts = []
    for i in range(account_limit):
        length = random.randint(5, 25)
        username = generate_random_string(length, 1, 1, 0)
        length = random.randint(8, 12)
        password = generate_random_string(length, 1, 1, 1)
        result = system_instance.register(username, password, password)
        std = capfd.readouterr()
        assert result is True and std.out.strip() == msg_reg_success
        password = system_instance.encryption(password)
        temp_accounts.append((username, password))

    # account limit reached, registering next account must fail
    length = random.randint(5, 25)
    username = generate_random_string(length, 1, 1, 0)
    length = random.randint(8, 12)
    password = generate_random_string(length, 1, 1, 1)
    result = system_instance.register(username, password, password)
    std = capfd.readouterr()
    user_query = "SELECT * FROM accounts WHERE (username, password) = (?, ?)"
    system_instance.cursor.execute(user_query, (username, system_instance.encryption(password)))
    account = system_instance.cursor.fetchone()
    assert result is False and std.out.strip() == msg_max_accounts and account is None

    # use a new connection to ensure registered accounts are committed
    system2 = System(False)
    users = ', '.join(['(?, ?)'] * len(temp_accounts))
    query = f"SELECT username, password FROM accounts WHERE (username, password) in ({users})"
    tmp_acc_list = [item for acc in temp_accounts for item in acc]
    system2.cursor.execute(query, tmp_acc_list)
    result = system2.cursor.fetchall()
    assert len(result) == len(temp_accounts)
    for acc in result:
        assert acc in temp_accounts


# tests that registration fails when username is invalid
def test_register_fail_username(system_instance, capfd, temp_remove_accounts):
    # msg_username_length = "Username must be less than 25 Characters in Length"
    msg_username_length = "Username must be 1-25 Characters in Length"
    msg_usr_not_unique = "Username has been taken."
    user_query = "SELECT * FROM accounts WHERE username = ?"
    # username too short (none)
    username = ''
    length = random.randint(8, 12)
    password = generate_random_string(length, 1, 1, 1)
    result = system_instance.register(username, password, password)
    std = capfd.readouterr()
    system_instance.cursor.execute(user_query, (username,))
    account = system_instance.cursor.fetchone()
    assert result is False and std.out.strip() == msg_username_length and account is None
    # username too long
    length = random.randint(26, 100)
    username = generate_random_string(length, 1, 1, 1)
    length = random.randint(8, 12)
    password = generate_random_string(length, 1, 1, 1)
    result = system_instance.register(username, password, password)
    std = capfd.readouterr()
    system_instance.cursor.execute(user_query, (username,))
    account = system_instance.cursor.fetchone()
    assert result is False and std.out.strip() == msg_username_length and account is None
    # username not unique
    length = random.randint(1, 25)
    username = generate_random_string(length, 1, 0, 0)
    length = random.randint(8, 12)
    password = generate_random_string(length, 1, 1, 1)
    for i in range(2):  # attempt to double register new user
        registered = system_instance.register(username, password, password)
        std = capfd.readouterr()
    assert registered is False and std.out.strip() == msg_usr_not_unique


# tests that registration fails when password is invalid
def test_register_fail_password(system_instance, capfd, temp_remove_accounts):
    password_warnings = {
        'length': "Password must be 8-12 Characters in Length",
        'uppercase': "Password must contain at least one upper case letter",
        'digit': "Password must contain at least one number",
        'special': "Password must contain at least one special character"
    }
    user_query = "SELECT * FROM accounts WHERE (username, password) = (?, ?)"

    # no password
    length = random.randint(5, 25)
    username = generate_random_string(length, 1, 0, 1)
    password = ''
    result = system_instance.register(username, password, password)
    std = capfd.readouterr()
    system_instance.cursor.execute(user_query, (username, system_instance.encryption(password)))
    account = system_instance.cursor.fetchone()
    assert result is False and std.out.strip() == password_warnings['length'] and account is None
    # password below minimum length
    length = random.randint(5, 25)
    username = generate_random_string(length, 1, 0, 1)
    length = random.randint(3, 7)
    password = generate_random_string(length, 1, 1, 1)
    result = system_instance.register(username, password, password)
    std = capfd.readouterr()
    system_instance.cursor.execute(user_query, (username, system_instance.encryption(password)))
    account = system_instance.cursor.fetchone()
    assert result is False and std.out.strip() == password_warnings['length'] and account is None
    # password exceeds maximum length
    length = random.randint(5, 25)
    username = generate_random_string(length, 1, 0, 1)
    length = random.randint(13, 100)
    password = generate_random_string(length, 1, 1, 1)
    result = system_instance.register(username, password, password)
    std = capfd.readouterr()
    system_instance.cursor.execute(user_query, (username, system_instance.encryption(password)))
    account = system_instance.cursor.fetchone()
    assert result is False and std.out.strip() == password_warnings['length'] and account is None
    # no uppercase letter in password
    length = random.randint(5, 25)
    username = generate_random_string(length, 1, 0, 1)
    length = random.randint(8, 12)
    password = generate_random_string(length, 0, 1, 1)
    result = system_instance.register(username, password, password)
    std = capfd.readouterr()
    system_instance.cursor.execute(user_query, (username, system_instance.encryption(password)))
    account = system_instance.cursor.fetchone()
    assert result is False and std.out.strip() == password_warnings['uppercase'] and account is None
    # no digit in password
    length = random.randint(5, 25)
    username = generate_random_string(length, 1, 0, 1)
    length = random.randint(8, 12)
    password = generate_random_string(length, 1, 0, 1)
    result = system_instance.register(username, password, password)
    std = capfd.readouterr()
    system_instance.cursor.execute(user_query, (username, system_instance.encryption(password)))
    account = system_instance.cursor.fetchone()
    assert result is False and std.out.strip() == password_warnings['digit'] and account is None
    # no special character in password
    length = random.randint(5, 25)
    username = generate_random_string(length, 1, 0, 1)
    length = random.randint(8, 12)
    password = generate_random_string(length, 1, 1, 0)
    result = system_instance.register(username, password, password)
    std = capfd.readouterr()
    system_instance.cursor.execute(user_query, (username, system_instance.encryption(password)))
    account = system_instance.cursor.fetchone()
    assert result is False and std.out.strip() == password_warnings['special'] and account is None


# tests that the register menu prompts the user for username and password
def test_login_menu_register(system_instance, capfd):
    # register menu prompts
    msg_enter_username = "Enter Username: "
    msg_enter_password = "Enter Password: "
    msg_confirm_pass = "Confirm Password: "
    # simulated inputs for testing register menu
    register = '2'
    length = random.randint(5, 25)
    username = generate_random_string(length, 0, 1, 0)
    length = random.randint(8, 12)
    password = generate_random_string(length, 1, 1, 1)
    pass_check = 'fail'
    exit_app = '0'
    inputs = [register, username, password, pass_check, exit_app]

    # run the registration menu with the simulated inputs
    with mock.patch('builtins.input', side_effect=inputs) as mock_input:
        system_instance.loginMenu()

    # clear additional non-input prompts
    capfd.readouterr()

    #  check that all registration prompts were displayed
    mock_input.assert_has_calls([
        mock.call(msg_enter_username),
        mock.call(msg_enter_password),
        mock.call(msg_confirm_pass)
    ])


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
