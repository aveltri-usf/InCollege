import os
import pytest
import sqlite3
from unittest import mock
from unittest.mock import Mock
from unittest.mock import patch
from system import Menu, Jobs, System


@pytest.fixture #creates instance of System and calls Main Menu
def system_instance():
  s1 = System()
  s1.initMenu()
  return s1

@pytest.fixture #removes existing accounts from db while testing
def temp_remove_accounts(system_instance): 
  system_instance.cursor.execute("SELECT * FROM accounts")
  saved_accounts = system_instance.cursor.fetchall()
  if len(saved_accounts) > 0:
    system_instance.cursor.execute("DELETE FROM accounts")
    system_instance.conn.commit()
  yield
  system_instance.cursor.execute("DELETE FROM accounts")
  if len(saved_accounts) > 0:
    system_instance.cursor.executemany(
      "INSERT INTO accounts (username, password, fName, lName) VALUES (?, ?, ?, ?)",
      saved_accounts)
  system_instance.conn.commit()


# Check for Find People I Know Option
def test_find_people(system_instance):
  system_instance = System()  # Create an instance of the System class
  system_instance.initMenu()
  # Get the menu items from the homePage
  menu_items = system_instance.homePage.selections
  # Check if the "InCollege Important Links" option exists in the home page manu
  find_people = next(
    (item
      for item in menu_items if item['label'] == 'Find People I Know'),
    None)
  # Assert that the option exists
  assert find_people is not None

# Check for first and last name prompts
def test_name_prompt(system_instance, capsys):
  # simulate user choosing Find People I Know Option
  with mock.patch('builtins.input', side_effect=['3', 'John', 'Doe', '0', '0']):
    system_instance.home_page()

  # capture output
  captured = capsys.readouterr()

  # assert user is prompted for first and last name
  assert "Enter First Name:" in captured.out
  assert "Enter Last Name:" in captured.out


# Query accounts table for matching first and last name
def test_query_names(system_instance, temp_remove_accounts, capsys):
  first_name = "jane"
  last_name = "smith"

  # simulate creating an account and then simulate user searching for that person
  with mock.patch('builtins.input', side_effect=['2', 'Jane35', first_name, last_name, 'Testing12*', 'Testing12*', 'Jane35', 'Testing12*', '0', '0']):
    system_instance.home_page()

  system_instance.cursor.execute(
    "SELECT * FROM accounts WHERE UPPER(fName) = UPPER(?) AND UPPER(lName) = UPPER(?)",
    (first_name, last_name))

  result_lower = system_instance.cursor.fetchall()

  assert len(result_lower) > 0

  system_instance.cursor.execute(
    "SELECT * FROM accounts WHERE UPPER(fName) = UPPER(?) AND UPPER(lName) = UPPER(?)",
    (first_name.capitalize(), last_name.capitalize()))

  result_capital = system_instance.cursor.fetchall()

  assert len(result_capital) > 0


# Check for message when user is located
def test_user_located(system_instance, temp_remove_accounts, capsys):
  # simulate creating an account and then simulate user searching for that person
  with mock.patch('builtins.input', side_effect=['2', 'Jane35', 'Jane', 'Smith', 'Testing12*', 'Testing12*','Jane35', 'Testing12*', '0', '3', 'Jane', 'Smith', '0', '0']):
    system_instance.home_page()

  # capture output
  captured = capsys.readouterr()

  assert "They Are Part Of The InCollege System." in captured.out


# Check for message when user not in system
def test_user_not_located(system_instance, capsys):
  # simulate user choosing Find People I Know Option
  with mock.patch('builtins.input', side_effect=['3', 'John', 'Doe', '0','0']):
    system_instance.home_page()

  # capture output
  captured = capsys.readouterr()

  # assert user is prompted for first and last name
  assert "They Are Not Yet A Part Of The InCollege System." in captured.out


# Check that join menu appears when a user finds someone they know
def test_join_menu(system_instance, temp_remove_accounts, capsys):
  join_msg = "Would You Like To Join Your Friends On InCollege?"
  join_menu = ["Login", "Register", "Return To Home Page"]

  # simulate creating an account and then simulate user searching for that person
  with mock.patch('builtins.input', side_effect=['2', 'Jane35', 'Jane', 'Smith', 'Testing12*', 'Testing12*', 'Jane35', 'Testing12*', '0', '3', 'Jane', 'Smith', '0', '0']):
    system_instance.home_page()

  # capture output
  captured = capsys.readouterr()

  assert join_msg in captured.out
  for item in join_menu:
    assert item in captured.out


# Check that video option is availabe
def test_video_option(system_instance, capsys):
  system_instance = System()  # Create an instance of the System class
  system_instance.initMenu()
  # Get the menu items from the homePage
  menu_items = system_instance.homePage.selections
  # Check if the "InCollege Important Links" option exists in the home page manu
  videos = next(
    (item
      for item in menu_items if item['label'] == 'See Our Success Video'),
    None)
  # Assert that the option exists
  assert videos is not None
  # simulate user choosing video option
  with mock.patch('builtins.input', side_effect=['4', '0', '0']):
    system_instance.home_page()

  # capture output
  captured = capsys.readouterr()

  # assert expected output
  assert "(Playing Video)" in captured.out


# Check to see that success story is displayed
def test_student_success(system_instance, capsys):
  # access homePage attribute
  home_page = system_instance.homePage

  success_story = """
      Welcome To The InCollege Home Page!
      
      The Place Where Students Take The Next Big Step.

      "I Had To Battle With Anxiety Every Day Until I Signed Up For InCollege.
       Now, My Future Is On The Right Track And Im Able To Apply My Education To My 
       Dream Career. Finding A Place In My Field Of Study Was A Breeze"
        - InCollege User

    """

  assert home_page.opening == success_story


#@pytest.fixture
#test that user can input first and last name when registering
def test_name_register(system_instance, temp_remove_accounts, capsys):
  # username = "test"
  # fName = "unit"
  # lName = "tests"
  # password = "Testing2$"
  # passwordCheck = "Testing2$"
  inputs = ['2', 'test', 'unit', 'tests', 'Testing2!', 'Testing2!', 'test', 'Testing2!', '0', '0']
  with mock.patch('builtins.input', side_effect=inputs):
    system_instance.home_page()
  captured = capsys.readouterr()
  output = captured.out.split('\n')
  assert output[21] == 'Account created successfully.'#22nd line of ouput from the program should be Account created successfully

def test_name_db(system_instance, temp_remove_accounts, name_register):#test that the users first and last name are stored in the db under fName and lName which are the second and third column
  fName = "unit"
  cursor = system_instance.conn.cursor()
  cursor.execute('Select * From accounts where fName = (?);', (fName,))
  result = cursor.fetchone()
  assert result[2] == 'unit' and result[3] == 'tests' 

@pytest.fixture
#test that user can input first and last name when registering
def name_register(system_instance, temp_remove_accounts, capsys):
  # username = "test"
  # fName = "unit"
  # lName = "tests"
  # password = "Testing2$"
  # passwordCheck = "Testing2$"
  inputs = ['2', 'tester', 'unit', 'tests', 'Testing3!', 'Testing3!', 'tester', 'Testing3!', '0', '0']
  with mock.patch('builtins.input', side_effect=inputs):
    system_instance.home_page()
  captured = capsys.readouterr()
  output = captured.out.split('\n')
  assert output[21] == 'Account created successfully.'#22nd line of ouput from the program should be Account created successfully
  yield

#@pytest.fixture#test that user can input first and last name when registering
def test_register(system_instance, capsys, temp_remove_accounts):
  inputs = ['2', 'tester', 'unit', 'tests', 'Testing3!', 'Testing3!', 'tester', 'Testing3!', '0', '0']
  with mock.patch('builtins.input', side_effect=inputs):
    system_instance.home_page()
  captured = capsys.readouterr()
  output = captured.out.split('\n')
  assert output[16] == 'Enter Username: '
  assert output[17] == 'Enter First Name: '
  assert output[18] == 'Enter Last Name: '
  assert output[19] == 'Enter Password: '
  assert output[20] == 'Confirm Password: '
  assert output[21] == 'Account created successfully.'

def test_login(system_instance, capsys, name_register):
  inputs = ['1', 'tester', 'Testing3!', '1', '0', '2', '0', '3', '0', '0', '0']
  with mock.patch('builtins.input', side_effect=inputs):
    system_instance.home_page()
  captured = capsys.readouterr()
  output = captured.out.split('\n')
  assert output[16] == 'Log In:'
  assert output[18] == 'Enter Username: '
  assert output[19] == 'Enter Password: '
  assert output[20] == 'You Have Successfully Logged In!'
  assert output[21] == 'Welcome User!'
  assert output[22] == '[1] Job/Internship Search'
  assert output[23] == '[2] Find A Friend'
  assert output[24] == '[3] Learn A Skill'
  assert output[25] == '[0] Log Out'
  assert output[26] == 'Welcome to the Job Postings Page'
  assert output[27] == '[1] Post Job'
  assert output[28] == '[0] Return To Main Menu'
  assert output[30] == 'Welcome User!'
  assert output[31] == '[1] Job/Internship Search'
  assert output[32] == '[2] Find A Friend'
  assert output[33] == '[3] Learn A Skill'
  assert output[34] == '[0] Log Out'
  assert output[36] == '[0] Exit'
  assert output[38] == 'Welcome User!'
  assert output[39] == '[1] Job/Internship Search'
  assert output[40] == '[2] Find A Friend'
  assert output[41] == '[3] Learn A Skill'
  assert output[42] == '[0] Log Out'
  assert output[43] == 'Please Select a Skill:'
  assert output[44] == '[1] Project Management'
  assert output[45] == '[2] Networking'
  assert output[46] == '[3] System Design'
  assert output[47] == '[4] Coding'
  assert output[48] == '[5] Professional Communication'
  assert output[49] == '[0] Return To Main Menu'

def test_findpeople(system_instance, capsys, name_register):
  inputs = ['3', 'unit', 'tests', '0', '0']
  with mock.patch('builtins.input', side_effect=inputs):
    system_instance.home_page()
  captured = capsys.readouterr()
  output = captured.out.split('\n')
  assert output[16] == 'Enter First Name: '
  assert output[17] == 'Enter Last Name: '
  assert output[18] == 'They Are Part Of The InCollege System.'
  assert output[19] == 'Would You Like To Join Your Friends On InCollege?'
  assert output[20] == '[1] Login'
  assert output[21] == '[2] Register'
  assert output[22] == '[0] Return To Home Page'

def test_success_video(system_instance, capsys):
  inputs = ['4', '0', '0']
  with mock.patch('builtins.input', side_effect=inputs):
    system_instance.home_page()
  captured = capsys.readouterr()
  output = captured.out.split('\n')
  assert output[16] == 'See Our Success Story:'
  assert output[17] == '(Playing Video)'
  assert output[19] == '[0] Exit'

# test this function: Create a jobs class with members: title, description, employer, location, salary, poster first name and last name.
def test_job_creation_with_description():
    job = Jobs(title="Software Engineer", employer="ABC Company", location="New York", salary=100000,
               posterFirstName="John", posterLastName="Doe", description="Job description")

    assert job.title == "Software Engineer"
    assert job.employer == "ABC Company"
    assert job.location == "New York"
    assert job.salary == 100000
    assert job.posterFirstName == "John"
    assert job.posterLastName == "Doe"
    assert job.description == "Job description"


def test_job_creation_with_default_values():
    job = Jobs(title="", employer="", location="", salary=0, posterFirstName="", posterLastName="")

    assert job.title == ""
    assert job.employer == ""
    assert job.location == ""
    assert job.salary == 0
    assert job.posterFirstName == ""
    assert job.posterLastName == ""
    assert job.description is None

#Create a jobs table in the database with fields: title, description, employer, location, salary, poster (first and last name). 


# # this method  verify if the 'jobs' table is successfully created in the database.
def test_jobs_table_creation(): 
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()
    # Check if the 'jobs' table exists in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='jobs'")
    table_exists = cursor.fetchone()
    conn.close()
    # Assert that the 'jobs' table exists
    assert table_exists is not None


# # this method is to ensure that the 'jobs' table is created with the correct attributes and schema.

def test_jobs_table_creation_withFields(): 
    # Connect to the database
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()
    # Get the column names of the jobs table
    cursor.execute("PRAGMA table_info(jobs)")
    columns = cursor.fetchall()
    column_names = [column[1] for column in columns]
    # Define the expected column names
    expected_columns = [
        'title',
        'description',
        'employer',
        'location',
        'salary',
        'posterFirstName',
        'posterLastName'
    ]
    # Assert that the column names match the expected column names
    assert column_names == expected_columns
    # Cleanup: Close the connection
    conn.close()



#Test that includes checking the field types and primary keys of the jobs table:

def test_jobs_table_schema():
    # Connect to the database
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()
    # Get the column information of the jobs table
    cursor.execute("PRAGMA table_info(jobs)")
    columns = cursor.fetchall()
    # Define the expected field types and primary keys
   #A value of 1 means the column does not allow NULL values, and 0 means NULL values are allowed.
    expected_schema = {
        'title': ('VARCHAR(128)', 0, None, 1),
        'description': ('TEXT', 0, None, 0),
        'employer': ('VARCHAR(128)', 1, None, 0),
        'location': ('VARCHAR(128)', 1, None, 0),
        'salary': ('INT', 1, None, 0),
        'posterFirstName': ('VARCHAR(128)', 0, None, 0),
        'posterLastName': ('VARCHAR(128)', 0, None, 0)
    }
 # Iterate over the columns and compare with expected schema
    for column in columns:
        column_name = column[1]
        field_type = column[2]
        is_primary_key = column[5]
        # Assert field type
        assert field_type == expected_schema[column_name][0]
        # Assert primary key
        assert is_primary_key == expected_schema[column_name][3]
    # Cleanup: Close the connection
    conn.close()


  #story: As I developer, I want to fix outstanding issues from previous sprint, so that the product owner is satisfied.

# Replace Skill A-E placeholders with actual skill names.

def test_skillA(capsys):
  system = System()
  system.skillA()
  captured = capsys.readouterr()
  assert "Project Management" in captured.out
  assert "Under Construction" in captured.out


def test_skillB(capsys):
  system = System()
  system.skillB()
  captured = capsys.readouterr()
  assert "Networking" in captured.out
  assert "Under Construction" in captured.out


def test_skillC(capsys):
  system = System()
  system.skillC()
  captured = capsys.readouterr()
  assert "System Design" in captured.out
  assert "Under Construction" in captured.out


def test_skillD(capsys):
  system = System()
  system.skillD()
  captured = capsys.readouterr()
  assert "Coding" in captured.out
  assert "Under Construction" in captured.out


def test_skillE(capsys):
  system = System()
  system.skillE()
  captured = capsys.readouterr()
  assert "Professional Communication" in captured.out
  assert "Under Construction" in captured.out

  def test_guestSearch(capsys):
    system = System()
    system.guestSearch()
    captured = capsys.readouterr()
    assert "Professional Communication" in captured.out
    assert "Under Construction" in captured.out


#Convert all prompts to title case
def is_title_case(string):
     return string.istitle()

@pytest.mark.parametrize("prompt", [
     "Welcome To The Incollege Home Page!",
      
     "The Place Where Students Take The Next Big Step.",

      ])
def test_prompt_title_case(prompt):
    assert is_title_case(prompt), f"Prompt '{prompt}' is not in title case"


#Clear the console each time before a new menu is displayed.
def test_clear_console_before_menu_display():
    # Instantiate the Menu class
    menu = Menu()
    
    # Mock the os.system method to capture the console clear command
    with mock.patch('os.system') as mock_system:
        # Call the displaySelections method
        menu.clear()
        
        # Assert that the os.system method was called with the clear command
        mock_system.assert_called_with('clear' if os.name != 'nt' else 'cls')


# #story: As a signed in user, I want to be able to post a job including details about the title, description, employer, location, and salary.
# Add a "Post A Job" option to the "Job Search/Internship" menu.
def test_addPostJobOption(system_instance):
  # access main menu attribute
  mainmenu =system_instance.mainMenu
  #acces job menu attribute 
  jobmenu =system_instance.jobsMenu
  #check if the job/searchInsership is in the main menu
  assert '1' in mainmenu.selections, "Selection '1' not found in jobs menu options"
  assert mainmenu.selections['1'] == {
    'label': 'Job/Internship Search',
    'action': system_instance.jobs_menu
  }
  #check that the Post Job option is in the menu under job/search
  assert jobmenu.opening == "Welcome to the Job Postings Page"
  assert jobmenu.selections['1'] == {
    'label': 'Post Job',
    'action': system_instance.postJob
  }
  assert jobmenu.exitStatement == "Return To Main Menu"


# When the user selects "Post A Job" they should be prompted for a title, description, employer, location, and salary.
def test_post_job_prompt(monkeypatch, capsys):
    system_instance = System()
  # Prepare inputs for the postJob function
    monkeypatch.setattr('builtins.input', lambda : '')
    monkeypatch.setattr('builtins.input', lambda : '')
    monkeypatch.setattr('builtins.input', lambda : '')
    monkeypatch.setattr('builtins.input', lambda : '')
    monkeypatch.setattr('builtins.input', lambda : '')

    # Call the postJob function
    system_instance.postJob()

    # Capture the output
    captured = capsys.readouterr()

    # Assert the expected output
    assert "Enter Title: " in captured.out
    assert "Enter Description: " in captured.out
    assert "Enter Employer: " in captured.out
    assert "Enter Location: " in captured.out
    assert "Enter Salary: " in captured.out


# #The system will permit up to 5 jobs to be posted.
# #this function is to test if the system limit the user to post more than 5 jobs. 
def test_postJobLimitReached(capsys):
    # Create an instance of the System class or a mock object if available
    system = System()
    # Mock the countRows method to return a value equal to the job post limit (5)
    system.countRows = Mock(return_value=5)
    # Call the postJob method
    result = system.postJob()
    # Assert that the maximum jobs limit message is printed
    captured = capsys.readouterr()
    assert captured.out.strip() == "Maximum Number Of Jobs Posts Created!"
    # Assert that the method returns None
    assert result is None


# test to check that the Job is saved into the data base correctly
@pytest.fixture
def system_instance_2():
    # Create an instance of the System class or initialize your system
  # delete the value of the table job to do the test 
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM jobs")
    conn.commit()
    conn.close()
  
    system = System()

    # Perform any necessary setup or data insertion for the test
    # For example, insert test data into the database
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO jobs (title, description, employer, location, salary, posterFirstName, posterLastName) VALUES (?, ?, ?, ?, ?, ?, ?)", ('Test Job Title', 'Test Job Description', 'Test Employer', 'Test Location', 50000.00, 'John', 'Doe'))
    conn.commit()
    conn.close()

    # Return the system instance for the test
    return system

# this test check that the job was posted correctly into the data base . 
def test_job_created_correctlyInDataBase(system_instance_2):
    # Retrieve the inserted job data from the database
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs WHERE title=?", ('Test Job Title',))
    result = cursor.fetchone()
    conn.close()

    # Assert that the job data matches the expected values
    assert result[0] == "Test Job Title"
    assert result[1] == "Test Job Description"
    assert result[2] == "Test Employer"
    assert result[3] == "Test Location"
    assert result[4] == 50000.00
    assert result[5] == "John"
    assert result[6] == "Doe"

# this test make sure a valid salary when post a job 
def test_post_job_with_invalid_salary():
    system = System()
    # Define the invalid salary input
    invalid_salary = "Invalid Salary"
    
    # Use patch to mock the behavior of input() and provide the input values
    with patch('builtins.input', side_effect=['Title', 'Description', 'Employer', 'Location', invalid_salary]):
        # Call the postJob function
        result = system.postJob()
        
    # Perform assertions on the result
    assert result is None
