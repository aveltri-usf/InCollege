import pytest
from system import System
from unittest import mock
from unittest.mock import patch
from io import StringIO

#story: As a new user, I want to be able to learn about important information about InCollege
def test_inCollegeImportantInformationHomePage():
    system_instance = System()  # Create an instance of the System class
    system_instance.initMenu()
    # Get the menu items from the homePage
    menu_items = system_instance.homePage.selections
    # Check if the "InCollege Important Links" option exists in the home page manu
    inCollege_links_option = next((item for item in menu_items if item['label'] == 'InCollege Important Links'), None)
    # Assert that the option exists
    assert inCollege_links_option is not None

#
def test_inCollageImportantInformationMainMenu():
    system_instance = System()
   # Call the initMenu method to initialize the menu
    system_instance.initMenu()
    # Get the menu items from the mainMenu
    menu_items = system_instance.mainMenu.selections
    # Check if the "InCollege Important Links" option exists in the main manu
    inCollege_links_option = next((item for item in menu_items if item['label'] == 'InCollege Important Links'), None)
    # Assert that the option exists
    assert inCollege_links_option is not None

# test to check when the user select the option 6 it display the menu for inCollage important links
def test_incollege_important_links_SubMenu(monkeypatch, capfd):
    system = System()
# Simulate user input
    user_input = "6\n"
    # Monkeypatch the input function to provide user input
    monkeypatch.setattr('builtins.input', lambda _: user_input)
    # Call the function that captures user input
    result = system.initMenu()
    # Capture the console output
    captured = capfd.readouterr()
    # Assert the captured output matches the expected output
    assert captured.out == "Welcome to the Important Links Page"
    assert captured.out =="[1] Copyright Notice"
    assert captured.out =="[2] About"
    assert captured.out =="[3] Accessibility"
    assert captured.out =="[4] User Agreement"
    assert captured.out =="[5] Privacy Policy"
    assert captured.out =="[6] Cookie Policy"
    assert captured.out =="[7] Brand Policy"
    assert captured.out =="[0] Return To Home Page"
    assert captured.out == "Enter the number of your selection: "
    # Assert the captured input matches the user input
    assert result == user_input
  
# #Task 1:Add a "Copyright Notice" link and have it contain relevant content 

def test_copyRightNoticelink(capsys):
    system_instance = System()
   # Call the initMenu method to initialize the menu
    system_instance.initMenu()
    # Get the menu items from the mainMenu
    menu_items = system_instance.importantLinks.selections
    # Check if the "InCollege Important Links" option exists in the main manu
    inCollege_links_option = next((item for item in menu_items if item['label'] == 'Copyright Notice'), None)
    # Assert that the option exists
    assert inCollege_links_option is not None
# Select the Copy Rigth Notice Option 
def test_copyRightNoticelinkCon(capfd,monkeypatch):
    system = System()
    # Simulate user input
    user_input = "6\n1\n0\n"  # Input sequence: Select option 6, then option 1, then option 0
    # Monkeypatch the input function to provide user input
    monkeypatch.setattr('builtins.input', lambda _: user_input)
    # Call the menu function
    system.initMenu()
    # Capture the console output
    captured = capfd.readouterr()
    # Assert the captured output contains the expected menus and text
    expected_output = """

Welcome To The InCollege Home Page!

The Place Where Students Take The Next Big Step.

"I Had To Battle With Anxiety Every Day Until I Signed Up For InCollege.
Now, My Future Is On The Right Track And Im Able To Apply My Education To My Dream Career.
Finding A Place In My Field Of Study Was A Breeze"
- InCollege User

[1] Login
[2] Register
[3] Find People I Know
[4] See Our Success Video
[5] Useful Links
[6] InCollege Important Links
[0] Exit

Enter the number of your selection: 
Welcome to the Important Links Page

[1] Copyright Notice
[2] About
[3] Accessibility
[4] User Agreement
[5] Privacy Policy
[6] Cookie Policy
[7] Brand Policy
[0] Return To Home Page

Enter the number of your selection: 
---------------------------
  COPYRIGHT NOTICE
---------------------------

All content and materials displayed on the InCollege website, including but not limited to text, graphics, logos, images, audio clips, and software, are the property of InCollege and are protected by international copyright laws.

The unauthorized reproduction, distribution, or modification of any content on the InCollege website is strictly prohibited without prior written permission from InCollege.

For any inquiries regarding the use of our copyrighted materials, please contact us at legal@incollege.com.

By accessing and using the InCollege website, you agree to comply with all applicable copyright laws and regulations.

---------------------------

[0] Back

Enter the number of your selection: 
"""

    assert captured.out.strip() == expected_output.strip()

# #Task 2:Add an "About" link and have it contain a history of the company and why it was created.

def test_aboutLink(capsys):
    system_instance = System()
   # Call the initMenu method to initialize the menu
    system_instance.initMenu()
    # Get the menu items from the mainMenu
    menu_items = system_instance.importantLinks.selections
    # Check if the "InCollege Important Links" option exists in the main manu
    inCollege_links_option = next((item for item in menu_items if item['label'] == 'About'), None)
    # Assert that the option exists
    assert inCollege_links_option is not None  

#Task 3:Add a "User Agreement" link and have it contain relevant content
def test_userAgreement(capsys):
    system_instance = System()
   # Call the initMenu method to initialize the menu
    system_instance.initMenu()
    # Get the menu items from the mainMenu
    menu_items = system_instance.importantLinks.selections
    # Check if the "InCollege Important Links" option exists in the main manu
    inCollege_links_option = next((item for item in menu_items if item['label'] == 'User Agreement'), None)
    # Assert that the option exists
    assert inCollege_links_option is not None
#Task 4:Add a "Privacy Policy" link and have it contain relevant content

def test_privacyPolicy(capsys):
    system_instance = System()
   # Call the initMenu method to initialize the menu
    system_instance.initMenu()
    # Get the menu items from the mainMenu
    menu_items = system_instance.importantLinks.selections
    # Check if the "InCollege Important Links" option exists in the main manu
    inCollege_links_option = next((item for item in menu_items if item['label'] == 'Privacy Policy'), None)
    # Assert that the option exists
    assert inCollege_links_option is not None

# #Task5:Add a "Cookie Policy" link and have it contain relevant content

def test_cookiePolicy(capsys):
    system_instance = System()
   # Call the initMenu method to initialize the menu
    system_instance.initMenu()
    # Get the menu items from the mainMenu
    menu_items = system_instance.importantLinks.selections
    # Check if the "InCollege Important Links" option exists in the main manu
    inCollege_links_option = next((item for item in menu_items if item['label'] == 'Cookie Policy'), None)
    # Assert that the option exists
    assert inCollege_links_option is not None
    
# #Task6: Clicking the Privacy Policy link will provide the user with the option to access Guest Controls, but only when they are logged in 
# def test_PrivacyPolicyGuestControls(capsys):
#   system=System()
#   inputs = ['4', '0', '0']
#   with mock.patch('builtins.input', side_effect=inputs):
#     system.home_page()
#   captured = capsys.readouterr()
#   output = captured.out.split('\n')
#   assert output[16] == 'Privacy Policy'
#   assert output[17] == 'Guest Controls'
#   assert output[19] == '[0] Exit'



# #Task7:Add a "Brand Policy" link and have it contain relevant content

def test_brandPolicy(capsys):
    system_instance = System()
   # Call the initMenu method to initialize the menu
    system_instance.initMenu()
    # Get the menu items from the mainMenu
    menu_items = system_instance.importantLinks.selections
    # Check if the "InCollege Important Links" option exists in the main manu
    inCollege_links_option = next((item for item in menu_items if item['label'] == 'Brand Policy'), None)
    # Assert that the option exists
    assert inCollege_links_option is not None

def test_Accessibility(capsys):
    system_instance = System()
   # Call the initMenu method to initialize the menu
    system_instance.initMenu()
    # Get the menu items from the mainMenu
    menu_items = system_instance.importantLinks.selections
    # Check if the "InCollege Important Links" option exists in the main manu
    inCollege_links_option = next((item for item in menu_items if item['label'] == 'Accessibility'), None)
    # Assert that the option exists
    assert inCollege_links_option is not None


# #Task8:Add a "Language" link Note: The option to change language is only available when the user is logged in
# def test_language(capsys):
#   system=System()
#    # access main menu attribute
#   mainmenu =system.mainMenu
  
#   assert '1' in mainmenu.selections, "Selection '1' not found in jobs menu options"
#   assert mainmenu.selections['1'] == {
#     'label': 'Job/Internship Search',
#     'action': system.jobs_menu
#   }


# #story: As a signed in user, I want to be able to switch the language

# #Task 1:Add an option to switch to Spanish

# def test_switchToSpanish(capsys):
#   system=System()
#    # access main menu attribute
#   mainmenu =system.mainMenu
  
#   assert '1' in mainmenu.selections, "Selection '1' not found in jobs menu options"
#   assert mainmenu.selections['1'] == {
#     'label': 'Job/Internship Search',
#     'action': system.jobs_menu
#   }
# #Task2: Add an option to switch to English, Language should be English by default 

# def test_switchToEnglish(capsys):
#   system=System()
#    # access main menu attribute
#   mainmenu =system.mainMenu
  
#   assert '1' in mainmenu.selections, "Selection '1' not found in jobs menu options"
#   assert mainmenu.selections['1'] == {
#     'label': 'Job/Internship Search',
#     'action': system.jobs_menu
#   }