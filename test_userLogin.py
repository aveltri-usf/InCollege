import pytest
from system import System

def test_validate_valid_password():
      system = System(loggedOn=False)
      # Call the validate function with a valid password
      valid_password = "ValidPas123!"
      valid_password_again = "ValidPas123!"
      result = system.validatePassword(valid_password,valid_password_again)
      # Assert that the result is True
      assert result is True

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


